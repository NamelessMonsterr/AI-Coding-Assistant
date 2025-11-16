"""
API Module
Contains routes and schemas for FastAPI endpoints
"""
from app.api.routes import router
from app.api import schemas

__all__ = [
    "router",
    "schemas"
]
