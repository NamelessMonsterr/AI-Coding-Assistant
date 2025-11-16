"""
Application constants and configuration values
"""

# Model identifiers
CLAUDE_MODEL = "claude-sonnet-4-20250514"
OPENAI_MODEL = "gpt-4-turbo-preview"
GEMINI_MODEL = "gemini-2.0-flash-exp"
HUGGINGFACE_MODEL = "Salesforce/codegen-350M-mono"

# Default parameters
DEFAULT_TEMPERATURE = 0.2
DEFAULT_MAX_TOKENS = 4096
CODE_GENERATION_TEMPERATURE = 0.2
CODE_REVIEW_TEMPERATURE = 0.3
ARCHITECTURE_TEMPERATURE = 0.4

# Supported languages
SUPPORTED_LANGUAGES = [
    "python", "javascript", "typescript", "java", "cpp", "c",
    "go", "rust", "ruby", "php", "swift", "kotlin", "scala",
    "html", "css", "sql", "bash", "powershell"
]

# Rate limits
RATE_LIMIT_GENERATE = 20
RATE_LIMIT_REVIEW = 15
RATE_LIMIT_ARCHITECTURE = 10
RATE_LIMIT_GITHUB = 5
RATE_LIMIT_QUICK_CHECK = 30

# Cache TTL (seconds)
CACHE_TTL_GENERATE = 3600
CACHE_TTL_REVIEW = 1800
CACHE_TTL_ARCHITECTURE = 7200