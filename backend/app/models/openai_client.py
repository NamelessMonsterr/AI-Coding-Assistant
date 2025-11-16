"""
OpenAI GPT-4 / Codex Client Implementation
For code generation, completion, and general-purpose tasks
"""
from openai import AsyncOpenAI
from typing import Dict, Any, AsyncIterator
from app.models.llm_interface import LLMInterface
import logging

logger = logging.getLogger(__name__)


class OpenAIClient(LLMInterface):
    """
    OpenAI GPT-4 / Codex integration for code generation and reasoning
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview"):
        """
        Initialize OpenAI client
        
        Args:
            api_key: OpenAI API key
            model: Model identifier (gpt-4-turbo-preview, gpt-4, gpt-3.5-turbo)
        """
        super().__init__(api_key, model)
        self.client = AsyncOpenAI(api_key=api_key)
        logger.info(f"Initialized OpenAIClient with model: {model}")
    
    async def generate(
        self,
        system: str,
        user: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate completion using OpenAI GPT-4
        
        Args:
            system: System prompt
            user: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters
            
        Returns:
            Dict with content, model info, and usage statistics
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            return {
                "content": response.choices[0].message.content,
                "model": self.model,
                "tokens_used": response.usage.total_tokens,
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "stop_reason": response.choices[0].finish_reason
            }
            
        except Exception as e:
            logger.error(f"Error generating with OpenAI: {str(e)}")
            raise
    
    async def stream_generate(
        self,
        system: str,
        user: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> AsyncIterator[str]:
        """
        Stream completion using OpenAI GPT-4
        
        Args:
            system: System prompt
            user: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            **kwargs: Additional parameters
            
        Yields:
            Chunks of generated text
        """
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                **kwargs
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"Error streaming with OpenAI: {str(e)}")
            raise
