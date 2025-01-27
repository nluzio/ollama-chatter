# 🚀 Ollama Chat UI

A simple web interface to chat with AI models running on your own computer (no cloud needed!). Perfect for beginners exploring local AI.

## 🌟 Quick Start

> **Note**
> When running models locally with Ollama, your available RAM is key to performance! Before pulling a model, we recommend:
> - Checking your available system memory (`top` on Mac/Linux, Task Manager on Windows)
> - Comparing it with your chosen model's size (smaller models like deepseek-r1:1.5b need less RAM)
> - Starting with smaller models like tinyllama or deepseek-r1:1.5b if you're unsure
> 
> This quick check helps ensure smooth operation! You can always upgrade to larger models as needed. 🚀


1. Install Ollama from [ollama.com/download](https://ollama.com/download)
2. Open a terminal and run:
   ```bash
   git clone https://github.com/nluzio/ollama-chatter.git
   cd ollama-chatter
   pip install -r requirements.txt
   ```
3. Start the services (in separate terminal windows):
   ```bash
   # Terminal 1: Pull a model & Start Ollama
   ollama pull deepseek-r1:1.5b
   ollama serve
   ```
   ```bash
   # Terminal 2: Start Phoenix tracing UI
   phoenix serve
   ```
   ```bash
   # Terminal 3: Start the chat app
   streamlit run main.py
   ```
4. Open your browser to:
   - Chat UI: `http://localhost:8501`
   - Phoenix UI: `http://localhost:6006`

## 🧰 Prerequisites

1. **Python 3.7 or newer**
   - Check your version: `python --version`
   - If needed, download from [python.org](https://www.python.org/downloads/)

2. **Ollama**
   - Download from [ollama.com/download](https://ollama.com/download)
   - Linux users can install with:
     ```bash
     curl -fsSL https://ollama.com/install.sh | sh
     ```

## 📖 Features

- Chat with AI models running on your computer
- Choose from multiple AI models
- Customize AI behavior with system prompts
- View the AI's thinking process
- Save chat history
- Clear conversations anytime
- Monitor and analyze chat interactions with Phoenix tracing

## 🔍 Tracing with [Phoenix](https://phoenix.arize.com/) <img src="https://github.com/user-attachments/assets/cc795f64-ba2e-484f-af4e-2d273146eb5d" width="40">


This app includes OpenTelemetry tracing integration with [Arize Phoenix](https://docs.arize.com/phoenix), allowing you to:

1. **Monitor Chat Interactions**
   - View detailed traces of each LLM Interaction
   - Track model performance and response times
   - Analyze input/output patterns

2. **Access the Tracing UI**
   - Open `http://localhost:6006` in your browser
   - View traces under the "Traces" tab
   - Filter and search through chat history
   - - Analyze full conversations with "Sessions" tab

3. **What's Being Traced**
   - Model information (name, provider)
   - Input messages and system prompts
   - Output responses
   - Token counts
   - Error states (if any)

4. **Troubleshooting Traces**
   - Ensure Phoenix is running (`phoenix serve`)
   - Check port 6006 is available
   - Verify traces appear in Phoenix UI after chat interactions

## 💭 Using the App

1. **Choose a Model**
   - Select a model from the sidebar dropdown

   - If no models appear, run: `ollama pull deepseek-r1:1.5b`

2. **Start Chatting**
   - Type messages in the bottom text box
   - Press Enter or click the send button
   - The AI's response will appear above

3. **Customize Behavior**
   - Use the "System Prompt" in the sidebar
   - Example: "You are a helpful coding assistant. Explain concepts simply."

4. **View Thinking Process (Only supported by some models)**
   - Click "View thinking process" above responses
   - See how the AI forms its answers

## 🤖 Recommended Models

Start with these beginner-friendly models:

| Model     | Best For                    | Size    | Command               |
|-----------|----------------------------|---------|----------------------|
| llama3    | General chat & assistance  | Large  | `ollama pull llama3` |
| mistral   | Clear, helpful responses   | Medium  | `ollama pull mistral`|
| deepseek-r1:1.5b | Small Version of Advanced Reasoning Model | Small   | `ollama pull deepseek-r1:1.5b` |
| tinyllama | Faster, lighter responses  | Tiny   | `ollama pull tinyllama` |

### 📚 Finding More Models

You can explore the full list of available models at [ollama.com/library](https://ollama.com/library). Some notable options:

- **DeepSeek Models**: 
  - Excellent for reasoning tasks
  - Available in various sizes (1.5B to 671B)
  - Install with: `ollama pull deepseek-r1`

- **Specialized Models**:
  - Code generation: `codellama`, `deepseek-coder`
  - Math & reasoning: `wizard-math`
  - Vision tasks: `llava`

To manage your models:
```bash
# List installed models
ollama list

# Remove a model
ollama rm model-name

# Update a model
ollama pull model-name
```

## ❓ Troubleshooting

1. **No Models Available?**
   - Ensure Ollama is running: `ollama serve`
   - Download a model: `ollama pull llama3`
   - Check installed models: `ollama list`

2. **Slow Responses?**
   - Try a smaller model like `tinyllama`
   - Close other resource-heavy applications
   - Check your computer's available memory

3. **Connection Issues?**
   - Verify Ollama is running: `ollama serve`
   - Check if port 11434 is available
   - Restart Ollama if needed

## 🔧 API Details

The app connects to Ollama's API at `http://localhost:11434`. For advanced users, full API documentation is available at [Ollama's API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md).

## 🤝 Contributing

Found a bug or want to help? Feel free to:
1. Open an issue
2. Submit a pull request
3. Share your feedback

## 💡 Need Help?

Create a [GitHub issue](https://github.com/nluzio/ollama-chatter/issues) with:
- What you were trying to do
- What happened instead
- Any error messages
- Screenshots (if helpful) 
