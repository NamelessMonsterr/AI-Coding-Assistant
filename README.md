# Unified AI Coding Assistant

Multi-agent AI coding assistant powered by Claude Sonnet 4.5, OpenAI GPT-4, Google Gemini, and Hugging Face models.

## 🚀 Features

### **Multi-LLM Support**
- **Anthropic Claude Sonnet 4.5** (Primary) - Advanced code generation and reasoning
- **OpenAI GPT-4/Codex** (Secondary) - Code completion and generation
- **Google Gemini 2.0** (Multimodal) - Complex architecture and multimodal tasks
- **Hugging Face** (Local) - Open-source models for offline use

### **5 Specialized AI Agents**
1. **Code Generator Agent** - Generate code from natural language
2. **Code Reviewer Agent** - Automated code review, bug detection, security analysis
3. **System Architect Agent** - Architecture design and pattern suggestions
4. **GitHub MCP Agent** - Real GitHub API integration for repo analysis
5. **Self-Evolving Agent** - Learns from feedback and improves over time

### **Performance Features**
- **Redis Caching** - Cache LLM responses for faster performance
- **Vector Store (ChromaDB)** - RAG capabilities for context-aware responses
- **GitHub API Integration** - Real repository analysis and code search
- **Rate Limiting** - API protection and abuse prevention
- **Authentication** - Secure API access

## 📦 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+ (for VS Code extension)
- Docker & Docker Compose (optional)
- Redis (optional, for caching)

### Backend Setup

Navigate to backend
cd backend

Create virtual environment
python -m venv venv

Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

Activate (Linux/Mac)
source venv/bin/activate

Install dependencies
pip install -r requirements.txt

Configure environment
cp .env.example .env

Edit .env with your API keys
Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

text

### Access API Documentation
Open `http://localhost:8000/docs` in your browser for interactive API documentation.

## 🔧 Configuration

Create `.env` file in `backend/` directory:

Required: At least one LLM API key
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
Optional: GitHub integration
GITHUB_TOKEN=ghp_...

Redis (optional but recommended)
REDIS_HOST=localhost
REDIS_POR

Settings
DEFAULT_MODEL=claude
ENABLE_FALLBACK=true
text

## 📚 Documentation

- [Backend Setup Guide](backend/README.md)
- [API Reference](docs/api-reference.md)
- [Architecture Overview](docs/architecture.md)
- [Development Guide](docs/development-guide.md)

## 🎯 API Examples

### Generate Code
curl -X POST "http://localhost:8000/api/v1/generate"
-H "Content-Type: application/json"
-d '{
"prompt": "Create a FastAPI endpoint for user authenticati
n", "language": "
ython", "mode
text

### Review Code
curl -X POST "http://localhost:8000/api/v1/review"
-H "Content-Type: application/json"
-d '{
"code": "def divide(a, b): return a /
b", "language":
text

### Analyze GitHub Repository
curl -X POST "http://localhost:8000/api/v1/github/analyze"
-H "Content-Type: application/json"
-d '{
"rehttps://github.com/user/repo",
"analysis_type": "struct
text

## 🧪 Testing

Run all tests
pytest tests/ -v

Run with coverage
pytest tests/ -v --cov=app --cov-report=html

Run specific test
pytest tests/test_api.py -v

Type checking
mypy app/

Code formatting
black app/

Linting
flake8 app/

text

## 🐳 Docker Deployment

Using Docker Compose (recommended)
cd backend
docker-co

Or build manually
docker build -t unified-ai-backend .
docker run -p 8000:80

text

## 📊 Project Structure

unified-ai-coding-assistant/
├── backend/ # FastAPI backend
│ ├── app/
│ │ ├── agents/ # AI agents
│ │ ├── models/ # LLM clients
│ │ ├── api/ # API routes
│ │ ├── memory/ # Caching & vector store
│ │ ├── middleware/ # Security & middleware
│ │ └── utils/ # Utilities
│ ├── tests/ # Test suite
│ └── requirements.txt
├── vscode-extension/ # VS Code extension
│ ├── src/
│ └── package.json
├── docs/ # Documentation
text

## 🛡️ Security

- API rate limiting enabled by default
- CORS configured for specific origins
- Input validation on all endpoints
- Secure API key handling
- Security headers applied to all responses

## 🚀 Performance

- Redis caching for repeated queries (optional)
- Vector store for RAG capabilities
- Automatic LLM fallback for high availability
- Streaming support for real-time generation
- Async/await for non-blocking operations

## 📈 Monitoring

Health check
curl http://localhost:8000/health

Available models
curl http://localhost:8000/api/v1/models

Cache statistics (if Redis enabled)
curl http://localhost:8000/api/v1/cache/stats

text

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Anthropic Claude for advanced AI capabilities
- OpenAI for GPT models
- Google for Gemini
- FastAPI for the excellent web framework

## 📧 Support

- Documentation: [docs/](docs/)
- Issues: [GitHub Issues](https://github.com/yourusername/unified-ai-coding-assistant/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/unified-ai-coding-assistant/discussions)

---

**Built with ❤️ using Claude Sonnet 4.5, OpenAI GPT-4, Google Gemini, and FastAPI**