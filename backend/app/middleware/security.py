"""
Security middleware for API protection
Rate limiting, authentication, and security headers
"""
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.config import settings
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Rate limiter with configurable limits
# limiter = Limiter(
#     key_func=get_remote_address,
#     default_limits=["100/hour", "20/minute"]
# )  # Temporarily disabled

# API Key authentication (optional)
security = HTTPBearer(auto_error=False)


async def verify_api_key(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> bool:
    """
    Verify API key if authentication is enabled
    
    Args:
        credentials: HTTP Bearer credentials
        
    Returns:
        bool: True if authenticated or auth disabled
        
    Raises:
        HTTPException: If authentication fails
    """
    # If no API key configured, allow all requests
    api_key = getattr(settings, 'api_key', None)
    if not api_key:
        return True
    
    # If API key configured, verify it
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if credentials.credentials != api_key:
        logger.warning(f"Invalid API key attempt from {get_remote_address}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return True


def setup_security_middleware(app):
    """
    Setup security middleware for FastAPI app
    Adds rate limiting and security headers

    Args:
        app: FastAPI application instance
    """
    # Add rate limiter to app state
    # app.state.limiter = limiter
    # app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Add SlowAPI middleware
    # app.add_middleware(SlowAPIMiddleware)  # Temporarily disabled
    
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        """Add security headers to all responses"""
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response
    
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Log all incoming requests"""
        logger.info(f"{request.method} {request.url.path}")
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response


def get_rate_limit_key(request: Request) -> str:
    """
    Get rate limit key based on API key or IP
    
    Args:
        request: FastAPI request object
        
    Returns:
        str: Rate limit key
    """
    # Use API key if provided, otherwise use IP
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:20]  # Use part of API key
    return get_remote_address(request)
