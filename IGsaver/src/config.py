"""Configuration management"""

import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

from .constants import ROOT_DIR, BACKUPS_DIR, SESSIONS_DIR, LOGS_DIR


class Config:
    """Application configuration manager"""
    
    def __init__(self, env_file: Optional[Path] = None) -> None:
        """
        Initialize configuration
        
        Args:
            env_file: Optional path to .env file
        """
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()
        
        self._username: Optional[str] = os.getenv('IG_USERNAME')
        self._setup_directories()
    
    def _setup_directories(self) -> None:
        """Create required directories if they don't exist"""
        BACKUPS_DIR.mkdir(exist_ok=True)
        SESSIONS_DIR.mkdir(exist_ok=True)
        LOGS_DIR.mkdir(exist_ok=True)
    
    @property
    def username(self) -> Optional[str]:
        """Get configured username"""
        return self._username
    
    @property
    def backup_dir(self) -> Path:
        """Get backups directory path"""
        return getattr(self, '_backup_dir', BACKUPS_DIR)
    
    @property
    def session_dir(self) -> Path:
        """Get sessions directory path"""
        return SESSIONS_DIR
    
    @property
    def logs_dir(self) -> Path:
        """Get logs directory path"""
        return LOGS_DIR
    
    @property
    def root_dir(self) -> Path:
        """Get root directory path"""
        return ROOT_DIR
