"""
Structured logging configuration
"""
import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging(log_level: str = "INFO"):
    """Setup structured JSON logging"""
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Console handler with JSON format
    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s',
        rename_fields={'timestamp': '@timestamp', 'level': 'severity'}
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # File handler for errors
    error_handler = logging.FileHandler('errors.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    return logger
