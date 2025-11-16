# API Reference

Complete API documentation for the Unified AI Coding Assistant.

## Base URL

http://localhost:8000

text

## Authentication

Optional API key authentication via Bearer token:

Authorization: Bearer YOUR_API_KEY

text

## Rate Limits

- Code Generation: 20 requests/minute
- Code Review: 15 requests/minute
- GitHub Analysis: 5 requests/minute
- Other endpoints: 10-30 requests/minute

## Endpoints

### Code Generation

#### POST /api/v1/generate

Generate code from natural language description.

**Request Body:**
{
"prompt": "Create a FastAPI endpoint for user authentication",
"language": "python",
"context": "Optional project context",
"temperature": 0.2,
"max_tokens": 4096,
"model": "claude"
}

text

**Response:**
{
"success": true,
"data": {
"code": "Generated code here...",
"language": "python",
"model_used": "claude-sonnet-4-20250514",
"tokens_used": 1234
},
"message": "Code generated successfully",
"model_used": "claude-sonnet-4-20250514"
}

text

#### POST /api/v1/generate/stream

Stream code generation for real-time feedback.

**Request Body:** Same as `/generate`

**Response:** Server-Sent Events stream

### Code Review

#### POST /api/v1/review

Perform comprehensive code review.

**Request Body:**
{
"code": "def divide(a, b): return a / b",
"language": "python",
"file_path": "optional/path.py",
"temperature": 0.3,
"model": "claude"
}

text

**Response:**
{
"success": true,
"data": {
"review": "Detailed review...",
"language": "python",
"file_path": "optional/path.py",
"model_used": "claude-sonnet-4-20250514",
"tokens_used": 567
},
"message": "Code review completed"
}

text

#### POST /api/v1/review/quick-check

Quick focused check (security/performance/style).

**Request Body:**
{
"code": "Code to check...",
"language": "python",
"check_type": "security"
}

text

### Architecture Design

#### POST /api/v1/architecture

Generate architectural design and recommendations.

**Request Body:**
{
"requirements": "Build a scalable e-commerce platform...",
"current_architecture": "Optional existing architecture",
"constraints": "Optional constraints",
"temperature": 0.4,
"model": "claude"
}

text

#### POST /api/v1/architecture/patterns

Suggest design patterns for a specific problem.

**Request Body:**
{
"problem_description": "Need to implement caching strategy...",
"language": "python",
"temperature": 0.3
}

text

#### POST /api/v1/architecture/optimize

Optimize existing architecture.

**Request Body:**
{
"current_design": "Current architecture description...",
"bottlenecks": "Optional known issues",
"temperature": 0.3
}

text

### GitHub Integration

#### POST /api/v1/github/analyze

Analyze a GitHub repository.

**Request Body:**
{
"repo_url": "https://github.com/user/repo",
"analysis_type": "structure",
"temperature": 0.3
}

text

#### POST /api/v1/github/pr-description

Generate pull request description.

**Request Body:**
{
"changes": "Added authentication feature...",
"context": "Optional additional context",
"temperature": 0.3
}

text

#### POST /api/v1/github/code-search

Assist with code search.

**Request Body:**
{
"search_query": "authentication middleware",
"repo_context": "Optional repo URL",
"temperature": 0.3
}

text

### Self-Evolving

#### POST /api/v1/learn/feedback

Process user feedback for improvement.

**Request Body:**
{
"previous_interaction": {"task": "details..."},
"feedback": "User feedback text",
"outcome": "success",
"temperature": 0.4
}

text

#### POST /api/v1/learn/adapt

Adapt strategy based on performance.

**Request Body:**
{
"task_type": "code-generation",
"context": "Optional context",
"temperature": 0.3
}

text

### Utility

#### GET /api/v1/models

Get available LLM models.

**Response:**
{
"available_models": ["claude", "openai", "gemini"],
"primary_model": "claude-sonnet-4-20250514",
"count": 3
}

text

#### GET /api/v1/cache/stats

