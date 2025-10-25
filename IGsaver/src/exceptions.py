"""Custom exceptions for IGsaver"""


class IGSaverException(Exception):
    """Base exception for all IGsaver errors"""
    pass


class AuthenticationError(IGSaverException):
    """Raised when authentication fails"""
    pass


class SessionError(IGSaverException):
    """Raised when session operations fail"""
    pass


class DownloadError(IGSaverException):
    """Raised when download operations fail"""
    pass


class ProfileError(IGSaverException):
    """Raised when profile operations fail"""
    pass


class ConfigurationError(IGSaverException):
    """Raised when configuration is invalid"""
    pass
