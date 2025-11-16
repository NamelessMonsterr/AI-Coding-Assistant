"""
GitHub MCP Agent - Enhanced with real GitHub API integration
"""
from app.models.llm_interface import LLMInterface
from app.utils.prompt_templates import GITHUB_MCP_TEMPLATE
from app.utils.github_api import GitHubAPIClient
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class GitHubMCPAgent:
    """
    Agent specialized in GitHub operations with real API integration
    """
    
    def __init__(self, llm: LLMInterface, github_token: Optional[str] = None):
        """
        Initialize GitHub MCP Agent
        
        Args:
            llm: LLM client instance
            github_token: GitHub personal access token
        """
        self.llm = llm
        self.github_client = GitHubAPIClient(github_token)
        logger.info("GitHubMCPAgent initialized with API integration")
    
    async def analyze_repository(
        self,
        repo_url: str,
        analysis_type: str = "structure",
        temperature: float = 0.3
    ) -> Dict[str, Any]:
        """
        Analyze a GitHub repository using real API data
        
        Args:
            repo_url: GitHub repository URL
            analysis_type: Type of analysis
            temperature: Sampling temperature
            
        Returns:
            Dict with analysis results
        """
        logger.info(f"Analyzing repository: {repo_url}")
        
        try:
            # Get real repository data from GitHub API
            repo_info = self.github_client.get_repository_info(repo_url)
            languages = self.github_client.get_languages(repo_url)
            
            # Prepare context with real data
            repo_context = f"""
Repository: {repo_info['full_name']}
Description: {repo_info['description']}
Primary Language: {repo_info['language']}
Stars: {repo_info['stars']}
Forks: {repo_info['forks']}
Open Issues: {repo_info['open_issues']}
Languages: {', '.join(languages.keys())}
            """
            
            system_prompt = GITHUB_MCP_TEMPLATE.format(
                repo_context=repo_context,
                operation=f"Analyze repository {analysis_type}"
            )
            
            user_prompt = f"""Analyze this GitHub repository focusing on {analysis_type}.

Repository Data:
{repo_context}

Provide:
1. Repository overview and assessment
2. Key findings for {analysis_type} analysis
3. Strengths and weaknesses
4. Recommendations for improvement
            """
            
            response = await self.llm.generate(
                system=system_prompt,
                user=user_prompt,
                temperature=temperature,
                max_tokens=3096
            )
            
            return {
                "analysis": response["content"],
                "repo_info": repo_info,
                "languages": languages,
                "analysis_type": analysis_type,
                "model_used": response["model"]
            }
            
        except Exception as e:
            logger.error(f"Error analyzing repository: {str(e)}")
            raise
    
    async def suggest_pr_description(
        self,
        changes: str,
        context: Optional[str] = None,
        temperature: float = 0.3
    ) -> Dict[str, Any]:
        """
        Generate pull request description
        
        Args:
            changes: Description of changes made
            context: Additional context
            temperature: Sampling temperature
            
        Returns:
            Dict with PR description
        """
        logger.info("Generating PR description...")
        
        system_prompt = """You are a GitHub collaboration expert.
Generate clear, professional pull request descriptions following best practices."""
        
        user_prompt = f"""Changes made:
{changes}

{f"Context: {context}" if context else ""}

Generate a PR description with:
1. Summary of changes
2. Motivation and context
3. Type of change (bug fix, feature, refactor, etc.)
4. Testing performed
5. Checklist for reviewers
        """
        
        try:
            response = await self.llm.generate(
                system=system_prompt,
                user=user_prompt,
                temperature=temperature,
                max_tokens=2048
            )
            
            return {
                "pr_description": response["content"],
                "model_used": response["model"]
            }
            
        except Exception as e:
            logger.error(f"Error generating PR description: {str(e)}")
            raise
    
    async def code_search_assistant(
        self,
        search_query: str,
        repo_url: Optional[str] = None,
        temperature: float = 0.3
    ) -> Dict[str, Any]:
        """
        Assist with code search using real GitHub search
        
        Args:
            search_query: What to search for
            repo_url: Optional repository to limit search
            temperature: Sampling temperature
            
        Returns:
            Dict with search results and guidance
        """
        logger.info(f"Assisting with code search: {search_query}")
        
        try:
            # Perform real GitHub code search if authenticated
            search_results = []
            if self.github_client.authenticated:
                try:
                    search_results = self.github_client.search_code(search_query, repo_url)
                except Exception as e:
                    logger.warning(f"GitHub search failed: {str(e)}")
            
            system_prompt = """You are a code search expert.
Help users find specific code, patterns, or functionality."""
            
            results_text = "\n".join([
                f"- {r['path']} in {r['repository']}"
                for r in search_results[:5]
            ]) if search_results else "No search results available"
            
            user_prompt = f"""Search query: {search_query}

{f"Repository: {repo_url}" if repo_url else ""}

Found results:
{results_text}

Provide:
1. Analysis of search results
2. Additional search strategies
3. Related patterns to look for
4. GitHub search syntax suggestions
            """
            
            response = await self.llm.generate(
                system=system_prompt,
                user=user_prompt,
                temperature=temperature,
                max_tokens=2048
            )
            
            return {
                "search_guidance": response["content"],
                "search_results": search_results,
                "query": search_query,
                "model_used": response["model"]
            }
            
        except Exception as e:
            logger.error(f"Error with code search: {str(e)}")
            raise
