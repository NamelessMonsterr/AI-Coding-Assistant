"""
System Architect Agent - High-level architecture and design guidance
"""
from app.models.llm_interface import LLMInterface
from app.utils.prompt_templates import SYSTEM_ARCHITECT_TEMPLATE
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class SystemArchitectAgent:
    """
    Agent specialized in system architecture, design patterns, and high-level guidance
    """
    
    def __init__(self, llm: LLMInterface):
        """
        Initialize System Architect Agent
        
        Args:
            llm: LLM client instance (Claude Sonnet 4.5)
        """
        self.llm = llm
        logger.info("SystemArchitectAgent initialized")
    
    async def design_architecture(
        self,
        requirements: str,
        current_architecture: Optional[str] = None,
        constraints: Optional[str] = None,
        temperature: float = 0.4,
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """
        Generate architectural design and recommendations
        
        Args:
            requirements: Project requirements and goals
            current_architecture: Existing architecture description
            constraints: Technical or business constraints
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            
        Returns:
            Dict containing architecture design, diagrams, and recommendations
        """
        logger.info("Designing system architecture...")
        
        system_prompt = SYSTEM_ARCHITECT_TEMPLATE.format(
            requirements=requirements,
            current_architecture=current_architecture or "New project - no existing architecture"
        )
        
        user_prompt = f"""Design a system architecture based on these requirements:

{requirements}

{f"Constraints: {constraints}" if constraints else ""}

Provide:
1. High-level architecture overview
2. Component breakdown with responsibilities
3. Data flow and interactions
4. Technology stack recommendations
5. Scalability and deployment considerations
6. Mermaid diagram syntax for visualization (if applicable)
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
                "architecture": content,
                "requirements": requirements,
                "model_used": response["model"],
                "tokens_used": response["tokens_used"]
            }
            
        except Exception as e:
            logger.error(f"Error designing architecture: {str(e)}")
            raise
    
    async def suggest_patterns(
        self,
        problem_description: str,
        language: str = "python",
        temperature: float = 0.3
    ) -> Dict[str, Any]:
        """
        Suggest design patterns for a specific problem
        
        Args:
            problem_description: Description of the problem to solve
            language: Programming language context
            temperature: Sampling temperature
            
        Returns:
            Dict with pattern suggestions and implementations
        """
        logger.info("Suggesting design patterns...")
        
        system_prompt = f"""You are an expert in software design patterns and {language} best practices.
Suggest appropriate design patterns with rationale and implementation guidance."""
        
        user_prompt = f"""Problem: {problem_description}

Language: {language}

Suggest:
1. Most appropriate design pattern(s)
2. Why this pattern fits the problem
3. Implementation approach in {language}
4. Trade-offs and considerations
5. Code example showing the pattern
"""
        
        try:
            response = await self.llm.generate(
                system=system_prompt,
                user=user_prompt,
                temperature=temperature,
                max_tokens=3096
            )
            
            return {
                "suggestions": response["content"],
                "problem": problem_description,
                "language": language,
                "model_used": response["model"]
            }
            
        except Exception as e:
            logger.error(f"Error suggesting patterns: {str(e)}")
            raise
    
    async def optimize_architecture(
        self,
        current_design: str,
        bottlenecks: Optional[str] = None,
        temperature: float = 0.3
    ) -> Dict[str, Any]:
        """
        Provide optimization recommendations for existing architecture
        
        Args:
            current_design: Current architecture description
            bottlenecks: Known performance or scaling issues
            temperature: Sampling temperature
            
        Returns:
            Dict with optimization recommendations
        """
        logger.info("Optimizing architecture...")
        
        system_prompt = """You are a senior software architect specializing in system optimization.
Analyze architectures for performance, scalability, and maintainability improvements."""
        
        user_prompt = f"""Current Architecture:
{current_design}

{f"Known Bottlenecks: {bottlenecks}" if bottlenecks else ""}

Provide optimization recommendations for:
1. Performance improvements
2. Scalability enhancements
3. Cost reduction opportunities
4. Maintainability improvements
5. Technology upgrades or migrations
"""
        
        try:
            response = await self.llm.generate(
                system=system_prompt,
                user=user_prompt,
                temperature=temperature,
                max_tokens=3096
            )
            
            return {
                "optimizations": response["content"],
                "current_design": current_design,
                "model_used": response["model"]
            }
            
        except Exception as e:
            logger.error(f"Error optimizing architecture: {str(e)}")
            raise
