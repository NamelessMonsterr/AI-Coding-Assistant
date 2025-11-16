"""
Code Reviewer Agent - Automated code quality assessment and review
"""
from app.models.llm_interface import LLMInterface
from app.utils.prompt_templates import CODE_REVIEW_TEMPLATE
from typing import Dict, Any, List, Optional
import logging
import json

logger = logging.getLogger(__name__)


class CodeReviewerAgent:
    """
    Agent specialized in code review, bug detection, and quality assessment
    """
    
    def __init__(self, llm: LLMInterface):
        """
        Initialize Code Reviewer Agent
        
        Args:
            llm: LLM client instance (Claude Sonnet 4.5)
        """
        self.llm = llm
        logger.info("CodeReviewerAgent initialized")
    
    async def review_code(
        self,
        code: str,
        language: str = "python",
        file_path: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """
        Perform comprehensive code review
        
        Args:
            code: Code to review
            language: Programming language
            file_path: Optional file path for context
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            
        Returns:
            Dict containing review findings, score, and recommendations
        """
        logger.info(f"Reviewing {language} code...")
        
        system_prompt = CODE_REVIEW_TEMPLATE.format(
            language=language,
            file_path=file_path or "Unknown file"
        )
        
        user_prompt = f"""Review the following code:

{code}

text

Provide a structured review with:
1. Overall quality score (0-10)
2. List of issues found (with severity, category, line number if applicable, description, and recommendation)
3. Positive aspects
4. Summary of key improvements needed
"""
        
        try:
            response = await self.llm.generate(
                system=system_prompt,
                user=user_prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            content = response["content"]
            
            return {
                "review": content,
                "language": language,
                "file_path": file_path,
                "model_used": response["model"],
                "tokens_used": response["tokens_used"]
            }
            
        except Exception as e:
            logger.error(f"Error reviewing code: {str(e)}")
            raise
    
    async def quick_check(
        self,
        code: str,
        language: str = "python",
        check_type: str = "security"
    ) -> Dict[str, Any]:
        """
        Quick focused check (security, performance, or style)
        
        Args:
            code: Code to check
            language: Programming language
            check_type: Type of check (security/performance/style)
            
        Returns:
            Dict with focused findings
        """
        logger.info(f"Running {check_type} check on {language} code...")
        
        check_prompts = {
            "security": "Focus on security vulnerabilities, injection risks, and authentication issues.",
            "performance": "Focus on performance bottlenecks, inefficiencies, and optimization opportunities.",
            "style": "Focus on code style, conventions, and readability."
        }
        
        system_prompt = f"""You are a code analysis expert specializing in {check_type} analysis.
{check_prompts.get(check_type, "")}

Provide concise, actionable findings."""
        
        user_prompt = f"""Analyze this {language} code for {check_type} issues:

{code}
"""

        try:
            response = await self.llm.generate(
                system=system_prompt,
                user=user_prompt,
                temperature=0.2,
                max_tokens=2048
            )
            
            return {
                "findings": response["content"],
                "check_type": check_type,
                "language": language,
                "model_used": response["model"]
            }
            
        except Exception as e:
            logger.error(f"Error in quick check: {str(e)}")
            raise