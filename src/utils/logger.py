"""
Logging utility for Horse Trainer AI

This module configures the logging for the application.
"""
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

def setup_logger(level='INFO', log_file=None):
    """
    Set up the logger for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to the log file. If None, logs will only go to console.
    
    Returns:
        The configured logger object
    """
    # Convert string level to logging level
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(numeric_level)
    
    # Remove existing handlers to avoid duplication in case of reconfiguration
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if log_file is specified
    if log_file:
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_default_log_file():
    """
    Get the default log file path.
    
    Returns:
        Path to the default log file
    """
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return str(log_dir / f'horse_trainer_{timestamp}.log')

def log_exception(logger, exc_info=True):
    """
    Log an exception with traceback.
    
    Args:
        logger: The logger object
        exc_info: Whether to include exception info in the log
    """
    logger.error("Exception occurred", exc_info=exc_info)

