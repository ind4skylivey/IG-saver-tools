"""Authentication management"""

import logging
from pathlib import Path
from typing import Optional
import instaloader

from .config import Config
from .ui import UI
from .exceptions import AuthenticationError, SessionError
from .constants import (
    SESSION_FILE_PREFIX,
    MSG_SESSION_LOADED,
    MSG_SESSION_EXPIRED,
    MSG_LOGIN_SUCCESS,
    MSG_NO_PASSWORD_REQUIRED,
    ERR_PASSWORD_EMPTY,
    ERR_INVALID_CREDENTIALS,
    ERR_2FA_REQUIRED,
    ERR_2FA_HINT,
)


class Authenticator:
    """Handle Instagram authentication and session management"""
    
    def __init__(self, config: Config, loader: instaloader.Instaloader) -> None:
        """
        Initialize authenticator
        
        Args:
            config: Application configuration
            loader: Instaloader instance
        """
        self.config = config
        self.loader = loader
        self.logger = logging.getLogger(__name__)
        self.username: Optional[str] = None
    
    def authenticate(self) -> str:
        """
        Complete authentication flow
        
        Returns:
            Authenticated username
            
        Raises:
            AuthenticationError: If authentication fails
        """
        self.username = self._get_username()
        
        # Try to load existing session
        if self._session_exists(self.username):
            if self._load_session(self.username):
                if self._verify_session():
                    self.logger.info(f"Authenticated as {self.username} using saved session")
                    return self.username
                else:
                    UI.print_warning(MSG_SESSION_EXPIRED)
        
        # Fallback: interactive login
        self._login_with_password(self.username)
        return self.username
    
    def _get_username(self) -> str:
        """
        Get username from config or user input
        
        Returns:
            Username string
        """
        if self.config.username:
            return self.config.username
        
        return UI.get_username_input()
    
    def _session_exists(self, username: str) -> bool:
        """
        Check if session file exists
        
        Args:
            username: Username to check
            
        Returns:
            True if session exists
        """
        session_file = self._get_session_path(username)
        return session_file.exists()
    
    def _get_session_path(self, username: str) -> Path:
        """
        Get session file path for username
        
        Args:
            username: Username
            
        Returns:
            Path to session file
        """
        return self.config.session_dir / f"{SESSION_FILE_PREFIX}{username}"
    
    def _load_session(self, username: str) -> bool:
        """
        Load existing session from file
        
        Args:
            username: Username to load session for
            
        Returns:
            True if session loaded successfully
        """
        try:
            UI.print_info(f"Loading saved session for {username}...")
            session_path = self._get_session_path(username)
            self.loader.load_session_from_file(username, str(session_path))
            UI.print_success(MSG_SESSION_LOADED)
            self.logger.info(f"Session loaded for {username}")
            return True
        except Exception as e:
            self.logger.warning(f"Could not load session: {e}")
            UI.print_warning(f"Could not load session: {e}")
            return False
    
    def _verify_session(self) -> bool:
        """
        Verify that loaded session is valid
        
        Returns:
            True if session is valid
        """
        try:
            self.loader.test_login()
            return True
        except Exception as e:
            self.logger.warning(f"Session validation failed: {e}")
            return False
    
    def _login_with_2fa(self, username: str, password: str) -> None:
        """
        Handle 2FA authentication
        
        Args:
            username: Username
            password: Password (already entered)
            
        Raises:
            AuthenticationError: If 2FA fails
        """
        two_factor_code = UI.get_2fa_code_input()
        
        if not two_factor_code:
            raise AuthenticationError("2FA code cannot be empty")
        
        try:
            UI.print_info(f"Authenticating with 2FA code...")
            self.loader.two_factor_login(two_factor_code)
            
            # Save session for future use
            session_path = self._get_session_path(username)
            self.loader.save_session_to_file(str(session_path))
            
            UI.print_success(MSG_LOGIN_SUCCESS)
            UI.print_success(MSG_NO_PASSWORD_REQUIRED)
            print()
            
            self.logger.info(f"Successfully logged in as {username} with 2FA")
            
        except instaloader.exceptions.BadCredentialsException:
            raise AuthenticationError("Invalid 2FA code")
        except Exception as e:
            raise AuthenticationError(f"2FA error: {e}")
    
    def _login_with_password(self, username: str) -> None:
        """
        Perform interactive login with password
        
        Args:
            username: Username to login with
            
        Raises:
            AuthenticationError: If login fails
        """
        UI.show_auth_notice()
        
        password = UI.get_password_input(username)
        
        if not password:
            raise AuthenticationError(ERR_PASSWORD_EMPTY)
        
        try:
            UI.print_info(f"\nLogging in as {username}...")
            self.loader.login(username, password)
            
            # Save session for future use
            session_path = self._get_session_path(username)
            self.loader.save_session_to_file(str(session_path))
            
            UI.print_success(MSG_LOGIN_SUCCESS)
            UI.print_success(MSG_NO_PASSWORD_REQUIRED)
            print()
            
            self.logger.info(f"Successfully logged in as {username}")
            
        except instaloader.exceptions.BadCredentialsException:
            self.logger.error(f"Invalid credentials for {username}")
            raise AuthenticationError(ERR_INVALID_CREDENTIALS)
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            self.logger.info(f"2FA required for {username}, requesting code")
            # Try 2FA login
            try:
                self._login_with_2fa(username, password)
            except Exception as e:
                self.logger.error(f"2FA login failed: {e}")
                raise AuthenticationError(f"2FA authentication failed: {e}")
        except Exception as e:
            self.logger.error(f"Login error: {e}")
            raise AuthenticationError(f"Login error: {e}")
