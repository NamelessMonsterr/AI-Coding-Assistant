"""
Abstract interface for LLM clients
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, AsyncIterator


class LLMInterface(ABC):
    """Abstract base class for all LLM providers"""
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
    
    @abstractmethod
    async def generate(
        self,
        system: str,
        user: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate completion from the LLM
        
        Args:
            system: System prompt
            user: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional model-specific parameters
            
        Returns:
            Dict containing response content, model info, and metadata
        """
        pass
    
    @abstractmethod
    async def stream_generate(
        self,
        system: str,
        user: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> AsyncIterator[str]:
        """
        Stream completion from the LLM
        
        Args:
            system: System prompt
            user: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional model-specific parameters
            
        Yields:
            Chunks of generated text
        """
        pass
