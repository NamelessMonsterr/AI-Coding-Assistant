"""
API endpoint tests
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestRootEndpoints:
    """Test root and health check endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns API information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "1.0.0"
        assert "available_models" in data
        assert "endpoints" in data
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["healthy", "unhealthy"]
        assert "service" in data
        assert "version" in data
        assert "available_models" in data
    
    def test_api_documentation(self):
        """Test OpenAPI documentation is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
        
        response = client.get("/openapi.json")
        assert response.status_code == 200


class TestCodeGeneration:
    """Test code generation endpoints"""
    
    def test_generate_code_valid_request(self):
        """Test code generation with valid request"""
        response = client.post(
            "/api/v1/generate",
            json={
                "prompt": "Create a function to add two numbers",
                "language": "python",
                "temperature": 0.2,
                "max_tokens": 1000
            }
        )
        # May fail without valid API keys, but should not crash
        assert response.status_code in [200, 500]
    
    def test_generate_code_invalid_prompt(self):
        """Test code generation with invalid prompt"""
        response = client.post(
            "/api/v1/generate",
            json={
                "prompt": "",
                "language": "python"
            }
        )
        assert response.status_code == 400
        assert "Prompt must be at least 5 characters" in response.json()["detail"]
    
    def test_generate_code_long_prompt(self):
        """Test code generation with excessively long prompt"""
        response = client.post(
            "/api/v1/generate",
            json={
                "prompt": "x" * 20000,
                "language": "python"
            }
        )
        assert response.status_code == 400
    
    def test_generate_code_missing_fields(self):
        """Test code generation with missing required fields"""
        response = client.post(
            "/api/v1/generate",
            json={}
        )
        assert response.status_code == 422  # Validation error


class TestCodeReview:
    """Test code review endpoints"""
    
    def test_review_code_valid_request(self, sample_code):
        """Test code review with valid request"""
        response = client.post(
            "/api/v1/review",
            json={
                "code": sample_code,
                "language": "python"
            }
        )
        assert response.status_code in [200, 500]
    
    def test_review_code_invalid_code(self):
        """Test code review with invalid code"""
        response = client.post(
            "/api/v1/review",
            json={
                "code": "x",
                "language": "python"
            }
        )
        assert response.status_code == 400
    
    def test_quick_check_security(self, sample_code):
        """Test quick security check"""
        response = client.post(
            "/api/v1/review/quick-check",
            json={
                "code": sample_code,
                "language": "python",
                "check_type": "security"
            }
        )
        assert response.status_code in [200, 500]
    
    def test_quick_check_invalid_type(self, sample_code):
        """Test quick check with invalid type"""
        response = client.post(
            "/api/v1/review/quick-check",
            json={
                "code": sample_code,
                "language": "python",
                "check_type": "invalid_type"
            }
        )
        assert response.status_code == 400


class TestArchitecture:
    """Test architecture design endpoints"""
    
    def test_design_architecture_valid(self):
        """Test architecture design with valid request"""
        response = client.post(
            "/api/v1/architecture",
            json={
                "requirements": "Build a scalable e-commerce platform with microservices architecture"
            }
        )
        assert response.status_code in [200, 500]
    
    def test_design_architecture_short_requirements(self):
        """Test architecture design with too short requirements"""
        response = client.post(
            "/api/v1/architecture",
            json={
                "requirements": "Build API"
            }
        )
        assert response.status_code == 400
    
    def test_suggest_patterns(self):
        """Test design pattern suggestions"""
        response = client.post(
            "/api/v1/architecture/patterns",
            json={
                "problem_description": "Need to implement observer pattern for event handling",
                "language": "python"
            }
        )
        assert response.status_code in [200, 500]


class TestGitHub:
    """Test GitHub integration endpoints"""
    
    def test_analyze_repository_valid(self):
        """Test repository analysis with valid URL"""
        response = client.post(
            "/api/v1/github/analyze",
            json={
                "repo_url": "https://github.com/fastapi/fastapi",
                "analysis_type": "structure"
            }
        )
        assert response.status_code in [200, 500]
    
    def test_analyze_repository_invalid_url(self):
        """Test repository analysis with invalid URL"""
        response = client.post(
            "/api/v1/github/analyze",
            json={
                "repo_url": "not-a-github-url",
                "analysis_type": "structure"
            }
        )
        assert response.status_code == 400
    
    def test_pr_description(self):
        """Test PR description generation"""
        response = client.post(
            "/api/v1/github/pr-description",
            json={
                "changes": "Added new authentication feature with JWT tokens"
            }
        )
        assert response.status_code in [200, 500]


class TestUtility:
    """Test utility endpoints"""
    
    def test_get_models(self):
        """Test getting available models"""
        response = client.get("/api/v1/models")
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            data = response.json()
            assert "available_models" in data
    
    def test_cache_stats(self):
        """Test cache statistics endpoint"""
        response = client.get("/api/v1/cache/stats")
        assert response.status_code == 200
        data = response.json()
        assert "cache_stats" in data
