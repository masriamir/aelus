"""Unit tests for custom ALS parser."""

from pathlib import Path

import pytest

from aelus.parsers.custom import CustomALSParser
from aelus.utils.exceptions import InvalidALSFileError


@pytest.mark.unit
class TestCustomParser:
    """Test custom ALS parser implementation."""

    @pytest.fixture
    def parser(self) -> CustomALSParser:
        """Create parser instance."""
        return CustomALSParser()

    def test_parse_valid_file(
        self, parser: CustomALSParser, sample_als_file: Path
    ) -> None:
        """Test parsing valid ALS file."""
        project = parser.parse(sample_als_file)
        assert project.name == sample_als_file.stem
        assert project.version is not None

    def test_parse_extracts_tempo(
        self, parser: CustomALSParser, sample_als_file: Path
    ) -> None:
        """Test that tempo is extracted correctly."""
        project = parser.parse(sample_als_file)
        assert project.tempo == 120.0

    def test_parse_extracts_tracks(
        self, parser: CustomALSParser, sample_als_file: Path
    ) -> None:
        """Test that tracks are extracted."""
        project = parser.parse(sample_als_file)
        assert len(project.tracks) == 2
        assert project.tracks[0].name == "1-Audio"
        assert project.tracks[0].track_type == "audio"
        assert project.tracks[1].name == "2-MIDI"
        assert project.tracks[1].track_type == "midi"

    def test_parse_extracts_time_signature(
        self, parser: CustomALSParser, sample_als_file: Path
    ) -> None:
        """Test that time signature is extracted."""
        project = parser.parse(sample_als_file)
        assert project.time_signature == (4, 4)

    def test_validate_valid_file(
        self, parser: CustomALSParser, sample_als_file: Path
    ) -> None:
        """Test validation of valid ALS file."""
        assert parser.validate(sample_als_file) is True

    def test_validate_invalid_file(
        self, parser: CustomALSParser, invalid_als_file: Path
    ) -> None:
        """Test validation of invalid file."""
        assert parser.validate(invalid_als_file) is False

    def test_validate_corrupted_file(
        self, parser: CustomALSParser, corrupted_gzip_file: Path
    ) -> None:
        """Test validation of corrupted gzip file."""
        assert parser.validate(corrupted_gzip_file) is False

    def test_parse_nonexistent_file_raises(
        self, parser: CustomALSParser, temp_dir: Path
    ) -> None:
        """Test parsing non-existent file raises exception."""
        nonexistent = temp_dir / "does_not_exist.als"
        with pytest.raises(FileNotFoundError):
            parser.parse(nonexistent)

    def test_parse_invalid_file_raises(
        self, parser: CustomALSParser, invalid_als_file: Path
    ) -> None:
        """Test parsing invalid file raises exception."""
        with pytest.raises(InvalidALSFileError):
            parser.parse(invalid_als_file)

    def test_parse_corrupted_gzip_raises(
        self, parser: CustomALSParser, corrupted_gzip_file: Path
    ) -> None:
        """Test parsing corrupted gzip file raises exception."""
        with pytest.raises(InvalidALSFileError):
            parser.parse(corrupted_gzip_file)


@pytest.mark.unit
@pytest.mark.asyncio
class TestCustomParserAsync:
    """Test async methods of custom parser."""

    @pytest.fixture
    def parser(self) -> CustomALSParser:
        """Create parser instance."""
        return CustomALSParser()

    async def test_parse_async(
        self, parser: CustomALSParser, sample_als_file: Path
    ) -> None:
        """Test async parsing."""
        project = await parser.parse_async(sample_als_file)
        assert project.name == sample_als_file.stem
        assert project.tempo == 120.0
