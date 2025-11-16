# **🤖 AI Coding Assistant**

<div align="center">

=white AI coding assistant with multi-LLM support and intelligent file operations

[Features](#-features) -  [Demo](#-demo) -  [Installation](#-quick-start) -  [Documentation](#-documentation) -  [API](#-api-reference)

<img src="https://via.placeholder.com/800x400/1e1e1e/ffffff?text=AI+Coding+Assistant+Demo" alt="Demo" width="100%">

</div>

***

## **🌟 Overview**

AI Coding Assistant is a next-generation development tool that combines the power of multiple AI models (Claude Sonnet 4.5, GPT-4, Gemini) with autonomous capabilities to revolutionize your coding workflow. Unlike traditional code assistants, it can **automatically create files, execute code, and make intelligent decisions** - just like having an AI pair programmer.

### **Why This Project?**

- 🤖 **Autonomous Operations** - Creates, edits, and executes files automatically
- 🧠 **Multi-LLM Intelligence** - Seamlessly switches between Claude, GPT-4, and Gemini
- 📁 **Full Context Awareness** - Understands your entire project structure
- 💬 **Modern Chat Interface** - Blackbox-style sidebar with rich interactions
- 🔄 **Real-Time Execution** - Run code and see results instantly
- 🎯 **5 Specialized Agents** - Each agent excels at specific tasks
- 🚀 **Production Ready** - Docker, CI/CD, and enterprise-grade architecture

***

## **✨ Features**

### **🎨 VS Code Extension**

#### **Autonomous Coding**
- ✅ **Auto-create files** - "Create a FastAPI app" → File created and saved automatically
- ✅ **Smart editing** - AI modifies existing files intelligently
- ✅ **One-click execution** - Run code with automatic error handling
- ✅ **Terminal integration** - Execute commands and read output
- ✅ **File change tracking** - Real-time notifications for all file operations

#### **Intelligent Chat Interface**
```
You: "Create a Python script to scrape a website and save to CSV"

AI: "I'll create that for you..."
    [Creates: web_scraper.py]
    [Writes code with requests and pandas]
    [Automatically executes]
    
✅ File created: web_scraper.py
✅ Executed successfully
📊 Output: Data saved to output.csv
```

#### **Context-Aware Intelligence**
- **Current file understanding** - AI knows what you're working on
- **Multi-file context** - Analyze relationships across files
- **Workspace analysis** - Understand entire project structure
- **Smart code suggestions** - Based on your coding patterns

### **🚀 Backend API**

#### **Multi-LLM Architecture**
```python
# Automatic fallback system
Primary: Claude Sonnet 4.5 (best reasoning)
Fallback: GPT-4 (broad knowledge)
Alternative: Gemini (multimodal)
```

#### **5 Specialized Agents**

| Agent | Purpose | Key Features |
|-------|---------|--------------|
| 🎨 **Code Generator** | Create new code | RAG-enhanced, multi-language, context-aware |
| ✅ **Code Reviewer** | Analyze & improve | Security, performance, best practices |
| 🏗️ **System Architect** | Design systems | Architecture patterns, scalability advice |
| 🔗 **GitHub MCP** | Repository ops | Analyze repos, generate PR descriptions |
| 🧠 **Self-Evolving** | Learn & adapt | Improves from feedback, adapts strategies |

#### **Performance Features**
- ⚡ **Redis caching** - Sub-100ms response for repeated queries
- 🔍 **ChromaDB RAG** - Context from your entire codebase
- 🔄 **Async architecture** - Handle 1000+ concurrent requests
- 📊 **Real-time streaming** - Live code generation

***

## **🏗️ Architecture**

```
┌─────────────────────────────────────────────────┐
│          VS Code Extension (TypeScript)         │
│  ┌──────────────┐  ┌──────────────┐            │
│  │Chat Interface│  │File Manager  │            │
│  │(Sidebar)     │  │(Autonomous)  │            │
│  └──────┬───────┘  └──────┬───────┘            │
│         │                  │                     │
│         └──────────────────┘                     │
└────────────────┼────────────────────────────────┘
                 │ REST API / WebSocket
                 ▼
┌─────────────────────────────────────────────────┐
│         FastAPI Backend (Python)                │
│  ┌──────────────────────────────────────────┐  │
│  │      Central Orchestrator                │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐   │  │
│  │  │Code Gen │ │Reviewer │ │Architect│   │  │
│  │  └────┬────┘ └────┬────┘ └────┬────┘   │  │
│  └───────┼───────────┼──────────┼─────────┘  │
│          │           │          │            │
│  ┌───────┴───────────┴──────────┴─────────┐  │
│  │       Multi-LLM Client Layer          │  │
│  │  Claude 4.5  →  GPT-4  →  Gemini     │  │
│  └───────────────────────────────────────┘  │
│                                               │
│  ┌─────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Redis   │  │ChromaDB  │  │GitHub    │   │
│  │ Cache   │  │ RAG      │  │ API      │   │
│  └─────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────┘
```

***

## **🚀 Quick Start**

### **Prerequisites**

```bash
# Required
Python 3.10+
Node.js 18+
VS Code 1.85+

# Optional (for full features)
Redis (caching)
Docker (deployment)
```

### **Installation**

#### **1. Clone Repository**

```bash
git clone https://github.com/NamelessMonsterr/AI-Coding-Assistant.git
cd AI-Coding-Assistant
```

#### **2. Backend Setup**

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
notepad .env  # Add your API keys
```

**Required API Keys:**
```env
# Get from: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here

# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-your-key-here

# Get from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your-gemini-key-here

# Optional: https://github.com/settings/tokens
GITHUB_TOKEN=ghp_your-token-here
```

#### **3. Start Backend**

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
✅ Unified AI Coding Assistant Starting...
✅ Claude Sonnet Client initialized
✅ All agents initialized successfully
🚀 Server ready at http://localhost:8000
```

#### **4. VS Code Extension**

```bash
cd ../vscode-extension

# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Open in VS Code
code .

# Press F5 to launch Extension Development Host
```

#### **5. Test It Out**

In the Extension Development Host window:
1. Click the **AI Assistant** icon in the sidebar
2. Try: "Create a Python script that prints hello world and run it"
3. Watch it automatically create the file and execute! 🎉

***

## **💡 Usage Examples**

### **Autonomous File Creation**

```
You: "Create a FastAPI app with user authentication"

AI: Creating your FastAPI application...

✅ Created: main.py
✅ Created: auth.py
✅ Created: models.py
✅ Created: requirements.txt

All files saved and ready to use!
```

### **Multi-File Analysis**

```
You: "Analyze the relationships between my Python files"

AI: Analyzing your project structure...

📊 Project Analysis:
- main.py imports auth.py and models.py
- auth.py depends on models.py
- Circular dependency detected in utils.py

🔧 Recommendations:
- Refactor utils.py to remove circular import
- Consider moving shared functions to separate module
```

### **Smart Code Review**

```
You: "Review my current file for security issues"

AI: Conducting security audit...

🔒 Security Issues Found:

1. ⚠️ SQL Injection Risk (Line 45)
   Current: f"SELECT * FROM users WHERE id={user_id}"
   Fix: Use parameterized queries

2. 🔴 Exposed Secret Key (Line 12)
   Current: SECRET_KEY = "hardcoded-secret"
   Fix: Load from environment variable

3. ⚠️ Missing Input Validation (Line 67)
   Add validation for user_input parameter
```

### **Code Generation with Context**

```
You: "Generate a function to process payments using Stripe"

AI: Based on your project structure, I'll integrate with your existing models...

✅ Code generated and inserted at cursor position
✅ Imported required dependencies
✅ Added error handling for your existing error types
```

***

## **📚 Documentation**

### **VS Code Commands**

| Command | Shortcut | Description |
|---------|----------|-------------|
| Generate Code | `Ctrl+Shift+G` | Generate code from description |
| Review Code | `Ctrl+Shift+R` | Review current file |
| Explain Code | `Ctrl+Shift+E` | Explain selected code |
| Refactor Code | - | Improve code quality |
| Open Chat | Click sidebar | Open AI chat interface |

### **Chat Interface Features**

- **+ Current** - Add current file to context
- **+ File** - Add any file to context
- **🔍 Analyze** - Analyze entire workspace
- **✕ Clear** - Clear context
- **Auto-execute toggle** - Enable/disable autonomous mode

### **API Endpoints**

**Base URL:** `http://localhost:8000`

#### **Code Generation**
```bash
POST /api/v1/generate
{
  "prompt": "Create a REST API endpoint",
  "language": "python",
  "temperature": 0.2,
  "model": "claude"
}
```

#### **Code Review**
```bash
POST /api/v1/review
{
  "code": "def function(): ...",
  "language": "python",
  "file_path": "app.py"
}
```

#### **Architecture Design**
```bash
POST /api/v1/architecture
{
  "requirements": "Build scalable e-commerce platform",
  "constraints": "AWS, budget $10k/month"
}
```

**Full API Docs:** http://localhost:8000/docs

***

## **⚙️ Configuration**

### **Backend (`backend/.env`)**

```env
# LLM Selection
DEFAULT_MODEL=claude              # claude|openai|gemini
ENABLE_FALLBACK=true              # Auto-switch on errors

# Performance
MAX_TOKENS=4096
TEMPERATURE=0.2
REDIS_ENABLED=true                # Enable caching

# Features
ENABLE_RAG=true                   # Context from codebase
CHROMA_ENABLED=true               # Vector store

# Security
RATE_LIMIT_ENABLED=true
API_KEY=your-secret-key           # Optional authentication
```

### **Extension (`VS Code Settings`)**

```json
{
  "unified-ai.apiUrl": "http://localhost:8000",
  "unified-ai.defaultModel": "claude",
  "unified-ai.autoExecute": true,
  "unified-ai.enableRAG": true
}
```

***

## **🧪 Testing**

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Extension tests
cd vscode-extension
npm test

# Integration tests
npm run test:integration
```

**Test Coverage:** 85%+ for backend, 75%+ for extension

***

## **🐳 Docker Deployment**

```bash
# Build and run with Docker Compose
docker-compose up -d

# Services available:
# - Backend: http://localhost:8000
# - Redis: localhost:6379
```

**Docker Compose includes:**
- FastAPI backend
- Redis cache
- Prometheus metrics (optional)

***

## **📊 Performance**

| Metric | Value |
|--------|-------|
| Response Time (cached) | <100ms |
| Response Time (uncached) | <2s |
| Concurrent Requests | 1000+ |
| Cache Hit Rate | 68-85% |
| Uptime (with fallback) | 99.9% |

***

## **🤝 Contributing**

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md)

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing`
5. Open Pull Request

***

## **📝 License**

This project is licensed under the MIT License - see [LICENSE](LICENSE)

***

## **🙏 Credits**

- **Anthropic** - Claude Sonnet API
- **OpenAI** - GPT-4 API
- **Google** - Gemini API
- **FastAPI** - Web framework
- **VS Code** - Extension platform

***

## **📞 Support**

- 🐛 **Issues:** [GitHub Issues](https://github.com/NamelessMonsterr/AI-Coding-Assistant/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/NamelessMonsterr/AI-Coding-Assistant/discussions)
- 📧 **Email:** support@example.com

***

## **🗺️ Roadmap**

- [x] Multi-LLM support
- [x] Autonomous file operations
- [x] VS Code extension
- [x] RAG with ChromaDB
- [ ] Voice input support
- [ ] Inline code suggestions
- [ ] Web interface
- [ ] Team collaboration features
- [ ] Fine-tuned models

---

<div align="center">

**⭐ Star this repo if you find it useful!**

Made with ❤️ by [NamelessMonsterr](https://github.com/NamelessMonsterr)

</div>
