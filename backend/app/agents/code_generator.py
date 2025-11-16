"""
Code Generator Agent - Specialized in generating code from natural language
"""
from app.models.llm_interface import LLMInterface
from app.utils.prompt_templates import CODE_GENERATION_TEMPLATE
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class CodeGeneratorAgent:
    """
    Agent specialized in code generation using Claude Sonnet 4.5
    """
    
    def __init__(self, llm: LLMInterface):
        """
        Initialize Code Generator Agent
        
        Args:
            llm: LLM client instance (Claude Sonnet 4.5)
        """
        self.llm = llm
        logger.info("CodeGeneratorAgent initialized")
    
    async def generate_code(
        self,
        prompt: str,
        language: str = "python",
        context: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """
        Generate code from natural language description
        
        Args:
            prompt: Natural language description of desired code
            language: Programming language (python, javascript, typescript, etc.)
            context: Additional project context
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Dict containing generated code, explanation, and metadata
        """
        logger.info(f"Generating {language} code for prompt: {prompt[:50]}...")
        
        system_prompt = CODE_GENERATION_TEMPLATE.format(
            language=language,
            context=context or "No additional context provided"
        )
        
        try:
            response = await self.llm.generate(
                system=system_prompt,
                user=prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Extract code and explanation
            content = response["content"]
            
            return {
                "code": content,
                "language": language,
                "model_used": response["model"],
                "tokens_used": response["tokens_used"],
                "input_tokens": response.get("input_tokens", 0),
                "output_tokens": response.get("output_tokens", 0)
            }
            
        except Exception as e:
            logger.error(f"Error generating code: {str(e)}")
            raise
    
    async def stream_generate_code(
        self,
        prompt: str,
        language: str = "python",
        context: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 4096
    ):
        """
        Stream code generation for real-time feedback
        
        Args:
            prompt: Natural language description
            language: Programming language
            context: Additional context
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            
        Yields:
            Chunks of generated code
        """
        logger.info(f"Streaming {language} code generation...")
        
        system_prompt = CODE_GENERATION_TEMPLATE.format(
            language=language,
            context=context or "No additional context provided"
        )
        
        try:
            async for chunk in self.llm.stream_generate(
                system=system_prompt,
                user=prompt,
                temperature=temperature,
                max_tokens=max_tokens
            ):
                yield chunk
                
        except Exception as e:
            logger.error(f"Error streaming code: {str(e)}")
            raise
