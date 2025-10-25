"""Application constants"""

from pathlib import Path

# Application info
APP_NAME = "IGsaver"
APP_DESCRIPTION = "Instagram Highlights Backup Tool"

# Directory structure
ROOT_DIR = Path(__file__).parent.parent
BACKUPS_DIR = ROOT_DIR / "backups"
SESSIONS_DIR = ROOT_DIR / ".sessions"
LOGS_DIR = ROOT_DIR / "logs"

# UI formatting
SEPARATOR_LINE = "=" * 50
SEPARATOR_CHAR = "="
SEPARATOR_LENGTH = 50

# Session configuration
SESSION_FILE_PREFIX = "session-"

# Download configuration
DOWNLOAD_VIDEOS = True
DOWNLOAD_VIDEO_THUMBNAILS = False
DOWNLOAD_GEOTAGS = True
DOWNLOAD_COMMENTS = False
SAVE_METADATA = True
COMPRESS_JSON = False

# Messages
MSG_AUTH_REQUIRED = "AUTHENTICATION REQUIRED"
MSG_PASSWORD_NOT_SAVED = "Your password will NOT be saved to any file."
MSG_TOKEN_SAVED = "Only a temporary session token will be stored."
MSG_SESSION_LOADED = "Session loaded successfully"
MSG_SESSION_EXPIRED = "Session has expired, new authentication required"
MSG_LOGIN_SUCCESS = "Session started and saved successfully"
MSG_NO_PASSWORD_REQUIRED = "Future runs won't require password entry"
MSG_BACKUP_COMPLETED = "Backup completed"
MSG_2FA_PROMPT = "Two-factor authentication detected"

# Error messages
ERR_USERNAME_REQUIRED = "Username is required"
ERR_PASSWORD_EMPTY = "Password cannot be empty"
ERR_INVALID_CREDENTIALS = "Invalid credentials"
ERR_2FA_REQUIRED = "Two-factor authentication is required"
ERR_2FA_HINT = "Please temporarily disable 2FA or configure backup codes"
ERR_PROFILE_NOT_FOUND = "Profile does not exist"
ERR_PRIVATE_PROFILE = "is a private account and you don't follow them"

# Prompts
PROMPT_USERNAME = "Instagram username: "
PROMPT_PASSWORD = "Password for {username}: "
PROMPT_2FA_CODE = "Enter 2FA code: "

# Log configuration
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
