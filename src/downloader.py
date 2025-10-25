"""Download management for Instagram highlights"""

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


class HighlightsDownloader:
    """Handle downloading of Instagram highlights"""
    
    def __init__(
        self, 
        config: Config, 
        loader: instaloader.Instaloader,
        progress: Optional[ProgressTracker] = None,
        skip_existing: bool = True
    ) -> None:
        """
        Initialize downloader
        
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
        Download all highlights for a user
        
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
            highlights_list = list(self._get_highlights(profile))
            
            self.stats.highlights_found = len(highlights_list)
            
            if self.stats.highlights_found == 0:
                UI.print_warning(f"No highlights found for {username}")
                self.stats.finish()
                return self.stats
            
            # Create progress bar for highlights
            pbar = self.progress.create_bar(
                total=self.stats.highlights_found,
                desc="Processing highlights",
                unit="highlight"
            )
            
            for highlight in highlights_list:
                result = self._download_highlight(username, highlight)
                if result == "downloaded":
                    self.stats.highlights_downloaded += 1
                elif result == "skipped":
                    self.stats.highlights_skipped += 1
                else:
                    self.stats.highlights_failed += 1
                pbar.update(1)
            
            pbar.close()
            self.stats.finish()
            return self.stats
            
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
    
    def _get_highlights(self, profile: instaloader.Profile) -> instaloader.NodeIterator:
        """
        Get highlights from profile
        
        Args:
            profile: Instagram profile
            
        Returns:
            Iterator of highlights
        """
        UI.print_info(f"Downloading highlights from {profile.username}...")
        self.logger.info(f"Fetching highlights for {profile.username}")
        return self.loader.get_highlights(profile)
    
    def _download_highlight(self, username: str, highlight: instaloader.Highlight) -> str:
        """
        Download a single highlight
        
        Args:
            username: Instagram username
            highlight: Highlight to download
            
        Returns:
            True if download successful
        """
        try:
            highlight_dir = self._get_highlight_dir(username, highlight.title)
            highlight_dir.mkdir(parents=True, exist_ok=True)
            
            self.logger.info(f"Processing highlight: {highlight.title}")
            self.progress.write(f"\n📁 {highlight.title}")
            
            items_downloaded = 0
            items_failed = 0
            
            # Direct iteration approach - let errors bubble up per item
            try:
                items_list = list(highlight.get_items())
                self.stats.items_total += len(items_list)
                
                for item in items_list:
                    try:
                        result = self._download_item(item, highlight_dir)
                        if result == "downloaded":
                            items_downloaded += 1
                            self.stats.increment_downloaded()
                        elif result == "skipped":
                            items_downloaded += 1  # Count as success
                            self.stats.increment_skipped()
                        else:
                            items_failed += 1
                            self.stats.increment_failed()
                    except KeyError as ke:
                        self.logger.warning(f"Skipping item - missing data: {ke}")
                        items_failed += 1
                        self.stats.increment_failed()
                        continue
                    except Exception as item_error:
                        self.logger.warning(f"Error on item: {item_error}")
                        items_failed += 1
                        self.stats.increment_failed()
                        continue
                        
            except (KeyError, AttributeError) as e:
                # Highlight structure issue - log and skip
                self.logger.error(f"Cannot access items in highlight '{highlight.title}': {e}")
                self.progress.write(f"  ⚠  No accessible items (may be expired)")
                self.stats.add_error(f"Highlight '{highlight.title}': {str(e)[:50]}")
                return "failed"
            
            total_items = items_downloaded + items_failed
            
            if total_items > 0:
                self.progress.write(f"  ✓ {items_downloaded} items, {items_failed} failed")
            else:
                self.progress.write(f"  ⚠  No items found")
            
            self.logger.info(
                f"Highlight '{highlight.title}': {items_downloaded} succeeded, {items_failed} failed"
            )
            
            if items_downloaded > 0:
                return "downloaded"
            elif items_failed == 0:
                return "skipped"
            else:
                return "failed"
            
        except Exception as e:
            self.logger.error(f"Error downloading highlight {highlight.title}: {e}", exc_info=True)
            self.progress.write(f"  ✗ Error: {str(e)[:50]}")
            self.stats.add_error(f"Highlight '{highlight.title}': {str(e)[:50]}")
            return "failed"
    
    def _download_highlight_native(self, highlight: instaloader.Highlight, target_dir: Path) -> None:
        """
        Download highlight using instaloader's native method
        
        Args:
            highlight: Highlight to download
            target_dir: Target directory
        """
        try:
            # Save current dirname_pattern
            old_pattern = self.loader.dirname_pattern
            self.loader.dirname_pattern = str(target_dir)
            
            # Download using native method
            self.loader.download_highlight(
                highlight=highlight,
                target=str(target_dir.parent.parent.name)  # username
            )
            
            # Restore pattern
            self.loader.dirname_pattern = old_pattern
            
            self.logger.info(f"Downloaded highlight using native method: {highlight.title}")
        except Exception as e:
            self.logger.error(f"Native download failed: {e}")
            raise
    
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
            self.logger.warning(f"Failed to download item: {e}")
            return "failed"
    
    def _get_highlight_dir(self, username: str, highlight_title: str) -> Path:
        """
        Get directory path for highlight
        
        Args:
            username: Instagram username
            highlight_title: Title of highlight
            
        Returns:
            Path to highlight directory
        """
        return self.config.backup_dir / username / "highlights" / highlight_title
    
    def _show_summary(self, username: str, count: int) -> None:
        """
        Show download summary
        
        Args:
            username: Instagram username
            count: Number of highlights downloaded
        """
        if count == 0:
            UI.print_info(f"\nNo highlights found for {username}")
        else:
            location = str(self.config.backup_dir / username)
            UI.show_summary(count, "highlights", location)
        
        self.logger.info(f"Download complete: {count} highlights for {username}")