Get cache statistics.

**Response:**
{
"cache_stats": {
"enabled": true,
"keyspace_hits": 1234,
"keyspace_misses": 567,
"hit_rate": 68.5
}
}

text

#### GET /health

Health check endpoint.

**Response:**
{
"status": "healthy",
"service": "unified-ai-coding-assistant",
"version": "1.0.0",
"available_models": ["claude", "openai"],
"services": {
"api": "operational",
"redis_cache": "operational",
"vector_store": "disabled"
}
}

text

## Error Responses

All endpoints return error responses in this format:

{
"detail": "Error message here"
}

text

Common HTTP status codes:
- 200: Success
- 400: Bad Request (validation error)
- 401: Unauthorized (invalid API key)
- 429: Too Many Requests (rate limit exceeded)
- 500: Internal Server Error

## Examples

### cURL Examples

**Generate Code:**
curl -X POST "http://localhost:8000/api/v1/generate"
-H "Content-Type: application/json"
-H "Authorization: Bearer YOUR_API_KEY"
-d '{
"prompt": "Create a REST API endpoint",
"language": "python"
}'

text

**Review Code:**
curl -X POST "http://localhost:8000/api/v1/review"
-H "Content-Type: application/json"
-d '{
"code": "def hello(): return "world"",
"language": "python"
}'

text

### Python Examples

import requests

Generate code
response = requests.post(
"http://localhost:8000/api/v1/generate",
json={
"prompt": "Create a FastAPI endpoint",
"language": "python"
},
headers={"Authorization": "Bearer YOUR_API_KEY"}
)
result = response.json()
print(result["data"]["code"])

text

### JavaScript Examples

// Generate code
const response = await fetch('http://localhost:8000/api/v1/generate', {
method: 'POST',
headers: {
'Content-Type': 'application/json',
'Authorization': 'Bearer YOUR_API_KEY'
},
body: JSON.stringify({
prompt: 'Create a React component',
language: 'javascript'
})
});
const result = await response.json();
console.log(result.data.code);

text
undefined
docs/architecture.md

text
# Architecture Overview

## System Architecture

┌────────────────────────────────────────────────┐
│ Unified AI Coding Assistant │
│ │
│ ┌──────────────────────────────────────────┐ │
│ │ FastAPI Backend │ │
│ │ │ │
│ │ ┌────────────────────────────────────┐ │ │
│ │ │ Central Orchestrator │ │ │
│ │ │ (Intelligent Routing & Fallback) │ │ │
│ │ └────────────────────────────────────┘ │ │
│ │ │ │
│ │ ┌──────────┐ ┌──────────┐ ┌─────────┐ │ │
│ │ │ Code Gen │ │ Review │ │ Arch │ │ │
│ │ │ Agent │ │ Agent │ │ Agent │ │ │
│ │ └──────────┘ └──────────┘ └─────────┘ │ │
│ │ ┌──────────┐ ┌──────────┐ │ │
│ │ │ GitHub │ │ Self │ │ │
│ │ │ MCP │ │ Evolving │ │ │
│ │ └──────────┘ └──────────┘ │ │
│ │ │ │
│ │ ┌────────────────────────────────────┐ │ │
│ │ │ Multi-LLM Layer │ │ │
│ │ │ Claude | OpenAI | Gemini | HF │ │ │
│ │ └────────────────────────────────────┘ │ │
│ │ │ │
│ │ ┌─────────┐ ┌──────────┐ ┌─────────┐ │ │
│ │ │ Redis │ │ Chroma │ │ GitHub │ │ │
│ │ │ Cache │ │ Vector │ │ API │ │ │
│ │ └─────────┘ └──────────┘ └─────────┘ │ │
│ └──────────────────────────────────────────┘ │
└────────────────────────────────────────────────┘

text

## Components

### 1. API Layer (FastAPI)
- RESTful API endpoints
- Request validation with Pydantic
- Rate limiting and authentication
- Security middleware
- CORS configuration
- Streaming support

