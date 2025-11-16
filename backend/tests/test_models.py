"""
Test LLM model clients
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.models.claude_sonnet_client import ClaudeSonnetClient
from app.models.openai_client import OpenAIClient


class TestClaudeSonnetClient:
    """Test Claude Sonnet client"""
    
    @pytest.fixture
    def claude_client(self):
        """Create Claude client fixture"""
        return ClaudeSonnetClient(api_key="test-key")
    
    def test_client_initialization(self, claude_client):
        """Test client initializes correctly"""
        assert claude_client.api_key == "test-key"
        assert claude_client.model == "claude-sonnet-4-20250514"
    
    @pytest.mark.asyncio
    async def test_generate_method_exists(self, claude_client):
        """Test generate method exists and has correct signature"""
        assert hasattr(claude_client, 'generate')
        assert callable(claude_client.generate)
    
    @pytest.mark.asyncio
    async def test_stream_generate_method_exists(self, claude_client):
        """Test stream_generate method exists"""
        assert hasattr(claude_client, 'stream_generate')
        assert callable(claude_client.stream_generate)


class TestOpenAIClient:
    """Test OpenAI client"""
    
    @pytest.fixture
    def openai_client(self):
        """Create OpenAI client fixture"""
        return OpenAIClient(api_key="test-key")
    
    def test_client_initialization(self, openai_client):
        """Test client initializes correctly"""
        assert openai_client.api_key == "test-key"
        assert "gpt-4" in openai_client.model
    
    @pytest.mark.asyncio
    async def test_generate_method_exists(self, openai_client):
        """Test generate method exists"""
        assert hasattr(openai_client, 'generate')
        assert callable(openai_client.generate)
