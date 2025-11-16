# Development Guide

## Setting Up Development Environment

### Prerequisites
- Python 3.10 or higher
- Node.js 18+ (for frontend/extension development)
- Git
- Docker (optional)
- Redis (optional, for caching)

### Initial Setup

1. **Clone the repository:**
git clone https://github.com/yourusername/unified-ai-coding-assistant.git
cd unified-ai-coding-assistant

text

2. **Backend setup:**
cd backend
python -m venv venv

Windows
.\venv\Scripts\Activate.ps1

Linux/Mac
source venv/bin/activate

pip install -r requirements.txt

text

3. **Configure environment:**
cp .env.example .env

Edit .env with your API keys
text

4. **Run the server:**
uvicorn app.main:app --reload

text

## Development Workflow

### Code Quality

**Format code:**
black app/

text

**Lint code:**
flake8 app/

text

**Type checking:**
mypy app/

text

**Sort imports:**
isort app/

text

**Run all quality checks:**
black app/ && flake8 app/ && mypy app/ && isort app/

text

### Testing

**Run all tests:**
pytest tests/ -v

text

**Run with coverage:**
pytest tests/ -v --cov=app --cov-report=html

text

**Run specific test:**
pytest tests/test_api.py::TestCodeGeneration::test_generate_code_valid_request -v

text

**Run tests in parallel:**
pytest tests/ -n auto

text

### Pre-commit Hooks

Install pre-commit hooks:
pre-commit install

text

Run hooks manually:
pre-commit run --all-files

text

## Project Structure

backend/
├── app/
│ ├── agents/ # AI agents
│ ├── models/ # LLM clients
│ ├── api/ # API routes & schemas
│ ├── memory/ # Caching & vector store
│ ├── middleware/ # Security & middleware
│ ├── utils/ # Utilities
│ ├── config.py # Configuration
│ ├── orchestrator.py # Central router
│ └── main.py # FastAPI app
├── tests/ # Test suite
├── docs/ # Documentation
└── requirements.txt # Dependencies

text

## Adding New Features

### Adding a New Agent

1. Create agent file in `app/agents/`:
from app.models.llm_interface import LLMInterface
from typing import Dict, Any
import logging

logger = logging.getLogger(name)

class NewAgent:
def init(self, llm: LLMInterface):
self.llm = llm
logger.info("NewAgent initialized")

text
async def process(self, input: str) -> Dict[str, Any]:
    # Implementation
    pass
text

2. Add to orchestrator in `app/orchestrator.py`:
from app.agents.new_agent import NewAgent

In init
self.new_agent = NewAgent(self.primary_llm)

In route_request
elif task_type == "new-task":
return await self.new_agent.process(**kwargs)

text

3. Add API endpoint in `app/api/routes.py`
4. Add tests in `tests/test_agents.py`

### Adding a New LLM Provider

1. Create client in `app/models/`:
from app.models.llm_interface import LLMInterface

class NewLLMClient(LLMInterface):
def init(self, api_key: str, model: str):
super().init(api_key, model)
# Initialize client

text
async def generate(self, system: str, user: str, **kwargs):
    # Implementation
    pass

async def stream_generate(self, system: str, user: str, **kwargs):
    # Implementation
    pass
text

2. Add to orchestrator initialization
3. Add tests

### Adding API Endpoints

1. Create schema in `app/api/schemas.py`:
class NewRequest(BaseModel):
field: str = Field(..., description="Description")

text

2. Add route in `app/api/routes.py`:
@router.post("/new-endpoint")
@limiter.limit("10/minute")
async def new_endpoint(request: NewRequest):
# Implementation
pass

text

3. Add tests in `tests/test_api.py`

## Debugging

### Enable Debug Logging
In app/main.py
logging.basicConfig(level=logging.DEBUG)

text

### Use FastAPI's Interactive Docs
Visit `http://localhost:8000/docs` for testing endpoints

### Debug with VS Code

`.vscode/launch.json`:
{
"version": "0.2.0",
"configurations": [
{
"name": "FastAPI",
"type": "python",
"request": "launch",
"module": "uvicorn",
"args": [
"app.main:app",
"--reload"
],
"jinja": true
}
]
}

text

## Common Issues

### Import Errors
Add project root to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

text

### Redis Connection Failed
- Check Redis is running
- Verify connection settings in .env
- System continues without caching

### LLM API Errors
- Verify API keys in .env
- Check rate limits
- Enable fallback in config

## Performance Optimization

### Enable Caching
- Install and run Redis
- Configure in .env
- Monitor cache hit rates

### Optimize LLM Calls
- Use appropriate temperature
- Limit max_tokens
- Enable response caching

### Database Optimization
- Use connection pooling
- Enable query caching
- Monitor slow queries

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Run tests and quality checks
5. Submit pull request

### Code Style
- Follow PEP 8
- Use type hints
- Write docstrings
- Add unit tests

### Commit Messages
feat: Add new feature
fix: Fix bug
docs: Update documentation
test: Add tests
refactor: Refactor code

text

## Release Process

1. Update version in `app/main.py`
2. Update CHANGELOG.md
3. Run full test suite
4. Tag release
5. Deploy to production

## Support

- Documentation: `docs/`
- Issues: GitHub Issues
- Discussions: GitHub Discussions