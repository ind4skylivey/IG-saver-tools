"""User interface and output formatting"""

import getpass
import sys
from typing import Optional

from .constants import (
    SEPARATOR_LINE,
    MSG_AUTH_REQUIRED,
    MSG_PASSWORD_NOT_SAVED,
    MSG_TOKEN_SAVED,
    MSG_2FA_PROMPT,
    PROMPT_USERNAME,
    PROMPT_PASSWORD,
    PROMPT_2FA_CODE,
    ERR_USERNAME_REQUIRED,
)


class UI:
    """User interface handler"""
    
    @staticmethod
    def print_separator() -> None:
        """Print separator line"""
        print(SEPARATOR_LINE)
    
    @staticmethod
    def print_header(title: str) -> None:
        """Print formatted header"""
        UI.print_separator()
        print(title)
        UI.print_separator()
    
    @staticmethod
    def print_success(message: str) -> None:
        """Print success message with checkmark"""
        print(f"✓ {message}")
    
    @staticmethod
    def print_error(message: str) -> None:
        """Print error message with cross"""
        print(f"✗ Error: {message}")
    
    @staticmethod
    def print_warning(message: str) -> None:
        """Print warning message"""
        print(f"⚠  {message}")
    
    @staticmethod
    def print_info(message: str) -> None:
        """Print info message"""
        print(message)
    
    @staticmethod
    def get_username_input() -> str:
        """
        Get username from user input
        
        Returns:
            Username string
            
        Raises:
            SystemExit: If username is empty
        """
        username = input(PROMPT_USERNAME).strip()
        if not username:
            UI.print_error(ERR_USERNAME_REQUIRED)
            sys.exit(1)
        return username
    
    @staticmethod
    def get_password_input(username: str) -> str:
        """
        Get password from user input (secure)
        
        Args:
            username: Username for prompt
            
        Returns:
            Password string
        """
        return getpass.getpass(PROMPT_PASSWORD.format(username=username))
    
    @staticmethod
    def get_2fa_code_input() -> str:
        """
        Get 2FA code from user input
        
        Returns:
            2FA code string
        """
        UI.print_info(f"\n{MSG_2FA_PROMPT}")
        return input(PROMPT_2FA_CODE).strip()
    
    @staticmethod
    def show_auth_notice() -> None:
        """Display authentication security notice"""
        print()
        UI.print_separator()
        print(MSG_AUTH_REQUIRED)
        UI.print_separator()
        print(MSG_PASSWORD_NOT_SAVED)
        print(MSG_TOKEN_SAVED)
        UI.print_separator()
        print()
    
    @staticmethod
    def show_download_progress(current: int, title: str) -> None:
        """
        Show download progress
        
        Args:
            current: Current item number
            title: Title of current item
        """
        print(f"\n[{current}] Downloading: {title}")
    
    @staticmethod
    def show_item_progress(item_num: int, success: bool, error: Optional[str] = None) -> None:
        """
        Show individual item download status
        
        Args:
            item_num: Item number
            success: Whether download succeeded
            error: Optional error message
        """
        if success:
            print(f"  ✓ Item {item_num} downloaded")
        else:
            error_msg = f": {error}" if error else ""
            print(f"  ✗ Error downloading item {item_num}{error_msg}")
    
    @staticmethod
    def show_summary(count: int, item_type: str, location: Optional[str] = None) -> None:
        """
        Show download summary
        
        Args:
            count: Number of items
            item_type: Type of items (e.g., "highlights")
            location: Optional location path
        """
        if count == 0:
            print(f"\nNo {item_type} found")
        else:
            print(f"\n✓ Completed: {count} {item_type} downloaded")
            if location:
                print(f"Location: {location}")
