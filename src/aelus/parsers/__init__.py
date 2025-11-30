"""Parser modules for Ableton Live Set files.

This package provides a pluggable architecture for parsing .als files,
supporting both custom implementations and third-party libraries.
"""

from enum import Enum
from functools import cache

from aelus.parsers.base import ALSProject, ALSTrack, BaseALSParser
from aelus.parsers.custom import CustomALSParser
from aelus.utils.exceptions import ParserNotFoundError

__all__ = [
    "ALSProject",
    "ALSTrack",
    "BaseALSParser",
    "CustomALSParser",
    "ParserType",
    "get_parser",
]


class ParserType(str, Enum):
    """Available parser types.

    Attributes:
        CUSTOM: Use the built-in custom parser.
        THIRD_PARTY: Use a third-party library wrapper.
        AUTO: Try third-party first, fallback to custom.
    """

    CUSTOM = "custom"
    THIRD_PARTY = "third_party"
    AUTO = "auto"


@cache
def get_parser(parser_type: ParserType = ParserType.AUTO) -> BaseALSParser:
    """Get parser instance based on type.

    Factory function that returns the appropriate parser based on the
    requested type. The AUTO type tries third-party first, then falls
    back to the custom implementation.

    Args:
        parser_type: Type of parser to use.

    Returns:
        Parser instance implementing BaseALSParser.

    Raises:
        ParserNotFoundError: If requested parser is not available.
        ValueError: If an unknown parser type is specified.

    Examples:
        >>> parser = get_parser()
        >>> parser = get_parser(ParserType.CUSTOM)
    """
    if parser_type == ParserType.CUSTOM:
        return CustomALSParser()
    elif parser_type == ParserType.THIRD_PARTY:
        # Third-party parser not currently available
        raise ParserNotFoundError(
            "Third-party parser (python-ableton-live) not installed. "
            "Use ParserType.CUSTOM or ParserType.AUTO instead."
        )
    elif parser_type == ParserType.AUTO:
        # Try third-party first, fall back to custom
        try:
            return get_parser(ParserType.THIRD_PARTY)
        except ParserNotFoundError:
            return CustomALSParser()
    else:
        raise ValueError(f"Unknown parser type: {parser_type}")
