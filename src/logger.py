"""Logging configuration and utilities"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

from .constants import LOG_FORMAT, LOG_DATE_FORMAT, LOGS_DIR


class Logger:
    """Application logger"""
    
    _instance: Optional[logging.Logger] = None
    
    @classmethod
    def get_logger(cls, name: str = "igsaver", log_file: Optional[Path] = None) -> logging.Logger:
        """
        Get or create logger instance
        
        Args:
            name: Logger name
            log_file: Optional log file path
            
        Returns:
            Configured logger instance
        """
        if cls._instance is None:
            cls._instance = cls._setup_logger(name, log_file)
        return cls._instance
    
    @classmethod
    def _setup_logger(cls, name: str, log_file: Optional[Path] = None) -> logging.Logger:
        """
        Setup logger with file and console handlers
        
        Args:
            name: Logger name
            log_file: Optional log file path
            
        Returns:
            Configured logger
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        
        # Avoid duplicate handlers
        if logger.handlers:
            return logger
        
        formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler
        if log_file is None:
            log_file = LOGS_DIR / f"igsaver_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger
