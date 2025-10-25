"""Command-line interface with argparse"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from . import __version__
from .constants import APP_NAME, APP_DESCRIPTION


class CLI:
    """Command-line interface handler"""
    
    def __init__(self) -> None:
        """Initialize CLI argument parser"""
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create argument parser with all options
        
        Returns:
            Configured ArgumentParser
        """
        parser = argparse.ArgumentParser(
            prog=APP_NAME.lower(),
            description=APP_DESCRIPTION,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=self._get_examples()
        )
        
        parser.add_argument(
            '--version',
            action='version',
            version=f'{APP_NAME} {__version__}'
        )
        
        # Target username
        parser.add_argument(
            'username',
            nargs='?',
            help='Instagram username to download from (defaults to authenticated user)'
        )
        
        # Authentication options
        auth_group = parser.add_argument_group('authentication options')
        auth_group.add_argument(
            '-u', '--user',
            dest='auth_username',
            metavar='USERNAME',
            help='Username for authentication (instead of .env)'
        )
        
        # Download options
        download_group = parser.add_argument_group('download options')
        download_group.add_argument(
            '--highlights-only',
            action='store_true',
            help='Download only highlights (default behavior)'
        )
        download_group.add_argument(
            '--stories',
            action='store_true',
            help='Download active stories (24h) instead of highlights'
        )
        download_group.add_argument(
            '--skip-existing',
            action='store_true',
            default=True,
            help='Skip already downloaded items (default: enabled)'
        )
        download_group.add_argument(
            '--force',
            action='store_true',
            help='Force re-download all items (disable incremental backup)'
        )
        
        # Output options
        output_group = parser.add_argument_group('output options')
        output_group.add_argument(
            '-o', '--output',
            metavar='DIR',
            type=Path,
            help='Custom output directory (default: ./backups)'
        )
        output_group.add_argument(
            '--list',
            action='store_true',
            help='List available highlights without downloading'
        )
        output_group.add_argument(
            '-q', '--quiet',
            action='store_true',
            help='Minimal output (errors only)'
        )
        output_group.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Verbose output (debug info)'
        )
        output_group.add_argument(
            '--no-progress',
            action='store_true',
            help='Disable progress bars'
        )
        
        return parser
    
    def _get_examples(self) -> str:
        """
        Get usage examples
        
        Returns:
            Formatted examples string
        """
        return """
examples:
  # Download your own highlights
  igsaver.py
  
  # Download from specific user
  igsaver.py username
  
  # Download with custom output directory
  igsaver.py -o /path/to/backups username
  
  # List highlights without downloading
  igsaver.py --list username
  
  # Force re-download everything
  igsaver.py --force
  
  # Quiet mode (minimal output)
  igsaver.py -q username
  
  # Verbose mode (debug info)
  igsaver.py -v username
"""
    
    def parse_args(self, args: Optional[list] = None) -> argparse.Namespace:
        """
        Parse command-line arguments
        
        Args:
            args: Optional argument list (defaults to sys.argv)
            
        Returns:
            Parsed arguments namespace
        """
        parsed = self.parser.parse_args(args)
        
        # Validate conflicting options
        if parsed.force and parsed.skip_existing:
            parsed.skip_existing = False
        
        if parsed.quiet and parsed.verbose:
            self.parser.error("--quiet and --verbose are mutually exclusive")
        
        return parsed
