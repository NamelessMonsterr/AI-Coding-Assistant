"""
GitHub API Integration using PyGithub
Provides real GitHub operations: repo analysis, PR management, code search
"""
from github import Github, GithubException
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class GitHubAPIClient:
    """
    GitHub API client for repository operations
    """
    
    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize GitHub API client
        
        Args:
            access_token: GitHub personal access token
        """
        self.github = Github(access_token) if access_token else Github()
        self.authenticated = access_token is not None
        logger.info(f"GitHub API initialized (authenticated: {self.authenticated})")
    
    def get_repository_info(self, repo_url: str) -> Dict[str, Any]:
        """
        Get basic repository information
        
        Args:
            repo_url: GitHub repository URL or owner/repo format
            
        Returns:
            Dict with repository details
        """
        try:
            # Extract owner/repo from URL
            repo_name = self._parse_repo_url(repo_url)
            repo = self.github.get_repo(repo_name)
            
            return {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "language": repo.language,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "open_issues": repo.open_issues_count,
                "created_at": repo.created_at.isoformat(),
                "updated_at": repo.updated_at.isoformat(),
                "default_branch": repo.default_branch,
                "size": repo.size,
                "url": repo.html_url,
                "topics": repo.get_topics(),
                "license": repo.license.name if repo.license else None
            }
            
        except GithubException as e:
            logger.error(f"GitHub API error: {str(e)}")
            raise
    
    def get_repository_structure(self, repo_url: str, path: str = "") -> List[Dict]:
        """
        Get repository file structure
        
        Args:
            repo_url: GitHub repository URL
            path: Path within repository (empty for root)
            
        Returns:
            List of files and directories
        """
        try:
            repo_name = self._parse_repo_url(repo_url)
            repo = self.github.get_repo(repo_name)
            contents = repo.get_contents(path)
            
            structure = []
            for content in contents:
                structure.append({
                    "name": content.name,
                    "path": content.path,
                    "type": content.type,  # "file" or "dir"
                    "size": content.size if content.type == "file" else None,
                    "url": content.html_url
                })
            
            return structure
            
        except GithubException as e:
            logger.error(f"Error getting repository structure: {str(e)}")
            raise
    
    def get_languages(self, repo_url: str) -> Dict[str, int]:
        """
        Get programming languages used in repository
        
        Args:
            repo_url: GitHub repository URL
            
        Returns:
            Dict of language: bytes_of_code
        """
        try:
            repo_name = self._parse_repo_url(repo_url)
            repo = self.github.get_repo(repo_name)
            return repo.get_languages()
            
        except GithubException as e:
            logger.error(f"Error getting languages: {str(e)}")
            raise
    
    def search_code(self, query: str, repo_url: Optional[str] = None) -> List[Dict]:
        """
        Search code in repository or globally
        
        Args:
            query: Search query
            repo_url: Optional repository to limit search
            
        Returns:
            List of code search results
        """
        try:
            if repo_url:
                repo_name = self._parse_repo_url(repo_url)
                full_query = f"{query} repo:{repo_name}"
            else:
                full_query = query
            
            results = self.github.search_code(full_query)
            
            code_results = []
            for result in results[:10]:  # Limit to top 10 results
                code_results.append({
                    "name": result.name,
                    "path": result.path,
                    "repository": result.repository.full_name,
                    "url": result.html_url,
                    "score": result.score
                })
            
            return code_results
            
        except GithubException as e:
            logger.error(f"Error searching code: {str(e)}")
            raise
    
    def get_pull_requests(self, repo_url: str, state: str = "open") -> List[Dict]:
        """
        Get pull requests from repository
        
        Args:
            repo_url: GitHub repository URL
            state: PR state (open/closed/all)
            
        Returns:
            List of pull requests
        """
        try:
            repo_name = self._parse_repo_url(repo_url)
            repo = self.github.get_repo(repo_name)
            pulls = repo.get_pulls(state=state)
            
            pr_list = []
            for pr in pulls[:20]:  # Limit to 20 PRs
                pr_list.append({
                    "number": pr.number,
                    "title": pr.title,
                    "state": pr.state,
                    "created_at": pr.created_at.isoformat(),
                    "updated_at": pr.updated_at.isoformat(),
                    "user": pr.user.login,
                    "url": pr.html_url,
                    "mergeable": pr.mergeable,
                    "merged": pr.merged
                })
            
            return pr_list
            
        except GithubException as e:
            logger.error(f"Error getting pull requests: {str(e)}")
            raise
    
    def get_file_content(self, repo_url: str, file_path: str) -> str:
        """
        Get content of a specific file
        
        Args:
            repo_url: GitHub repository URL
            file_path: Path to file in repository
            
        Returns:
            File content as string
        """
        try:
            repo_name = self._parse_repo_url(repo_url)
            repo = self.github.get_repo(repo_name)
            content = repo.get_contents(file_path)
            
            if content.encoding == "base64":
                import base64
                return base64.b64decode(content.content).decode('utf-8')
            return content.decoded_content.decode('utf-8')
            
        except GithubException as e:
            logger.error(f"Error getting file content: {str(e)}")
            raise
    
    def _parse_repo_url(self, repo_url: str) -> str:
        """
        Parse repository URL to owner/repo format
        
        Args:
            repo_url: GitHub URL or owner/repo
            
        Returns:
            owner/repo string
        """
        # If already in owner/repo format
        if "/" in repo_url and "github.com" not in repo_url:
            return repo_url
        
        # Extract from URL
        if "github.com" in repo_url:
            parts = repo_url.rstrip("/").split("/")
            return f"{parts[-2]}/{parts[-1].replace('.git', '')}"
        
        return repo_url
