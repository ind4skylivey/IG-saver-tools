"""Main application class"""

import logging
from pathlib import Path
from typing import Optional
import instaloader

from .config import Config
from .auth import Authenticator
from .downloader import HighlightsDownloader
from .stories_downloader import StoriesDownloader
from .logger import Logger
from .exceptions import IGSaverException
from .progress import ProgressTracker
from .summary import BackupStats
from .config_loader import ConfigLoader
from .constants import (
    DOWNLOAD_VIDEOS,
    DOWNLOAD_VIDEO_THUMBNAILS,
    DOWNLOAD_GEOTAGS,
    DOWNLOAD_COMMENTS,
    SAVE_METADATA,
    COMPRESS_JSON,
)


class IGSaver:
    """Main application class orchestrating all components"""
    
    def __init__(
        self, 
        config: Optional[Config] = None,
        output_dir: Optional[Path] = None,
        skip_existing: bool = True,
        show_progress: bool = True,
        config_file: Optional[Path] = None
    ) -> None:
        """
        Initialize application
        
        Args:
            config: Optional configuration instance
            output_dir: Custom output directory
            skip_existing: Enable incremental backup
            show_progress: Show progress bars
        """
        self.config = config or Config()
        
        # Load configuration file if exists
        self.config_loader = ConfigLoader(config_file)
        
        # Override output directory if specified
        if output_dir:
            self.config._backup_dir = output_dir
            output_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger = Logger.get_logger()
        self.loader = self._create_loader()
        self.authenticator = Authenticator(self.config, self.loader)
        
        # Create progress tracker
        self.progress = ProgressTracker(disable=not show_progress)
        
        # Create downloaders with progress and skip_existing
        self.highlights_downloader = HighlightsDownloader(
            self.config, 
            self.loader,
            progress=self.progress,
            skip_existing=skip_existing
        )
        
        self.stories_downloader = StoriesDownloader(
            self.config,
            self.loader,
            progress=self.progress,
            skip_existing=skip_existing
        )
        
        self.authenticated_username: Optional[str] = None
    
    def _create_loader(self) -> instaloader.Instaloader:
        """
        Create and configure Instaloader instance
        
        Returns:
            Configured Instaloader instance
        """
        return instaloader.Instaloader(
            download_videos=DOWNLOAD_VIDEOS,
            download_video_thumbnails=DOWNLOAD_VIDEO_THUMBNAILS,
            download_geotags=DOWNLOAD_GEOTAGS,
            download_comments=DOWNLOAD_COMMENTS,
            save_metadata=SAVE_METADATA,
            compress_json=COMPRESS_JSON,
            dirname_pattern='{target}'
        )
    
    def authenticate(self) -> None:
        """
        Authenticate user
        
        Raises:
            IGSaverException: If authentication fails
        """
        try:
            self.authenticated_username = self.authenticator.authenticate()
        except IGSaverException as e:
            self.logger.error(f"Authentication failed: {e}")
            raise
    
    def download_highlights(self, username: Optional[str] = None) -> BackupStats:
        """
        Download highlights for a user
        
        Args:
            username: Optional username to download from (defaults to authenticated user)
            
        Returns:
            Backup statistics
            
        Raises:
            IGSaverException: If download fails
        """
        target_username = username or self.authenticated_username
        
        if not target_username:
            raise IGSaverException("No username specified for download")
        
        try:
            stats = self.highlights_downloader.download(target_username)
            self.progress.close()
            return stats
        except IGSaverException as e:
            self.logger.error(f"Download failed: {e}")
            self.progress.close()
            raise
    
    def download_stories(self, username: Optional[str] = None) -> BackupStats:
        """
        Download active stories (24h) for a user
        
        Args:
            username: Optional username to download from (defaults to authenticated user)
            
        Returns:
            Backup statistics
            
        Raises:
            IGSaverException: If download fails
        """
        target_username = username or self.authenticated_username
        
        if not target_username:
            raise IGSaverException("No username specified for download")
        
        try:
            stats = self.stories_downloader.download(target_username)
            self.progress.close()
            return stats
        except IGSaverException as e:
            self.logger.error(f"Download failed: {e}")
            self.progress.close()
            raise
    
    def run(self, target_username: Optional[str] = None, download_stories: bool = False) -> BackupStats:
        """
        Run complete backup process
        
        Args:
            target_username: Optional username to backup (defaults to authenticated user)
            download_stories: If True, download active stories instead of highlights
            
        Returns:
            Backup statistics
            
        Raises:
            IGSaverException: If process fails
        """
        self.authenticate()
        
        if download_stories:
            return self.download_stories(target_username)
        else:
            return self.download_highlights(target_username)
