# 🤖 Unified AI Coding Assistant

A powerful VS Code extension that brings advanced AI capabilities to your editor, powered by **Claude Sonnet 4.5**, **OpenAI GPT-4**, and **Google Gemini**.

<div align="center">

[![VS Code](https://img.shields.io/badge/VS%20Code-v1.85+-blue.svg?style=flat-square&logo=visual-studio-code)](https://code.visualstudio.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red.svg?style=flat-square)](https://github.com)

</div>

---

## ✨ Key Features

### 🎯 **AI-Powered Code Operations**
- **Code Generation** - Create functions, components, and entire modules from natural language
- **Code Review** - Automated analysis with security, performance, and best practice checks
- **Code Explanation** - Understand complex code instantly with AI-powered insights
- **Code Refactoring** - Improve code quality with smart suggestions
- **Architecture Design** - Get professional architecture recommendations

### 🧠 **Multi-LLM Intelligence**
- **Claude Sonnet 4.5** - Primary model for advanced reasoning
- **OpenAI GPT-4** - Powerful code completion and generation
- **Google Gemini** - Multimodal analysis capabilities
- **Smart Model Selection** - Automatic fallback for reliability

### ⚡ **Performance & Efficiency**
- **Real-time Streaming** - See responses as they're generated
- **Intelligent Caching** - Reuse results for faster responses
- **Context Awareness** - Analyzes your entire project structure
- **Background Repository Analysis** - Index your codebase for better context

---

## 🚀 Quick Start

### Prerequisites
- **VS Code** 1.85 or higher
- **Backend Service** running on `http://localhost:8000`

### Installation

1. **Install the Extension**
   - Open VS Code and navigate to Extensions
   - Search for "Unified AI Coding Assistant"
   - Click Install

2. **Configure Settings**
   - Open VS Code Settings (`Ctrl+,` or `Cmd+,`)
   - Search for "Unified AI"
   - Set your Backend URL: `http://localhost:8000`
   - (Optional) Set API Key for authentication

3. **Select Your AI Model**
   - Press `Ctrl+Shift+M` (or `Cmd+Shift+M` on Mac)
   - Choose your preferred model (Claude, OpenAI, or Gemini)

---

## ⌨️ Commands & Shortcuts

| Command | Shortcut | Action |
|---------|----------|--------|
| **Generate Code** | `Ctrl+Shift+G` | AI generates code from description |
| **Review Code** | `Ctrl+Shift+R` | Comprehensive code quality review |
| **Explain Code** | `Ctrl+Shift+E` | Detailed explanation of selected code |
| **Refactor Code** | Right-click Menu | Smart code improvements |
| **Show Opened Files** | `Ctrl+Shift+O` | List all open files for context |
| **Open Chat** | Sidebar Icon | Launch AI Chat interface |
| **Select Model** | Command Palette | Switch AI models dynamically |

**Mac Users:** Replace `Ctrl` with `Cmd`

---

## 💡 Usage Examples

### Generate Code
1. Select an empty file or position your cursor
2. Press `Ctrl+Shift+G`
3. Describe what you need:
   ```
   Create a function to validate email addresses
   ```
4. Watch as the AI generates the code

### Review Code
1. Select the code you want reviewed
2. Press `Ctrl+Shift+R`
3. Get detailed feedback on:
   - Security issues
   - Performance bottlenecks
   - Best practices
   - Bug potential

### Explain Code
1. Highlight any code section
2. Press `Ctrl+Shift+E`
3. Receive a clear, detailed explanation

---

## ⚙️ Configuration

Open VS Code Settings and search for `unified-ai`:

```json
{
  "unified-ai.apiUrl": "http://localhost:8000",
  "unified-ai.apiKey": "",
  "unified-ai.defaultModel": "claude",
  "unified-ai.temperature": 0.2,
  "unified-ai.maxTokens": 4096,
  "unified-ai.enableStreaming": true,
  "unified-ai.enableCache": true
}
```

| Setting | Default | Description |
|---------|---------|-------------|
| **apiUrl** | `http://localhost:8000` | Backend service URL |
| **apiKey** | *(empty)* | Optional authentication key |
| **defaultModel** | `claude` | Primary AI model (claude, openai, gemini, auto) |
| **temperature** | `0.2` | Lower = more focused, Higher = more creative |
| **maxTokens** | `4096` | Maximum response length |
| **enableStreaming** | `true` | Real-time response streaming |
| **enableCache** | `true` | Cache responses for speed |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│     VS Code Extension (Frontend)         │
│  ┌───────────────────────────────────┐  │
│  │    WebView Chat Interface         │  │
│  │    Command Palette Integration    │  │
│  │    Context Menu Options           │  │
│  └───────────────────────────────────┘  │
│              │                           │
│   HTTP API   │ Streaming                │
│              ▼                           │
├─────────────────────────────────────────┤
│     Backend Service (FastAPI)            │
│  ┌───────────────────────────────────┐  │
│  │    5 Specialized AI Agents        │  │
│  │    • Code Generation              │  │
│  │    • Code Review & Analysis       │  │
│  │    • Architecture Design          │  │
│  │    • GitHub Integration           │  │
│  │    • Self-Evolution               │  │
│  └───────────────────────────────────┘  │
│              │                           │
│              ▼                           │
│  ┌───────────────────────────────────┐  │
│  │   Multi-LLM Layer                 │  │
│  │   Claude | OpenAI | Gemini        │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

---

## 🐛 Troubleshooting

### Extension Not Connecting
- ✅ Verify backend is running: `curl http://localhost:8000/health`
- ✅ Check API URL in settings
- ✅ Ensure no firewall blocking port 8000

### Model Not Responding
- ✅ Check API keys in backend `.env` file
- ✅ Try switching models in settings
- ✅ Check backend logs for errors

### Slow Response Times
- ✅ Enable caching: `"unified-ai.enableCache": true`
- ✅ Reduce `maxTokens` if not needed
- ✅ Lower temperature for faster responses

---

## 📚 Resources

- **[Backend Setup Guide](../backend/README.md)** - Install and configure the backend service
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs
- **[VS Code Extension Guide](https://code.visualstudio.com/api)** - VS Code extension development

---

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Support

- 📧 **Issues?** Open an issue on GitHub
- 💬 **Questions?** Start a discussion
- ⭐ **Like it?** Please star the repository!

---

<div align="center">

**Built with ❤️ using VS Code API, FastAPI, Claude Sonnet 4.5, OpenAI GPT-4, and Google Gemini**

*Empowering developers with AI at their fingertips*

</div>
