"""
Main FastAPI application for Unified AI Coding Assistant
Multi-agent AI coding assistant powered by Claude Sonnet 4.5, OpenAI, and Gemini
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.routes import router
from app.config import settings
from app.middleware.security import setup_security_middleware
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Unified AI Coding Assistant",
    version="1.0.0",
    description="""
    Multi-agent AI coding assistant with multi-LLM support
    
    Features:
    - Code Generation (Claude Sonnet 4.5, GPT-4, Gemini)
    - Code Review & Analysis
    - System Architecture Design
    - GitHub Integration
    - Self-Evolving Learning
    - Rate Limiting & Security
    - Redis Caching
    - Vector Store (RAG)
    
    Agents:
    - Code Generator Agent
    - Code Reviewer Agent
    - System Architect Agent
    - GitHub MCP Agent
    - Self-Evolving Agent
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "API Support",
        "email": "support@example.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Setup security middleware (rate limiting, headers)
setup_security_middleware(app)

# CORS middleware with specific origins for production
allowed_origins = settings.cors_origins if isinstance(settings.cors_origins, list) else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Setup security middleware
# setup_security_middleware(app)  # Temporarily disabled

# Include API routes
app.include_router(router, prefix="/api/v1", tags=["ai-agents"])


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all uncaught exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred. Please try again later.",
            "type": "internal_server_error"
        }
    )


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("=" * 60)
    logger.info("Unified AI Coding Assistant Starting...")
    logger.info("=" * 60)
    logger.info(f"Primary Model: {settings.default_model}")
    logger.info(f"API Host: {settings.api_host}:{settings.api_port}")
    logger.info(f"Fallback Enabled: {settings.enable_fallback}")
    
    # Import here to trigger orchestrator initialization
    try:
        from app.orchestrator import orchestrator
        logger.info(f"Available Models: {orchestrator.get_available_models()}")
        logger.info("✅ All agents initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize orchestrator: {str(e)}")
        logger.warning("Some features may not be available")
    
    logger.info("=" * 60)
    logger.info("🚀 Server is ready to accept requests")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("=" * 60)
    logger.info("Unified AI Coding Assistant Shutting Down...")
    logger.info("=" * 60)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    try:
        from app.orchestrator import orchestrator
        available_models = orchestrator.get_available_models()
    except:
        available_models = []
    
    return {
        "message": "Unified AI Coding Assistant API",
        "version": "1.0.0",
        "status": "operational",
        "available_models": available_models,
        "primary_model": settings.default_model,
        "features": {
            "code_generation": True,
            "code_review": True,
            "architecture_design": True,
            "github_integration": True,
            "self_evolving": True,
            "caching": True,
            "rate_limiting": True
        },
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "models": "/api/v1/models",
            "generate": "/api/v1/generate",
            "review": "/api/v1/review",
            "architecture": "/api/v1/architecture",
            "github": "/api/v1/github/*",
            "learn": "/api/v1/learn/*"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint with system status"""
    try:
        from app.orchestrator import orchestrator
        from app.memory.redis_cache import cache
        from app.memory.vector_store import vector_store
        
        cache_status = cache.get_stats() if hasattr(cache, 'get_stats') else {"enabled": False}
        vector_status = vector_store.get_stats() if hasattr(vector_store, 'get_stats') else {"enabled": False}
        
        return {
            "status": "healthy",
            "service": "unified-ai-coding-assistant",
            "version": "1.0.0",
            "available_models": orchestrator.get_available_models(),
            "primary_model": settings.default_model,
            "services": {
                "api": "operational",
                "redis_cache": "operational" if cache_status.get("enabled") else "disabled",
                "vector_store": "operational" if vector_status.get("enabled") else "disabled"
            },
            "cache_stats": cache_status,
            "vector_stats": vector_status
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": "Service initialization failed"
            }
        )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level="info",
        access_log=True
    )
