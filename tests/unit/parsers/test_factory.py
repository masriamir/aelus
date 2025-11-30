"""Unit tests for parser factory."""

import pytest

from aelus.parsers import ParserType, get_parser
from aelus.parsers.custom import CustomALSParser
from aelus.utils.exceptions import ParserNotFoundError


@pytest.mark.unit
class TestParserFactory:
    """Test parser factory functions."""

    def test_get_parser_custom(self) -> None:
        """Test getting custom parser explicitly."""
        # Clear the cache to ensure fresh parser
        get_parser.cache_clear()
        parser = get_parser(ParserType.CUSTOM)
        assert isinstance(parser, CustomALSParser)

    def test_get_parser_auto_returns_custom(self) -> None:
        """Test auto parser falls back to custom when third-party unavailable."""
        get_parser.cache_clear()
        parser = get_parser(ParserType.AUTO)
        # Should fall back to custom parser since third-party is not available
        assert isinstance(parser, CustomALSParser)

    def test_get_parser_third_party_raises(self) -> None:
        """Test third-party parser raises when not installed."""
        get_parser.cache_clear()
        with pytest.raises(ParserNotFoundError):
            get_parser(ParserType.THIRD_PARTY)

    def test_get_parser_invalid_type(self) -> None:
        """Test invalid parser type raises ValueError."""
        get_parser.cache_clear()
        with pytest.raises(ValueError, match="Unknown parser type"):
            get_parser("invalid")  # type: ignore[arg-type]

    def test_get_parser_caching(self) -> None:
        """Test parser instances are cached."""
        get_parser.cache_clear()
        parser1 = get_parser(ParserType.CUSTOM)
        parser2 = get_parser(ParserType.CUSTOM)
        assert parser1 is parser2
