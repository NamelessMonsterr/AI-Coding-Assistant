"""
Test AI agents
"""
import pytest
from unittest.mock import Mock, AsyncMock
from app.agents.code_generator import CodeGeneratorAgent
from app.agents.code_reviewer import CodeReviewerAgent


class TestCodeGeneratorAgent:
    """Test Code Generator Agent"""
    
    @pytest.fixture
    def mock_llm(self):
        """Create mock LLM"""
        llm = Mock()
        llm.generate = AsyncMock(return_value={
            "content": "def hello(): return 'world'",
            "model": "test-model",
            "tokens_used": 100
        })
        return llm
    
    @pytest.fixture
    def agent(self, mock_llm):
        """Create agent with mock LLM"""
        return CodeGeneratorAgent(mock_llm)
    
    @pytest.mark.asyncio
    async def test_generate_code(self, agent, mock_llm):
        """Test code generation"""
        result = await agent.generate_code(
            prompt="Create a hello world function",
            language="python"
        )
        
        assert "code" in result
        assert "language" in result
        assert result["language"] == "python"
        mock_llm.generate.assert_called_once()


class TestCodeReviewerAgent:
    """Test Code Reviewer Agent"""
    
    @pytest.fixture
    def mock_llm(self):
        """Create mock LLM"""
        llm = Mock()
        llm.generate = AsyncMock(return_value={
            "content": "Code looks good. No major issues found.",
            "model": "test-model",
            "tokens_used": 150
        })
        return llm
    
    @pytest.fixture
    def agent(self, mock_llm):
        """Create agent with mock LLM"""
        return CodeReviewerAgent(mock_llm)
    
    @pytest.mark.asyncio
    async def test_review_code(self, agent, mock_llm, sample_code):
        """Test code review"""
        result = await agent.review_code(
            code=sample_code,
            language="python"
        )
        
        assert "review" in result
        assert "language" in result
        mock_llm.generate.assert_called_once()
