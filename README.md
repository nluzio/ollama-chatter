# Ollama Chat UI

A Streamlit-based chat interface for interacting with local Ollama models. This application provides a user-friendly web interface to chat with various language models using Ollama's API.

## Features

- Interactive chat interface with AI models
- Support for multiple local Ollama models
- System prompt customization
- Chat history management
- Thinking process visualization
- Clear chat functionality

## Prerequisites

1. **Python 3.7+**
2. **Ollama** - Follow the installation instructions below
3. **Required Python packages** - Listed in `requirements.txt`

## Installing Ollama

### macOS

Go to [Ollama's website](https://ollama.com/download) and download the installer for macOS.

### Linux

Go to [Ollama's website](https://ollama.com/download) and download the installer for Linux.

### Windows

Go to [Ollama's website](https://ollama.com/download) and download the installer for Windows.

## Setup

1. Clone this repository:
```bash
git clone https://github.com/nluzio/ollama-chatter.git
cd ollama-chatter
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. Start the Ollama service:
```bash
ollama serve
```

4. Run the Streamlit app:
```bash
streamlit run main.py
```

## Using the App

1. **Select a Model**: Choose from available models in the sidebar. If you don't see any models, you'll need to pull them first using Ollama CLI:
```bash
ollama pull llama2
```

2. **System Prompt**: Optionally set a system prompt in the sidebar to guide the model's behavior.

3. **Chat Interface**: 
   - Type your message in the input box at the bottom
   - View the conversation history in the main chat area
   - Expand "View thinking process" to see the model's thought process
   - Use "Clear Chat" to start a new conversation

## Available Models

You can use any model available in the Ollama library. Some popular options include:
- llama2
- mistral
- codellama
- llava (multimodal)
- deepseek

You can find a list of all available models at [Ollama's website](https://ollama.ai/models).

To download a model, use:
```bash
ollama pull <model-name>
```

## API Reference

The app uses Ollama's API running on `http://localhost:11434`. Key endpoints used:
- `/api/tags` - List available models
- `/api/chat` - Chat with a model

For full API documentation, visit [Ollama's API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md).

## Troubleshooting

1. **No models available?**
   - Ensure Ollama is running (`ollama serve`)
   - Pull at least one model using `ollama pull`
   - Check which models are available using `ollama list`

2. **Can't connect to Ollama?**
   - Check if the Ollama service is running on port 11434
   - Verify no firewall is blocking the connection

3. **Slow responses?**
   - Check your system resources
   - Consider using a smaller or more optimized model

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 