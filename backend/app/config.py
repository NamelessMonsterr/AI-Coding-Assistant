"""
Enhanced configuration with validation and dynamic updates
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, validator
from typing import Optional, List, Dict, Any
import os


class Settings(BaseSettings):
    """Application settings with comprehensive validation"""
    
    # API Keys
    anthropic_api_key: Optional[str] = Field(None, min_length=20)
    openai_api_key: Optional[str] = Field(None, min_length=20)
    gemini_api_key: Optional[str] = Field(None, min_length=20)
    github_token: Optional[str] = None
    
    # Security
    api_key: Optional[str] = None
    secret_key: str = Field(default_factory=lambda: os.urandom(32).hex())
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = Field(default=6379, ge=1, le=65535)
    redis_password: Optional[str] = None
    redis_db: int = Field(default=0, ge=0)
    redis_enabled: bool = True
    
    # Models
    default_model: str = Field(default="claude", pattern="^(claude|openai|gemini|auto)$")
    claude_model: str = "claude-sonnet-4-20250514"
    openai_model: str = "gpt-4-turbo-preview"
    gemini_model: str = "gemini-2.0-flash-exp"
    
    # Generation parameters
    max_tokens: int = Field(default=4096, ge=100, le=32000)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    
    # API Server
    api_host: str = "0.0.0.0"
    api_port: int = Field(default=8000, ge=1024, le=65535)
    api_workers: int = Field(default=4, ge=1, le=16)
    
    # Vector Store
    chroma_persist_directory: str = "./chroma_db"
    chroma_enabled: bool = True
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Features
    enable_fallback: bool = True
    enable_ensemble: bool = False
    enable_streaming: bool = True
    enable_rag: bool = True
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_default: str = "100/hour"
    
    # Monitoring
    enable_metrics: bool = True
    enable_tracing: bool = False
    
    # Logging
    log_level: str = Field(default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    log_format: str = Field(default="json", pattern="^(json|text)$")
    
    @validator('cors_origins', pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    @property
    def has_llm_key(self) -> bool:
        """Check if at least one LLM API key is configured"""
        return any([
            self.anthropic_api_key,
            self.openai_api_key,
            self.gemini_api_key
        ])
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()

# Validate on startup
if not settings.has_llm_key:
    import warnings
    warnings.warn("No LLM API keys configured. AI features will not work.")
