"""
Central Orchestrator - Routes requests to appropriate agents and LLMs
Supports multiple LLM providers with fallback and ensemble capabilities
"""
from app.models.claude_sonnet_client import ClaudeSonnetClient
from app.models.openai_client import OpenAIClient
from app.models.gemini_client import GeminiClient
# from app.models.huggingface_client import HuggingFaceClient  # Commented out to avoid torch import issues
from app.agents.code_generator import CodeGeneratorAgent
from app.agents.code_reviewer import CodeReviewerAgent
from app.agents.system_architect import SystemArchitectAgent
from app.agents.github_mcp import GitHubMCPAgent
from app.agents.self_evolving import SelfEvolvingAgent
from app.config import settings
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Central orchestrator that manages all agents and LLMs
    Provides intelligent routing, fallback, and ensemble capabilities
    """
    
    def __init__(self):
        """Initialize orchestrator with all LLMs and agents"""
        logger.info("Initializing AgentOrchestrator with multi-LLM support...")
        
        # Initialize available LLM clients
        self.llms = {}
        
        # Claude Sonnet 4.5 (Primary for code generation and reasoning)
        if settings.anthropic_api_key:
            try:
                self.llms['claude'] = ClaudeSonnetClient(
                    api_key=settings.anthropic_api_key,
                    model=settings.claude_model
                )
                logger.info("✅ Claude Sonnet initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Claude: {e}")
        
        # OpenAI GPT-4 (Fallback and alternative)
        if settings.openai_api_key:
            try:
                self.llms['openai'] = OpenAIClient(
                    api_key=settings.openai_api_key,
                    model=settings.openai_model
                )
                logger.info("✅ OpenAI GPT-4 initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI: {e}")
        
        # Google Gemini (Multimodal capabilities)
        if settings.gemini_api_key:
            try:
                self.llms['gemini'] = GeminiClient(
                    api_key=settings.gemini_api_key,
                    model=settings.gemini_model
                )
                logger.info("✅ Google Gemini initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini: {e}")
        
        # Hugging Face (Local/open-source option) - Commented by default
        # try:
        #     self.llms['huggingface'] = HuggingFaceClient(
        #         model=settings.huggingface_model
        #     )
        #     logger.info("✅ Hugging Face model initialized")
        # except Exception as e:
        #     logger.warning(f"Failed to initialize Hugging Face: {e}")
        
        if not self.llms:
            raise RuntimeError("No LLM clients initialized! Please provide at least one API key.")
        
        # Get primary LLM
        self.primary_llm = self.llms.get(settings.default_model) or list(self.llms.values())[0]
        logger.info(f"Primary LLM: {settings.default_model}")
        
        # Initialize agents with primary LLM
        self.code_generator = CodeGeneratorAgent(self.primary_llm)
        self.code_reviewer = CodeReviewerAgent(self.primary_llm)
        self.system_architect = SystemArchitectAgent(self.primary_llm)
        self.github_mcp = GitHubMCPAgent(
            self.primary_llm,
            github_token=settings.github_token
        )
        self.self_evolving = SelfEvolvingAgent(self.primary_llm)
        
        logger.info(f"AgentOrchestrator initialized with {len(self.llms)} LLM(s)")

    def get_available_models(self):
        """Get list of available LLM models"""
        return list(self.llms.keys())

    def get_llm(self, model_name: Optional[str] = None):
        """Get specific LLM or primary LLM"""
        if model_name and model_name in self.llms:
            return self.llms[model_name]
        return self.primary_llm
    
    async def route_request(
        self,
        task_type: str,
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Route request to appropriate agent with specified or primary LLM
        
        Args:
            task_type: Type of task (generate/review/architecture/github/learn)
            model: Optional specific model to use (claude/openai/gemini/huggingface)
            **kwargs: Task-specific parameters
            
        Returns:
            Dict with task results
        """
        logger.info(f"Routing task: {task_type} with model: {model or 'primary'}")
        
        # If specific model requested, temporarily update agent's LLM
        original_llm = None
        if model and model in self.llms:
            target_llm = self.llms[model]
        else:
            target_llm = self.primary_llm
        
        try:
            if task_type == "generate":
                # Temporarily swap LLM if needed
                if model:
                    original_llm = self.code_generator.llm
                    self.code_generator.llm = target_llm
                
                result = await self.code_generator.generate_code(**kwargs)
                
                # Restore original LLM
                if original_llm:
                    self.code_generator.llm = original_llm
                    
                return result
            
            elif task_type == "review":
                if model:
                    original_llm = self.code_reviewer.llm
                    self.code_reviewer.llm = target_llm
                    
                result = await self.code_reviewer.review_code(**kwargs)
                
                if original_llm:
                    self.code_reviewer.llm = original_llm
                    
                return result
            
            elif task_type == "quick-check":
                return await self.code_reviewer.quick_check(**kwargs)
            
            elif task_type == "architecture":
                if model:
                    original_llm = self.system_architect.llm
                    self.system_architect.llm = target_llm
                    
                result = await self.system_architect.design_architecture(**kwargs)
                
                if original_llm:
                    self.system_architect.llm = original_llm
                    
                return result
            
            elif task_type == "suggest-patterns":
                return await self.system_architect.suggest_patterns(**kwargs)
            
            elif task_type == "optimize-architecture":
                return await self.system_architect.optimize_architecture(**kwargs)
            
            elif task_type == "analyze-repo":
                return await self.github_mcp.analyze_repository(**kwargs)
            
            elif task_type == "pr-description":
                return await self.github_mcp.suggest_pr_description(**kwargs)
            
            elif task_type == "code-search":
                return await self.github_mcp.code_search_assistant(**kwargs)
            
            elif task_type == "learn":
                return await self.self_evolving.learn_from_feedback(**kwargs)
            
            elif task_type == "adapt":
                return await self.self_evolving.adapt_strategy(**kwargs)
            
            else:
                raise ValueError(f"Unknown task type: {task_type}")
                
        except Exception as e:
            logger.error(f"Error routing task {task_type}: {str(e)}")
            
            # Fallback to another model if enabled
            if settings.enable_fallback and model != 'openai' and 'openai' in self.llms:
                logger.info("Attempting fallback to OpenAI...")
                return await self.route_request(task_type, model='openai', **kwargs)
            
            raise
    
    async def stream_generate(self, model: Optional[str] = None, **kwargs):
        """
        Stream code generation with specified or primary LLM

        Args:
            model: Optional specific model to use (claude/openai/gemini)
            **kwargs: Task-specific parameters (prompt, language, context, etc.)

        Yields:
            Chunks of generated text
        """
        logger.info(f"Streaming generation with model: {model or 'primary'}")

        # Get target LLM
        target_llm = self.llms.get(model) if model else self.primary_llm

        # Temporarily swap LLM in code generator
        original_llm = self.code_generator.llm
        self.code_generator.llm = target_llm

        try:
            async for chunk in self.code_generator.stream_generate_code(**kwargs):
                yield chunk
        except Exception as e:
            logger.error(f"Error in stream_generate: {str(e)}")

            # Try fallback if enabled
            if settings.enable_fallback and model != 'openai' and 'openai' in self.llms:
                logger.info("Attempting fallback to OpenAI for streaming...")
                try:
                    self.code_generator.llm = self.llms['openai']
                    async for chunk in self.code_generator.stream_generate_code(**kwargs):
                        yield chunk
                except Exception as fallback_error:
                    logger.error(f"Fallback also failed: {str(fallback_error)}")
                    yield f"\n\nError: {str(fallback_error)}"
            else:
                yield f"\n\nError: {str(e)}"
        finally:
            # Always restore original LLM
            self.code_generator.llm = original_llm


# Global orchestrator instance
orchestrator = AgentOrchestrator()
