"""
Anthropic Claude Sonnet 4.5 Client Implementation
Primary LLM for the Unified AI Coding Assistant
"""
from anthropic import AsyncAnthropic
from typing import Dict, Any, AsyncIterator
from app.models.llm_interface import LLMInterface
import logging

logger = logging.getLogger(__name__)


class ClaudeSonnetClient(LLMInterface):
    """
    Claude Sonnet 4.5 integration for advanced code generation,
    review, and reasoning tasks.
    """
    
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize Claude Sonnet client
        
        Args:
            api_key: Anthropic API key
            model: Model identifier (default: claude-sonnet-4-20250514)
        """
        super().__init__(api_key, model)
        self.client = AsyncAnthropic(api_key=api_key)
        logger.info(f"Initialized ClaudeSonnetClient with model: {model}")
    
    async def generate(
        self,
        system: str,
        user: str,
        temperature: float = 0.2,
        max_tokens: int = 4096,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate completion using Claude Sonnet 4.5
        
        Args:
            system: System prompt defining agent behavior
            user: User request/prompt
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters
            
        Returns:
            Dict with content, model info, and usage statistics
        """
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system,
                messages=[
                    {"role": "user", "content": user}
                ],
                **kwargs
            )
            
            return {
                "content": response.content[0].text,
                "model": self.model,
                "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "stop_reason": response.stop_reason
            }
            
        except Exception as e:
            logger.error(f"Error generating with Claude: {str(e)}")
            raise
    
    async def stream_generate(
        self,
        system: str,
        user: str,
        temperature: float = 0.2,
        max_tokens: int = 4096,
        **kwargs
    ) -> AsyncIterator[str]:
        """
        Stream completion using Claude Sonnet 4.5
        
        Args:
            system: System prompt
            user: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters
            
        Yields:
            Chunks of generated text
        """
        try:
            async with self.client.messages.stream(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system,
                messages=[
                    {"role": "user", "content": user}
                ],
                **kwargs
            ) as stream:
                async for text in stream.text_stream:
                    yield text
                    
        except Exception as e:
            logger.error(f"Error streaming with Claude: {str(e)}")
            raise
