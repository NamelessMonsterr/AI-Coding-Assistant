"""
Google Gemini Client Implementation
For multimodal code understanding and advanced reasoning
"""
import google.generativeai as genai
from typing import Dict, Any, AsyncIterator
from app.models.llm_interface import LLMInterface
import logging
import asyncio

logger = logging.getLogger(__name__)


class GeminiClient(LLMInterface):
    """
    Google Gemini integration for multimodal code understanding
    """
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash-exp"):
        """
        Initialize Gemini client
        
        Args:
            api_key: Google AI API key
            model: Model identifier (gemini-2.0-flash-exp, gemini-pro)
        """
        super().__init__(api_key, model)
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model)
        logger.info(f"Initialized GeminiClient with model: {model}")
    
    async def generate(
        self,
        system: str,
        user: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate completion using Google Gemini
        
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
            # Combine system and user prompts for Gemini
            combined_prompt = f"""{system}

User Request:
{user}"""
            
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                **kwargs
            )
            
            # Run in executor since genai is sync
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.generate_content(
                    combined_prompt,
                    generation_config=generation_config
                )
            )
            
            return {
                "content": response.text,
                "model": self.model,
                "tokens_used": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0,
                "input_tokens": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else 0,
                "output_tokens": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else 0,
                "stop_reason": "completed"
            }
            
        except Exception as e:
            logger.error(f"Error generating with Gemini: {str(e)}")
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
        Stream completion using Google Gemini
        
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
            combined_prompt = f"""{system}

User Request:
{user}"""
            
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                **kwargs
            )
            
            # Run in executor since genai is sync
            loop = asyncio.get_event_loop()
            response_stream = await loop.run_in_executor(
                None,
                lambda: self.client.generate_content(
                    combined_prompt,
                    generation_config=generation_config,
                    stream=True
                )
            )
            
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            logger.error(f"Error streaming with Gemini: {str(e)}")
            raise
