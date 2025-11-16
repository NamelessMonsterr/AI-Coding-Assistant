"""
Hugging Face Client Implementation
For local/open-source model integration (CodeBERT, CodeT5, etc.)
"""
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from typing import Dict, Any, AsyncIterator, Optional
from app.models.llm_interface import LLMInterface
import logging
import torch
import asyncio

logger = logging.getLogger(__name__)


class HuggingFaceClient(LLMInterface):
    """
    Hugging Face integration for local/open-source models
    Supports models like CodeT5, CodeBERT, StarCoder, etc.
    """
    
    def __init__(
        self, 
        api_key: str = None,  # Not needed for local models
        model: str = "Salesforce/codegen-350M-mono",
        device: str = "auto"
    ):
        """
        Initialize Hugging Face client
        
        Args:
            api_key: Optional (not needed for local models)
            model: Model identifier from Hugging Face Hub
            device: Device to run on (auto/cpu/cuda)
        """
        super().__init__(api_key or "local", model)
        
        logger.info(f"Loading Hugging Face model: {model}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model)
            self.model_instance = AutoModelForCausalLM.from_pretrained(
                model,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map=device
            )
            
            # Create pipeline for easier generation
            self.pipeline = pipeline(
                "text-generation",
                model=self.model_instance,
                tokenizer=self.tokenizer,
                device_map=device
            )
            
            logger.info(f"Successfully loaded {model}")
            
        except Exception as e:
            logger.error(f"Error loading Hugging Face model: {str(e)}")
            raise
    
    async def generate(
        self,
        system: str,
        user: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate completion using Hugging Face model
        
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
            # Combine prompts
            combined_prompt = f"""{system}

{user}"""
            
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.pipeline(
                    combined_prompt,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    do_sample=True,
                    top_p=0.95,
                    **kwargs
                )
            )
            
            generated_text = result[0]['generated_text']
            # Remove the prompt from output
            output = generated_text[len(combined_prompt):].strip()
            
            return {
                "content": output,
                "model": self.model,
                "tokens_used": len(self.tokenizer.encode(generated_text)),
                "input_tokens": len(self.tokenizer.encode(combined_prompt)),
                "output_tokens": len(self.tokenizer.encode(output)),
                "stop_reason": "completed"
            }
            
        except Exception as e:
            logger.error(f"Error generating with Hugging Face: {str(e)}")
