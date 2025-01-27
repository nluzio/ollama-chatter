import streamlit as st
import requests
import json
import re

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
        """Send a chat request to Ollama API"""
        url = f"{self.base_url}/chat"
        
        if system_prompt:
            messages.insert(0, {
                "role": "system",
                "content": system_prompt
            })
        
        data = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()["message"]["content"]
        except Exception as e:
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
            available_models = ["llama2"]
        
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
    main()