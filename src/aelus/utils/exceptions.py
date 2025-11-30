"""Custom exceptions for Aelus application.

This module defines the exception hierarchy used throughout the Aelus
application for error handling and reporting.
"""


class AelusError(Exception):
    """Base exception for Aelus application.

    All custom exceptions in Aelus should inherit from this class
    to allow for consistent exception handling.
    """


# Alias for backwards compatibility
AelusException = AelusError


class FileOperationError(AelusError):
    """Raised when file operations fail.

    This exception indicates errors during file reading, writing,
    or other filesystem operations.

    Attributes:
        message: Description of the error.
        path: Path to the file that caused the error.
    """

    def __init__(self, message: str, path: str | None = None) -> None:
        """Initialize FileOperationError.

        Args:
            message: Description of the error.
            path: Optional path to the file that caused the error.
        """
        self.path = path
        super().__init__(message)


class InvalidALSFileError(AelusError):
    """Raised when an ALS file is invalid or corrupted.

    This exception indicates that a file could not be parsed as a
    valid Ableton Live Set file.
    """


class ParseError(AelusError):
    """Raised when parsing fails.

    This exception indicates general parsing errors that are not
    specific to invalid file format.
    """


class ParserNotFoundError(AelusError):
    """Raised when a requested parser is not available.

    This exception indicates that the specified parser type cannot
    be instantiated, typically because a required library is not installed.
    """
