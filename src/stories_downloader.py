"""Download active Instagram stories (24h)"""

import logging
import os
from pathlib import Path
from typing import Optional
import instaloader

from .config import Config
from .ui import UI
from .exceptions import DownloadError, ProfileError
from .constants import ERR_PROFILE_NOT_FOUND, ERR_PRIVATE_PROFILE
from .progress import ProgressTracker
from .summary import BackupStats


class StoriesDownloader:
    """Handle downloading of active Instagram stories (24h)"""
    
    def __init__(
        self, 
        config: Config, 
        loader: instaloader.Instaloader,
        progress: Optional[ProgressTracker] = None,
        skip_existing: bool = True
    ) -> None:
        """
        Initialize stories downloader
        
        Args:
            config: Application configuration
            loader: Authenticated Instaloader instance
            progress: Optional progress tracker
            skip_existing: If True, skip already downloaded files
        """
        self.config = config
        self.loader = loader
        self.logger = logging.getLogger(__name__)
        self.progress = progress or ProgressTracker()
        self.skip_existing = skip_existing
        self.stats = BackupStats()
    
    def download(self, username: str) -> BackupStats:
        """
        Download all active stories for a user
        
        Args:
            username: Instagram username
            
        Returns:
            Backup statistics
            
        Raises:
            ProfileError: If profile cannot be accessed
            DownloadError: If download fails
        """
        try:
            profile = self._get_profile(username)
            
            # Get user's stories
            UI.print_info(f"Fetching active stories from {username}...")
            self.logger.info(f"Fetching stories for {username}")
            
            try:
                stories = list(self.loader.get_stories([profile.userid]))
                
                if not stories:
                    UI.print_warning(f"No active stories found for {username}")
                    self.stats.finish()
                    return self.stats
                
                # Process each story
                for story in stories:
                    self._download_story(username, story)
                
                self.progress.close()
                self.stats.finish()
                return self.stats
                
            except Exception as e:
                self.logger.error(f"Error getting stories: {e}")
                raise DownloadError(f"Could not fetch stories: {e}")
            
        except instaloader.exceptions.ProfileNotExistsException:
            self.logger.error(f"Profile {username} does not exist")
            raise ProfileError(f"{username} - {ERR_PROFILE_NOT_FOUND}")
        except instaloader.exceptions.PrivateProfileNotFollowedException:
            self.logger.error(f"Private profile {username} not followed")
            raise ProfileError(f"{username} {ERR_PRIVATE_PROFILE}")
        except Exception as e:
            self.logger.error(f"Download error: {e}")
            raise DownloadError(f"Download error: {e}")
    
    def _get_profile(self, username: str) -> instaloader.Profile:
        """
        Get Instagram profile
        
        Args:
            username: Instagram username
            
        Returns:
            Profile instance
        """
        UI.print_info(f"\nFetching profile for {username}...")
        self.logger.info(f"Fetching profile: {username}")
        return instaloader.Profile.from_username(self.loader.context, username)
    
    def _download_story(self, username: str, story: instaloader.Story) -> None:
        """
        Download all items from a story
        
        Args:
            username: Instagram username
            story: Story object
        """
        try:
            story_dir = self._get_story_dir(username)
            story_dir.mkdir(parents=True, exist_ok=True)
            
            self.progress.write(f"\n📱 Active Stories")
            
            items_list = list(story.get_items())
            self.stats.items_total += len(items_list)
            
            # Create progress bar for story items
            if len(items_list) > 0:
                pbar = self.progress.create_bar(
                    total=len(items_list),
                    desc="Downloading stories",
                    unit="item"
                )
                
                for item in items_list:
                    try:
                        result = self._download_item(item, story_dir)
                        if result == "downloaded":
                            self.stats.increment_downloaded()
                        elif result == "skipped":
                            self.stats.increment_skipped()
                        else:
                            self.stats.increment_failed()
                        pbar.update(1)
                    except Exception as e:
                        self.logger.warning(f"Error downloading story item: {e}")
                        self.stats.increment_failed()
                        pbar.update(1)
                        continue
                
                pbar.close()
                self.progress.write(f"  ✓ Downloaded {self.stats.items_downloaded} items")
            
        except Exception as e:
            self.logger.error(f"Error downloading story: {e}")
            self.stats.add_error(f"Story download error: {str(e)[:50]}")
    
    def _download_item(self, item: instaloader.StoryItem, target_dir: Path) -> str:
        """
        Download a single story item
        
        Args:
            item: Story item to download
            target_dir: Target directory
            
        Returns:
            Status: "downloaded", "skipped", or "failed"
        """
        try:
            # Check if file already exists (incremental backup)
            if self.skip_existing:
                date_str = item.date_utc.strftime('%Y-%m-%d_%H-%M-%S_UTC')
                video_file = target_dir / f"{date_str}.mp4"
                jpg_file = target_dir / f"{date_str}.jpg"
                
                if video_file.exists() or jpg_file.exists():
                    self.logger.debug(f"Skipping existing item: {date_str}")
                    return "skipped"
            
            # Change to target directory to avoid path issues
            original_dir = os.getcwd()
            os.chdir(target_dir)
            
            try:
                self.loader.download_storyitem(item, '.')
            finally:
                os.chdir(original_dir)
            
            return "downloaded"
        except Exception as e:
            self.logger.warning(f"Failed to download story item: {e}")
            return "failed"
    
    def _get_story_dir(self, username: str) -> Path:
        """
        Get directory path for active stories
        
        Args:
            username: Instagram username
            
        Returns:
            Path to stories directory
        """
        return self.config.backup_dir / username / "stories"
