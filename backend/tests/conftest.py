"""
Pytest configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
import os

# Set test environment variables
os.environ["ANTHROPIC_API_KEY"] = "test-key"
os.environ["OPENAI_API_KEY"] = "test-key"
os.environ["REDIS_HOST"] = "localhost"


@pytest.fixture
def client():
    """FastAPI test client fixture"""
    return TestClient(app)


@pytest.fixture
def mock_settings():
    """Mock settings for testing"""
    return {
        "anthropic_api_key": "test-anthropic-key",
        "openai_api_key": "test-openai-key",
        "default_model": "claude",
        "enable_fallback": True
    }


@pytest.fixture
def sample_code():
    """Sample code for testing"""
    return """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
"""


@pytest.fixture
def sample_prompt():
    """Sample prompt for code generation"""
    return "Create a Python function to calculate the factorial of a number"
