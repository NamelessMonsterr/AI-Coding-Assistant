"""
Self-Evolving Agent - Learns from feedback and improves over time
"""
from app.models.llm_interface import LLMInterface
from app.utils.prompt_templates import SELF_EVOLVING_TEMPLATE
from typing import Dict, Any, Optional, List
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class SelfEvolvingAgent:
    """
    Agent that learns from interactions and improves responses over time
    Implements feedback loops and strategy refinement
    """
    
    def __init__(self, llm: LLMInterface):
        """
        Initialize Self-Evolving Agent
        
        Args:
            llm: LLM client instance (Claude Sonnet 4.5)
        """
        self.llm = llm
        self.interaction_history: List[Dict] = []
        logger.info("SelfEvolvingAgent initialized")
    
    async def learn_from_feedback(
        self,
        previous_interaction: Dict[str, Any],
        feedback: str,
        outcome: str,
        temperature: float = 0.4
    ) -> Dict[str, Any]:
        """
        Analyze feedback and generate improved strategy
        
        Args:
            previous_interaction: Details of the previous interaction
            feedback: User feedback or corrections
            outcome: Success/failure outcome
            temperature: Sampling temperature
            
        Returns:
            Dict with learned insights and improved strategy
        """
        logger.info("Learning from feedback...")
        
        system_prompt = SELF_EVOLVING_TEMPLATE.format(
            previous_interaction=json.dumps(previous_interaction, indent=2),
            feedback=feedback,
            outcome=outcome
        )
        
        user_prompt = """Analyze this interaction and provide:
1. What worked well
2. What could be improved
3. Specific lessons learned
4. Improved prompt/strategy for similar future tasks
5. Patterns to remember for future interactions
"""
        
        try:
            response = await self.llm.generate(
                system=system_prompt,
                user=user_prompt,
                temperature=temperature,
                max_tokens=2048
            )
            
            learning = {
                "timestamp": datetime.now().isoformat(),
                "analysis": response["content"],
                "previous_interaction": previous_interaction,
                "feedback": feedback,
                "outcome": outcome,
                "model_used": response["model"]
            }
            
            # Store in history
            self.interaction_history.append(learning)
            
            return learning
            
        except Exception as e:
            logger.error(f"Error learning from feedback: {str(e)}")
            raise
    
    async def adapt_strategy(
        self,
        task_type: str,
        context: Optional[str] = None,
        temperature: float = 0.3
    ) -> Dict[str, Any]:
        """
        Adapt strategy based on historical performance
        
        Args:
            task_type: Type of task (code-generation/review/architecture)
            context: Additional context
            temperature: Sampling temperature
            
        Returns:
            Dict with adapted strategy
        """
        logger.info(f"Adapting strategy for {task_type}...")
        
        # Filter relevant history
        relevant_history = [
            h for h in self.interaction_history
            if h.get("previous_interaction", {}).get("task_type") == task_type
        ][-5:]  # Last 5 relevant interactions
        
        system_prompt = f"""You are a self-improving AI agent.
Analyze past performance and adapt strategy for better outcomes.

Task Type: {task_type}
Recent History: {json.dumps(relevant_history, indent=2) if relevant_history else "No history yet"}
"""
        
        user_prompt = f"""Based on past interactions, provide an adapted strategy for {task_type} tasks.

{f"Additional Context: {context}" if context else ""}

Include:
1. Key insights from past performance
2. Adapted approach
3. Specific improvements to implement
4. Success metrics
"""
        
        try:
            response = await self.llm.generate(
                system=system_prompt,
                user=user_prompt,
                temperature=temperature,
                max_tokens=2048
            )
            
            return {
                "adapted_strategy": response["content"],
                "task_type": task_type,
                "based_on_interactions": len(relevant_history),
                "model_used": response["model"]
            }
            
        except Exception as e:
            logger.error(f"Error adapting strategy: {str(e)}")
            raise
    
    def get_interaction_history(self) -> List[Dict]:
        """Get all stored interaction history"""
        return self.interaction_history
    
    def clear_history(self):
        """Clear interaction history"""
        self.interaction_history = []
        logger.info("Interaction history cleared")
