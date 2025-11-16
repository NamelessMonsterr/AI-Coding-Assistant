"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class CodeGenerationRequest(BaseModel):
    """Request schema for code generation"""
    prompt: str = Field(..., description="Natural language description of desired code")
    language: str = Field(default="python", description="Programming language")
    context: Optional[str] = Field(None, description="Additional project context")
    temperature: float = Field(default=0.2, ge=0.0, le=1.0, description="Sampling temperature")
    max_tokens: int = Field(default=4096, ge=100, le=8000, description="Maximum tokens")
    model: Optional[str] = Field(None, description="Specific LLM to use (claude/openai/gemini)")


class CodeReviewRequest(BaseModel):
    """Request schema for code review"""
    code: str = Field(..., description="Code to review")
    language: str = Field(default="python", description="Programming language")
    file_path: Optional[str] = Field(None, description="File path for context")
    temperature: float = Field(default=0.3, ge=0.0, le=1.0)
    model: Optional[str] = Field(None, description="Specific LLM to use")


class QuickCheckRequest(BaseModel):
    """Request schema for quick focused checks"""
    code: str = Field(..., description="Code to check")
    language: str = Field(default="python", description="Programming language")
    check_type: str = Field(..., description="Type of check (security/performance/style)")


class ArchitectureRequest(BaseModel):
    """Request schema for architecture design"""
    requirements: str = Field(..., description="Project requirements and goals")
    current_architecture: Optional[str] = Field(None, description="Existing architecture")
    constraints: Optional[str] = Field(None, description="Technical or business constraints")
    temperature: float = Field(default=0.4, ge=0.0, le=1.0)
    model: Optional[str] = Field(None, description="Specific LLM to use")


class PatternSuggestionRequest(BaseModel):
    """Request schema for design pattern suggestions"""
    problem_description: str = Field(..., description="Description of problem to solve")
    language: str = Field(default="python", description="Programming language")
    temperature: float = Field(default=0.3, ge=0.0, le=1.0)


class ArchitectureOptimizationRequest(BaseModel):
    """Request schema for architecture optimization"""
    current_design: str = Field(..., description="Current architecture description")
    bottlenecks: Optional[str] = Field(None, description="Known issues")
    temperature: float = Field(default=0.3, ge=0.0, le=1.0)


class RepoAnalysisRequest(BaseModel):
    """Request schema for repository analysis"""
    repo_url: str = Field(..., description="GitHub repository URL")
    analysis_type: str = Field(default="structure", description="Type of analysis")
    temperature: float = Field(default=0.3, ge=0.0, le=1.0)


class PRDescriptionRequest(BaseModel):
    """Request schema for PR description generation"""
    changes: str = Field(..., description="Description of changes made")
    context: Optional[str] = Field(None, description="Additional context")
    temperature: float = Field(default=0.3, ge=0.0, le=1.0)


class CodeSearchRequest(BaseModel):
    """Request schema for code search assistance"""
    search_query: str = Field(..., description="What to search for")
    repo_context: Optional[str] = Field(None, description="Repository context")
    temperature: float = Field(default=0.3, ge=0.0, le=1.0)


class FeedbackRequest(BaseModel):
    """Request schema for self-evolving feedback"""
    previous_interaction: Dict[str, Any] = Field(..., description="Previous interaction details")
    feedback: str = Field(..., description="User feedback or corrections")
    outcome: str = Field(..., description="Success/failure outcome")
    temperature: float = Field(default=0.4, ge=0.0, le=1.0)


class AdaptStrategyRequest(BaseModel):
    """Request schema for strategy adaptation"""
    task_type: str = Field(..., description="Task type to adapt for")
    context: Optional[str] = Field(None, description="Additional context")
    temperature: float = Field(default=0.3, ge=0.0, le=1.0)


class GenericResponse(BaseModel):
    """Generic response schema"""
    success: bool
    data: Dict[str, Any]
    message: Optional[str] = None
    model_used: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    available_models: List[str]
    primary_model: str


class StreamRequest(BaseModel):
    """Request schema for streaming generation"""
    prompt: str = Field(..., description="Natural language prompt")
    language: str = Field(default="python", description="Programming language")
    context: Optional[str] = Field(None, description="Additional context")
    temperature: float = Field(default=0.2, ge=0.0, le=1.0)
    max_tokens: int = Field(default=4096, ge=100, le=8000)
    model: Optional[str] = Field(None, description="Specific LLM to use")
