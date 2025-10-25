"""Configuration file loader and manager"""

import yaml
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from dataclasses import dataclass


@dataclass
class DownloadConfig:
    """Download configuration"""
    only_videos: bool = False
    only_photos: bool = False
    min_date: Optional[datetime] = None
    max_date: Optional[datetime] = None
    video_quality: str = "high"
    stories_include_archived: bool = False


@dataclass
class OutputConfig:
    """Output configuration"""
    use_date_folders: bool = False
    flatten_structure: bool = False
    include_caption: bool = False
    max_filename_length: int = 255


@dataclass
class AdvancedConfig:
    """Advanced configuration"""
    delay_between_items: float = 0.5
    max_retries: int = 3
    log_level: str = "INFO"
    concurrent_downloads: int = 1


@dataclass
class FiltersConfig:
    """Filters configuration"""
    exclude_patterns: list = None
    include_patterns: list = None
    min_size_mb: Optional[float] = None
    max_size_mb: Optional[float] = None
    
    def __post_init__(self):
        if self.exclude_patterns is None:
            self.exclude_patterns = []
        if self.include_patterns is None:
            self.include_patterns = []


class ConfigLoader:
    """Load and manage configuration from YAML file"""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration loader
        
        Args:
            config_path: Path to config.yaml file
        """
        self.config_path = config_path or Path("config.yaml")
        self.download = DownloadConfig()
        self.output = OutputConfig()
        self.advanced = AdvancedConfig()
        self.filters = FiltersConfig()
        
        if self.config_path.exists():
            self.load()
    
    def load(self) -> None:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                data = yaml.safe_load(f) or {}
            
            # Load download config
            if 'download' in data:
                self._load_download_config(data['download'])
            
            # Load output config
            if 'output' in data:
                self._load_output_config(data['output'])
            
            # Load advanced config
            if 'advanced' in data:
                self._load_advanced_config(data['advanced'])
            
            # Load filters config
            if 'filters' in data:
                self._load_filters_config(data['filters'])
                
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
            print("Using default configuration")
    
    def _load_download_config(self, data: Dict[str, Any]) -> None:
        """Load download configuration section"""
        self.download.only_videos = data.get('only_videos', False)
        self.download.only_photos = data.get('only_photos', False)
        self.download.video_quality = data.get('video_quality', 'high')
        self.download.stories_include_archived = data.get('stories_include_archived', False)
        
        # Parse dates
        if data.get('min_date'):
            try:
                self.download.min_date = datetime.strptime(data['min_date'], '%Y-%m-%d')
            except ValueError:
                print(f"Warning: Invalid min_date format: {data['min_date']}")
        
        if data.get('max_date'):
            try:
                self.download.max_date = datetime.strptime(data['max_date'], '%Y-%m-%d')
            except ValueError:
                print(f"Warning: Invalid max_date format: {data['max_date']}")
    
    def _load_output_config(self, data: Dict[str, Any]) -> None:
        """Load output configuration section"""
        self.output.use_date_folders = data.get('use_date_folders', False)
        self.output.flatten_structure = data.get('flatten_structure', False)
        self.output.include_caption = data.get('include_caption', False)
        self.output.max_filename_length = data.get('max_filename_length', 255)
    
    def _load_advanced_config(self, data: Dict[str, Any]) -> None:
        """Load advanced configuration section"""
        self.advanced.delay_between_items = data.get('delay_between_items', 0.5)
        self.advanced.max_retries = data.get('max_retries', 3)
        self.advanced.log_level = data.get('log_level', 'INFO')
        self.advanced.concurrent_downloads = data.get('concurrent_downloads', 1)
    
    def _load_filters_config(self, data: Dict[str, Any]) -> None:
        """Load filters configuration section"""
        self.filters.exclude_patterns = data.get('exclude_patterns', [])
        self.filters.include_patterns = data.get('include_patterns', [])
        self.filters.min_size_mb = data.get('min_size_mb')
        self.filters.max_size_mb = data.get('max_size_mb')
    
    def should_download_item(self, item, item_date: Optional[datetime] = None) -> bool:
        """
        Check if item should be downloaded based on filters
        
        Args:
            item: Item to check
            item_date: Optional item date
            
        Returns:
            True if item should be downloaded
        """
        # Date filters
        if item_date:
            if self.download.min_date and item_date < self.download.min_date:
                return False
            if self.download.max_date and item_date > self.download.max_date:
                return False
        
        # Type filters
        if hasattr(item, 'is_video'):
            if self.download.only_videos and not item.is_video:
                return False
            if self.download.only_photos and item.is_video:
                return False
        
        return True
