#!/usr/bin/env python3
"""Main entry point for IGsaver application"""

import sys
import logging
from pathlib import Path
from typing import Optional

from .app import IGSaver
from .cli import CLI
from .ui import UI
from .exceptions import IGSaverException
from .summary import SummaryReport
from .constants import APP_DESCRIPTION


def main(args: Optional[list] = None) -> int:
    """
    Main application entry point
    
    Args:
        args: Optional command-line arguments
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Parse command-line arguments
        cli = CLI()
        parsed_args = cli.parse_args(args)
        
        # Set logging level
        if parsed_args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        elif parsed_args.quiet:
            logging.getLogger().setLevel(logging.ERROR)
        
        # Print header (unless quiet mode)
        if not parsed_args.quiet:
            UI.print_header(APP_DESCRIPTION)
        
        # Create app with configuration
        app = IGSaver(
            output_dir=parsed_args.output,
            skip_existing=not parsed_args.force,
            show_progress=not parsed_args.no_progress and not parsed_args.quiet,
            config_file=Path("config.yaml") if Path("config.yaml").exists() else None
        )
        
        # Override auth username if specified
        if parsed_args.auth_username:
            app.config._username = parsed_args.auth_username
        
        # Determine target username
        target_username = parsed_args.username
        
        # Run backup (stories or highlights)
        stats = app.run(target_username, download_stories=parsed_args.stories)
        
        # Show summary (unless quiet mode)
        if not parsed_args.quiet:
            output_dir = parsed_args.output or app.config.backup_dir
            target = target_username or app.authenticated_username
            SummaryReport.print_summary(stats, target, output_dir)
        
        # Return appropriate exit code
        if stats.items_failed > 0 or stats.highlights_failed > 0:
            return 1 if stats.items_downloaded == 0 else 0
        
        return 0
        
    except IGSaverException as e:
        if not hasattr(parsed_args, 'quiet') or not parsed_args.quiet:
            UI.print_error(str(e))
        return 1
    except KeyboardInterrupt:
        print("\n")
        UI.print_warning("Operation cancelled by user")
        return 1
    except Exception as e:
        UI.print_error(f"Unexpected error: {e}")
        if hasattr(parsed_args, 'verbose') and parsed_args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def cli_entry() -> None:
    """Command-line entry point"""
    sys.exit(main())


if __name__ == "__main__":
    cli_entry()
