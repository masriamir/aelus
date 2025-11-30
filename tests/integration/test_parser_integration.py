"""Integration tests for parser functionality."""

from pathlib import Path

import pytest

from aelus.parsers import ParserType, get_parser


@pytest.mark.integration
class TestParserIntegration:
    """Test parser integration with file I/O."""

    def test_parse_and_validate_workflow(self, sample_als_file: Path) -> None:
        """Test complete parse and validate workflow."""
        get_parser.cache_clear()
        parser = get_parser(ParserType.AUTO)

        # First validate
        is_valid = parser.validate(sample_als_file)
        assert is_valid is True

        # Then parse
        project = parser.parse(sample_als_file)
        assert project.name is not None
        assert project.tempo > 0

    def test_invalid_file_workflow(self, invalid_als_file: Path) -> None:
        """Test workflow with invalid file."""
        get_parser.cache_clear()
        parser = get_parser(ParserType.AUTO)

        # Validation should fail
        is_valid = parser.validate(invalid_als_file)
        assert is_valid is False

    def test_parse_multiple_files(self, temp_dir: Path, sample_als_file: Path) -> None:
        """Test parsing multiple files."""
        import shutil

        # Create another sample file
        sample2 = temp_dir / "project2.als"
        shutil.copy(sample_als_file, sample2)

        get_parser.cache_clear()
        parser = get_parser(ParserType.AUTO)

        project1 = parser.parse(sample_als_file)
        project2 = parser.parse(sample2)

        assert project1.tempo == project2.tempo


@pytest.mark.integration
@pytest.mark.asyncio
class TestParserAsyncIntegration:
    """Test async parser integration."""

    async def test_async_parse_workflow(self, sample_als_file: Path) -> None:
        """Test async parsing workflow."""
        get_parser.cache_clear()
        parser = get_parser(ParserType.AUTO)

        project = await parser.parse_async(sample_als_file)
        assert project.name == sample_als_file.stem
        assert project.tempo == 120.0
