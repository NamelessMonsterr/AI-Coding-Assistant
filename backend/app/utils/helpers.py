"""
Helper utility functions
"""
import hashlib
import json
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


def generate_hash(data: str) -> str:
    """Generate MD5 hash of string data"""
    return hashlib.md5(data.encode()).hexdigest()


def safe_json_dumps(obj: Any) -> str:
    """Safely serialize object to JSON with fallback"""
    try:
        return json.dumps(obj, default=str)
    except Exception as e:
        logger.error(f"Error serializing to JSON: {str(e)}")
        return "{}"


def safe_json_loads(data: str) -> Dict:
    """Safely deserialize JSON with fallback"""
    try:
        return json.loads(data)
    except Exception as e:
        logger.error(f"Error deserializing JSON: {str(e)}")
        return {}


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def extract_code_blocks(text: str) -> list:
    """Extract code blocks from markdown text"""
    import re
    pattern = r"``````"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches
