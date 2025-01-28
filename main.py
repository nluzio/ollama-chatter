import streamlit as st
import requests
import json
import re
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from openinference.semconv.trace import SpanAttributes, OpenInferenceSpanKindValues

@st.cache_resource
def init_telemetry():
    # Initialize with proper resource attributes
    resource = Resource.create({
        "service.name": "ollama-chatter",
        "service.version": "1.0.0",
        "deployment.environment": "development"
    })
    
    tracer_provider = TracerProvider(resource=resource)
    # Configure OTLP exporter for Phoenix
    otlp_exporter = OTLPSpanExporter(
        endpoint="http://localhost:6006/v1/traces"
    )
    tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    trace.set_tracer_provider(tracer_provider)
    return trace.get_tracer(__name__)

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434/api"):
        self.base_url = base_url
    
    def get_available_models(self):
        """Get list of available models from Ollama"""
        try:
            response = requests.get(f"{self.base_url}/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [model["name"] for model in models]
            return []
        except Exception as e:
            st.error(f"Error fetching models: {e}")
            return []
    
    def chat(self, model, messages, system_prompt=None):
        with tracer.start_as_current_span(
            "ollama.chat",
            attributes={
                SpanAttributes.OPENINFERENCE_SPAN_KIND: OpenInferenceSpanKindValues.LLM.value,
                SpanAttributes.LLM_MODEL_NAME: model,
                SpanAttributes.LLM_PROVIDER: "ollama",
                SpanAttributes.LLM_INVOCATION_PARAMETERS: json.dumps({
                    "temperature": 0.7,
                    "top_p": 1.0,
                    "max_tokens": 2048
                })
            }
        ) as span:
            try:
                # Set current input value (last message)
                span.set_attribute(SpanAttributes.INPUT_VALUE, messages[-1]["content"])
                
                # Prepare messages and set input attributes
                chat_messages = messages.copy()  # Create a copy to avoid modifying original
                if system_prompt:
                    chat_messages.insert(0, {"role": "system", "content": system_prompt})

                # Set conversation history
                for idx, msg in enumerate(chat_messages):
                    span.set_attribute(f"{SpanAttributes.LLM_INPUT_MESSAGES}.{idx}.message.role", msg["role"])
                    span.set_attribute(f"{SpanAttributes.LLM_INPUT_MESSAGES}.{idx}.message.content", msg["content"])
                
                # Make request
                response = requests.post(
                    f"{self.base_url}/chat",
                    json={
                        "model": model,
                        "messages": chat_messages,
                        "stream": False
                    }
                )
                response.raise_for_status()
                content = response.json()["message"]["content"]
                
                # Set output value and message attributes
                span.set_attribute(SpanAttributes.OUTPUT_VALUE, content)
                span.set_attribute(f"{SpanAttributes.LLM_OUTPUT_MESSAGES}.0.message.role", "assistant")
                span.set_attribute(f"{SpanAttributes.LLM_OUTPUT_MESSAGES}.0.message.content", content)
                span.set_attribute(SpanAttributes.LLM_TOKEN_COUNT_COMPLETION, len(content.split()))
                
                # Set success status
                span.set_status(trace.Status(trace.StatusCode.OK))
                
                return content
                
            except Exception as e:
                span.record_exception(e)
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                st.error(f"Error generating response: {e}")
                return None

def parse_thinking(text):
    """Parse text to separate thinking process from regular response"""
    # Look for various thinking tag formats
    thinking_patterns = [
        r'<think>(.*?)</think>',
        r'<think>(.*?)</think\?>',
        r'\*thinks\*(.*?)\*/thinks\*',
        r'<thinking>(.*?)</thinking>'
    ]
    
    thinking_content = []
    main_content = text
    
    for pattern in thinking_patterns:
        matches = re.finditer(pattern, text, re.DOTALL)
        for match in matches:
            thinking_content.append(match.group(1).strip())
            # Remove the thinking section from main content
            main_content = main_content.replace(match.group(0), '').strip()
    
    return thinking_content, main_content

def display_message(role, content):
    """Display a message with special formatting for thinking process"""
    thinking_parts, main_content = parse_thinking(content)
    
    with st.chat_message(role):
        # Display thinking process in an expander if present
        if thinking_parts:
            with st.expander("View thinking process", expanded=False):
                for i, thinking in enumerate(thinking_parts, 1):
                    st.markdown(f"**Thinking step {i}:**")
                    st.markdown(thinking)
                st.divider()
        
        # Display main content
        if main_content:
            st.write(main_content)

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "client" not in st.session_state:
        st.session_state.client = OllamaClient()

def main():
    st.title("Ollama Chat")
    
    initialize_session_state()
    
    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        
        # Model selection
        available_models = st.session_state.client.get_available_models()
        if not available_models:
            available_models = ["run ollama pull <model_name>"]
        
        selected_model = st.selectbox(
            "Select Model",
            options=available_models
        )
        
        # System prompt
        system_prompt = st.text_area(
            "System Prompt",
            help="Enter a system prompt to guide the model's behavior"
        )
        
        # Clear chat button
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    # Display chat messages
    for message in st.session_state.messages:
        display_message(message["role"], message["content"])

    # Chat input
    if prompt := st.chat_input("Enter your message"):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_message("user", prompt)

        # Get assistant response
        response = st.session_state.client.chat(
            selected_model,
            st.session_state.messages.copy(),
            system_prompt
        )
        if response:
            display_message("assistant", response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    tracer = init_telemetry()
    main()
