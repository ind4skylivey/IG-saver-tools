"""Backup summary and statistics"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional
from pathlib import Path


@dataclass
class BackupStats:
    """Statistics for a backup operation"""
    
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    
    highlights_found: int = 0
    highlights_downloaded: int = 0
    highlights_skipped: int = 0
    highlights_failed: int = 0
    
    items_total: int = 0
    items_downloaded: int = 0
    items_skipped: int = 0
    items_failed: int = 0
    
    bytes_downloaded: int = 0
    
    errors: List[str] = field(default_factory=list)
    
    def finish(self) -> None:
        """Mark backup as finished"""
        self.end_time = datetime.now()
    
    @property
    def duration(self) -> timedelta:
        """Get backup duration"""
        end = self.end_time or datetime.now()
        return end - self.start_time
    
    @property
    def duration_str(self) -> str:
        """Get formatted duration string"""
        total_seconds = int(self.duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    @property
    def size_str(self) -> str:
        """Get formatted size string"""
        bytes_val = self.bytes_downloaded
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.1f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.1f} TB"
    
    def add_error(self, error: str) -> None:
        """
        Add an error to the list
        
        Args:
            error: Error message
        """
        self.errors.append(error)
    
    def increment_downloaded(self, file_size: int = 0) -> None:
        """
        Increment downloaded counters
        
        Args:
            file_size: Size of downloaded file in bytes
        """
        self.items_downloaded += 1
        self.bytes_downloaded += file_size
    
    def increment_skipped(self) -> None:
        """Increment skipped counter"""
        self.items_skipped += 1
    
    def increment_failed(self) -> None:
        """Increment failed counter"""
        self.items_failed += 1


class SummaryReport:
    """Generate and display backup summary reports"""
    
    @staticmethod
    def generate(stats: BackupStats, target_user: str, output_dir: Path) -> str:
        """
        Generate summary report
        
        Args:
            stats: Backup statistics
            target_user: Target username
            output_dir: Output directory
            
        Returns:
            Formatted summary string
        """
        lines = []
        lines.append("\n" + "=" * 60)
        lines.append("BACKUP SUMMARY")
        lines.append("=" * 60)
        lines.append(f"Target: {target_user}")
        lines.append(f"Output: {output_dir}")
        lines.append(f"Duration: {stats.duration_str}")
        lines.append("")
        
        # Highlights summary
        lines.append("Highlights:")
        lines.append(f"  ✓ Downloaded: {stats.highlights_downloaded}")
        if stats.highlights_skipped > 0:
            lines.append(f"  ⊘ Skipped: {stats.highlights_skipped}")
        if stats.highlights_failed > 0:
            lines.append(f"  ✗ Failed: {stats.highlights_failed}")
        lines.append(f"  ━ Total found: {stats.highlights_found}")
        lines.append("")
        
        # Items summary
        lines.append("Items:")
        lines.append(f"  ✓ Downloaded: {stats.items_downloaded}")
        if stats.items_skipped > 0:
            lines.append(f"  ⊘ Skipped (already exist): {stats.items_skipped}")
        if stats.items_failed > 0:
            lines.append(f"  ✗ Failed: {stats.items_failed}")
        lines.append(f"  ━ Total: {stats.items_total}")
        lines.append("")
        
        # Size info
        if stats.bytes_downloaded > 0:
            lines.append(f"Downloaded: {stats.size_str}")
            lines.append("")
        
        # Errors
        if stats.errors:
            lines.append("Errors:")
            for i, error in enumerate(stats.errors[:5], 1):  # Show max 5 errors
                lines.append(f"  {i}. {error[:70]}...")
            if len(stats.errors) > 5:
                lines.append(f"  ... and {len(stats.errors) - 5} more errors")
            lines.append("")
        
        # Status
        if stats.items_failed == 0 and stats.highlights_failed == 0:
            lines.append("✓ BACKUP COMPLETED SUCCESSFULLY")
        elif stats.items_downloaded > 0:
            lines.append("⚠ BACKUP COMPLETED WITH SOME ERRORS")
        else:
            lines.append("✗ BACKUP FAILED")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    @staticmethod
    def print_summary(stats: BackupStats, target_user: str, output_dir: Path) -> None:
        """
        Print summary report to console
        
        Args:
            stats: Backup statistics
            target_user: Target username
            output_dir: Output directory
        """
        summary = SummaryReport.generate(stats, target_user, output_dir)
        print(summary)
