"""Progress tracking and visual feedback"""

from typing import Optional
from tqdm import tqdm


class ProgressTracker:
    """Handle progress bars and tracking"""
    
    def __init__(self, disable: bool = False) -> None:
        """
        Initialize progress tracker
        
        Args:
            disable: If True, disable all progress bars
        """
        self.disable = disable
        self.current_bar: Optional[tqdm] = None
    
    def create_bar(self, total: int, desc: str, unit: str = "item") -> tqdm:
        """
        Create a new progress bar
        
        Args:
            total: Total number of items
            desc: Description of what's being processed
            unit: Unit name for items
            
        Returns:
            tqdm progress bar instance
        """
        if self.current_bar:
            self.current_bar.close()
        
        self.current_bar = tqdm(
            total=total,
            desc=desc,
            unit=unit,
            disable=self.disable,
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]'
        )
        return self.current_bar
    
    def update(self, n: int = 1) -> None:
        """
        Update current progress bar
        
        Args:
            n: Number of items to increment
        """
        if self.current_bar:
            self.current_bar.update(n)
    
    def close(self) -> None:
        """Close current progress bar"""
        if self.current_bar:
            self.current_bar.close()
            self.current_bar = None
    
    def write(self, message: str) -> None:
        """
        Write message without breaking progress bar
        
        Args:
            message: Message to write
        """
        if self.current_bar:
            self.current_bar.write(message)
        else:
            print(message)