### 2. Central Orchestrator
- Routes requests to appropriate agents
- Multi-LLM management
- Automatic fallback mechanism
- Load balancing
- Error handling

### 3. AI Agents

#### Code Generator Agent
- Generates code from natural language
- Supports multiple programming languages
- Context-aware generation
- Template-based prompts

#### Code Reviewer Agent
- Comprehensive code review
- Security analysis
- Performance optimization
- Style checking
- Bug detection

#### System Architect Agent
- Architecture design
- Design pattern suggestions
- System optimization
- Technology recommendations

#### GitHub MCP Agent
- Repository analysis
- PR description generation
- Code search assistance
- Real GitHub API integration

#### Self-Evolving Agent
- Learns from feedback
- Strategy adaptation
- Performance tracking
- Continuous improvement

### 4. LLM Layer

#### Claude Sonnet 4.5 (Primary)
- Advanced reasoning
- Long context windows
- Safety and alignment
- Code generation expertise

#### OpenAI GPT-4 (Fallback)
- Strong code understanding
- Multi-modal capabilities
- Broad knowledge base

#### Google Gemini (Multimodal)
- Multimodal processing
- Fast inference
- Good for complex tasks

#### Hugging Face (Local)
- Open-source models
- Offline capability
- Custom fine-tuning

### 5. Storage & Caching

#### Redis Cache
- Response caching
- Session management
- Rate limiting data
- TTL-based expiration

#### ChromaDB Vector Store
- Code embeddings
- Semantic search
- RAG capabilities
- Context retrieval

### 6. External Integrations

#### GitHub API
- Repository analysis
- Code search
- PR management
- Issue tracking

## Data Flow

### 1. Code Generation Flow
User Request → API Validation → Orchestrator →
Check Cache → Agent Selection → LLM Call →
Response Processing → Cache Storage → User

text

### 2. Code Review Flow
Code Submission → Validation → Orchestrator →
Review Agent → Multi-aspect Analysis →
Security Check → Performance Check →
Best Practices → Consolidated Report → User

text

### 3. Architecture Design Flow
Requirements → Validation → Architect Agent →
LLM Analysis → Pattern Selection →
Component Design → Technology Stack →
Diagram Generation → Recommendations → User

text

## Security Architecture

### Authentication
- Optional API key authentication
- Bearer token support
- Configurable per endpoint

### Rate Limiting
- Per-IP rate limiting
- Per-API-key rate limiting
- Configurable limits per endpoint

### Input Validation
- Pydantic schemas
- Length restrictions
- Type checking
- Sanitization

### Security Headers
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection
- Strict-Transport-Security
- Content-Security-Policy

## Scalability

### Horizontal Scaling
- Stateless API design
- Redis for shared state
- Load balancer compatible
- Container-ready

### Vertical Scaling
- Async/await architecture
- Non-blocking I/O
- Connection pooling
- Resource optimization

### Caching Strategy
- Response caching
- Query result caching
- Vector embedding caching
- TTL-based invalidation

## Monitoring & Observability

### Logging
- Structured logging
- Request/response logging
- Error tracking
- Performance metrics

### Health Checks
- API health endpoint
- Service status checks
- Dependency monitoring
- Cache statistics

### Metrics
- Request latency
- Error rates
- Cache hit rates
- Token usage

## Deployment Options

### Docker
- Single container deployment
- Docker Compose for multi-service
- Environment-based configuration

### Kubernetes
- Helm charts
- Auto-scaling
- Rolling updates
- Health checks

### Cloud Platforms
- AWS (ECS, Lambda)
- Google Cloud (Cloud Run)
- Azure (Container Instances)
- Heroku

## Future Enhancements

1. WebSocket support for real-time collaboration
2. User authentication and multi-tenancy
3. Fine-tuned models for specific domains
4. Advanced caching with CDN
5. GraphQL API option
6. VS Code extension integration
7. Plugin system for extensibility
8. Advanced analytics and insights