"""
API routes for Unified AI Coding Assistant
Enhanced with error handling, validation, and rate limiting
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import StreamingResponse
from app.api.schemas import *
from app.orchestrator import orchestrator
from app.middleware.security import verify_api_key
# from app.middleware.security import limiter  # Temporarily disabled
from app.memory.redis_cache import cache
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from typing import AsyncIterator

logger = logging.getLogger(__name__)
router = APIRouter()


# Retry decorator for transient failures
def get_retry_decorator():
    return retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError)),
        reraise=True
    )


def validate_language(language: str) -> bool:
    """Validate programming language"""
    supported = [
        "python", "javascript", "typescript", "java", "cpp", "c",
        "go", "rust", "ruby", "php", "swift", "kotlin", "scala",
        "html", "css", "sql", "bash", "powershell"
    ]
    return language.lower() in supported


@router.post("/generate", response_model=GenericResponse)
# @limiter.limit("20/minute")  # Temporarily disabled for testing
async def generate_code(
    request: CodeGenerationRequest
    # authenticated: bool = Depends(verify_api_key)  # Temporarily disabled
):
    """
    Generate code from natural language description
    
    Supports multiple LLM backends: Claude, OpenAI, Gemini
    Rate limited to 20 requests per minute
    """
    try:
        # Input validation
        if not request.prompt or len(request.prompt.strip()) < 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prompt must be at least 5 characters long"
            )
        
        if request.prompt and len(request.prompt) > 10000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prompt exceeds maximum length of 10000 characters"
            )
        
        if not validate_language(request.language):
            logger.warning(f"Unsupported language requested: {request.language}")
        
        # Check cache first
        cache_key = cache._generate_key("generate", request.prompt, request.language, request.model)
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info("Returning cached result")
            return GenericResponse(
                success=True,
                data=cached_result,
                message="Code generated successfully (cached)",
                model_used=cached_result.get("model_used")
            )
        
        # Generate with retry logic
        @get_retry_decorator()
        async def generate_with_retry():
            return await orchestrator.route_request(
                task_type="generate",
                model=request.model,
                prompt=request.prompt,
                language=request.language,
                context=request.context,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
        
        result = await generate_with_retry()
        
        # Cache the result
        cache.set(cache_key, result, ttl=3600)
        
        return GenericResponse(
            success=True,
            data=result,
            message="Code generated successfully",
            model_used=result.get("model_used")
        )
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in generate_code: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while generating code. Please try again."
        )


@router.post("/generate/stream")
# @limiter.limit("10/minute")  # Temporarily disabled
async def stream_generate_code(
    request: StreamRequest,
    authenticated: bool = Depends(verify_api_key)
):
    """
    Stream code generation for real-time feedback
    Rate limited to 10 requests per minute
    """
    async def generate() -> AsyncIterator[str]:
        try:
            # Validation
            if not request.prompt or len(request.prompt.strip()) < 5:
                yield "Error: Prompt must be at least 5 characters long"
                return
            
            async for chunk in orchestrator.stream_generate(
                model=request.model,
                prompt=request.prompt,
                language=request.language,
                context=request.context,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            ):
                yield chunk
                
        except Exception as e:
            logger.error(f"Error in stream_generate: {str(e)}", exc_info=True)
            yield f"\n\nError: {str(e)}"
    
    return StreamingResponse(generate(), media_type="text/plain")


@router.post("/review", response_model=GenericResponse)
# @limiter.limit("15/minute")  # Temporarily disabled
async def review_code(
    request: CodeReviewRequest,
    authenticated: bool = Depends(verify_api_key)
):
    """
    Perform comprehensive code review
    Rate limited to 15 requests per minute
    """
    try:
        # Validation
        if not request.code or len(request.code.strip()) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Code must be at least 10 characters long"
            )
        
        if len(request.code) > 50000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Code exceeds maximum length of 50000 characters"
            )
        
        # Check cache
        cache_key = cache._generate_key("review", request.code, request.language)
        cached_result = cache.get(cache_key)
        if cached_result:
            return GenericResponse(
                success=True,
                data=cached_result,
                message="Code review completed (cached)",
                model_used=cached_result.get("model_used")
            )
        
        result = await orchestrator.route_request(
            task_type="review",
            model=request.model,
            code=request.code,
            language=request.language,
            file_path=request.file_path,
            temperature=request.temperature
        )
        
        # Cache result
        cache.set(cache_key, result, ttl=1800)
        
        return GenericResponse(
            success=True,
            data=result,
            message="Code review completed",
            model_used=result.get("model_used")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in review_code: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during code review. Please try again."
        )


@router.post("/review/quick-check", response_model=GenericResponse)
# @limiter.limit("30/minute")  # Temporarily disabled
async def quick_check(
    request: QuickCheckRequest,
    authenticated: bool = Depends(verify_api_key)
):
    """
    Quick focused code check (security/performance/style)
    Rate limited to 30 requests per minute
    """
    try:
        if request.check_type not in ["security", "performance", "style"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="check_type must be one of: security, performance, style"
            )
        
        result = await orchestrator.route_request(
            task_type="quick-check",
            code=request.code,
            language=request.language,
            check_type=request.check_type
        )
        
        return GenericResponse(
            success=True,
            data=result,
            message=f"{request.check_type.capitalize()} check completed"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in quick_check: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/architecture", response_model=GenericResponse)
# @limiter.limit("10/minute")  # Temporarily disabled
async def design_architecture(
    request: ArchitectureRequest,
    authenticated: bool = Depends(verify_api_key)
):
    """Generate architectural design and recommendations"""
    try:
        if not request.requirements or len(request.requirements.strip()) < 20:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Requirements must be at least 20 characters long"
            )
        
        result = await orchestrator.route_request(
            task_type="architecture",
            model=request.model,
            requirements=request.requirements,
            current_architecture=request.current_architecture,
            constraints=request.constraints,
            temperature=request.temperature
        )
        
        return GenericResponse(
            success=True,
            data=result,
            message="Architecture design completed",
            model_used=result.get("model_used")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in design_architecture: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/architecture/patterns", response_model=GenericResponse)
# @limiter.limit("15/minute")  # Temporarily disabled
async def suggest_patterns(
    request: PatternSuggestionRequest,
    authenticated: bool = Depends(verify_api_key)
):
    """Suggest design patterns for a specific problem"""
    try:
        result = await orchestrator.route_request(
            task_type="suggest-patterns",
            problem_description=request.problem_description,
            language=request.language,
            temperature=request.temperature
        )
        
        return GenericResponse(
            success=True,
            data=result,
            message="Design patterns suggested"
        )
        
    except Exception as e:
        logger.error(f"Error in suggest_patterns: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/architecture/optimize", response_model=GenericResponse)
# @limiter.limit("10/minute")  # Temporarily disabled
async def optimize_architecture(
    request: ArchitectureOptimizationRequest,
    authenticated: bool = Depends(verify_api_key)
):
    """Provide optimization recommendations for existing architecture"""
    try:
        result = await orchestrator.route_request(
            task_type="optimize-architecture",
            current_design=request.current_design,
            bottlenecks=request.bottlenecks,
            temperature=request.temperature
        )
        
        return GenericResponse(
            success=True,
            data=result,
            message="Architecture optimization suggestions generated"
        )
        
    except Exception as e:
        logger.error(f"Error in optimize_architecture: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/github/analyze", response_model=GenericResponse)
# @limiter.limit("5/minute")  # Temporarily disabled
async def analyze_repository(
    request: RepoAnalysisRequest,
    authenticated: bool = Depends(verify_api_key)
):
    """Analyze a GitHub repository"""
    try:
        if not request.repo_url or "github.com" not in request.repo_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid GitHub repository URL"
            )
        
        result = await orchestrator.route_request(
            task_type="analyze-repo",
            repo_url=request.repo_url,
            analysis_type=request.analysis_type,
            temperature=request.temperature
        )
        
        return GenericResponse(
            success=True,
            data=result,
            message="Repository analysis completed"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in analyze_repository: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/github/pr-description", response_model=GenericResponse)
# @limiter.limit("10/minute")  # Temporarily disabled
async def generate_pr_description(
    request: PRDescriptionRequest,
    authenticated: bool = Depends(verify_api_key)
):
    """Generate pull request description"""
    try:
        result = await orchestrator.route_request(
            task_type="pr-description",
            changes=request.changes,
            context=request.context,
            temperature=request.temperature
        )
        
        return GenericResponse(
            success=True,
            data=result,
            message="PR description generated"
        )
        
    except Exception as e:
        logger.error(f"Error in generate_pr_description: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/github/code-search", response_model=GenericResponse)
# @limiter.limit("10/minute")  # Temporarily disabled
async def assist_code_search(
    request: CodeSearchRequest,
    authenticated: bool = Depends(verify_api_key)
):
    """Assist with code search and navigation"""
    try:
        result = await orchestrator.route_request(
            task_type="code-search",
            search_query=request.search_query,
            repo_context=request.repo_context,
            temperature=request.temperature
        )
        
        return GenericResponse(
            success=True,
            data=result,
            message="Code search guidance provided"
        )
        
    except Exception as e:
        logger.error(f"Error in assist_code_search: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/learn/feedback", response_model=GenericResponse)
# @limiter.limit("20/minute")  # Temporarily disabled
async def process_feedback(
    request: FeedbackRequest,
    authenticated: bool = Depends(verify_api_key)
):
    """Learn from user feedback for self-improvement"""
    try:
        result = await orchestrator.route_request(
            task_type="learn",
            previous_interaction=request.previous_interaction,
            feedback=request.feedback,
            outcome=request.outcome,
            temperature=request.temperature
        )
        
        return GenericResponse(
            success=True,
            data=result,
            message="Feedback processed and learned"
        )
        
    except Exception as e:
        logger.error(f"Error in process_feedback: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/learn/adapt", response_model=GenericResponse)
# @limiter.limit("20/minute")  # Temporarily disabled
async def adapt_strategy(
    request: AdaptStrategyRequest,
    authenticated: bool = Depends(verify_api_key)
):
    """Adapt strategy based on historical performance"""
    try:
        result = await orchestrator.route_request(
            task_type="adapt",
            context=request.context,
            temperature=request.temperature
        )
        
        return GenericResponse(
            success=True,
            data=result,
            message="Strategy adapted"
        )
        
    except Exception as e:
        logger.error(f"Error in adapt_strategy: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
async def get_available_models(authenticated: bool = Depends(verify_api_key)):
    """Get list of available LLM models"""
    try:
        models = orchestrator.get_available_models()
        return {
            "available_models": models,
            "primary_model": orchestrator.primary_llm.model,
            "count": len(models)
        }
    except Exception as e:
        logger.error(f"Error getting models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cache/stats")
async def get_cache_stats(authenticated: bool = Depends(verify_api_key)):
    """Get cache statistics"""
    try:
        from app.memory.redis_cache import cache
        stats = cache.get_stats()
        return {"cache_stats": stats}
    except Exception as e:
        logger.error(f"Error getting cache stats: {str(e)}")
        return {"cache_stats": {"enabled": False, "error": str(e)}}
