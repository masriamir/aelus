"""Unit tests for file I/O utilities."""

import gzip
from pathlib import Path

import pytest

from aelus.utils.exceptions import FileOperationError
from aelus.utils.file_io import list_als_files, read_gzipped_file


@pytest.mark.unit
class TestReadGzippedFile:
    """Test gzipped file reading."""

    def test_read_valid_gzip(self, temp_dir: Path) -> None:
        """Test reading valid gzipped file."""
        content = b"test content"
        gz_path = temp_dir / "test.gz"
        with gzip.open(gz_path, "wb") as f:
            f.write(content)

        result = read_gzipped_file(gz_path)
        assert result == content

    def test_read_nonexistent_file_raises(self, temp_dir: Path) -> None:
        """Test reading non-existent file raises error."""
        nonexistent = temp_dir / "does_not_exist.gz"
        with pytest.raises(FileOperationError):
            read_gzipped_file(nonexistent)

    def test_read_invalid_gzip_raises(self, temp_dir: Path) -> None:
        """Test reading invalid gzip file raises error."""
        invalid_path = temp_dir / "invalid.gz"
        invalid_path.write_text("not a gzip file")
        with pytest.raises(FileOperationError):
            read_gzipped_file(invalid_path)


@pytest.mark.unit
class TestListALSFiles:
    """Test ALS file listing."""

    def test_list_als_files_empty(self, temp_dir: Path) -> None:
        """Test listing files in empty directory."""
        files = list(list_als_files(temp_dir))
        assert files == []

    def test_list_als_files_finds_files(self, temp_dir: Path) -> None:
        """Test listing finds .als files."""
        # Create some test files
        (temp_dir / "project1.als").touch()
        (temp_dir / "project2.als").touch()
        (temp_dir / "other.txt").touch()

        files = list(list_als_files(temp_dir))
        assert len(files) == 2
        file_names = [f.name for f in files]
        assert "project1.als" in file_names
        assert "project2.als" in file_names
        assert "other.txt" not in file_names

    def test_list_als_files_recursive(self, temp_dir: Path) -> None:
        """Test listing finds files in subdirectories."""
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        (temp_dir / "project1.als").touch()
        (subdir / "project2.als").touch()

        files = list(list_als_files(temp_dir))
        assert len(files) == 2

    def test_list_als_files_nonexistent_dir_raises(self, temp_dir: Path) -> None:
        """Test listing non-existent directory raises error."""
        nonexistent = temp_dir / "does_not_exist"
        with pytest.raises(FileOperationError):
            list(list_als_files(nonexistent))

    def test_list_als_files_not_a_dir_raises(self, temp_dir: Path) -> None:
        """Test listing a file instead of directory raises error."""
        file_path = temp_dir / "file.txt"
        file_path.touch()
        with pytest.raises(FileOperationError):
            list(list_als_files(file_path))


@pytest.mark.unit
@pytest.mark.asyncio
class TestAsyncFileIO:
    """Test async file I/O functions."""

    async def test_read_gzipped_file_async(self, temp_dir: Path) -> None:
        """Test async gzipped file reading."""
        from aelus.utils.file_io import read_gzipped_file_async

        content = b"async test content"
        gz_path = temp_dir / "async_test.gz"
        with gzip.open(gz_path, "wb") as f:
            f.write(content)

        result = await read_gzipped_file_async(gz_path)
        assert result == content

    async def test_list_als_files_async(self, temp_dir: Path) -> None:
        """Test async ALS file listing."""
        from aelus.utils.file_io import list_als_files_async

        (temp_dir / "project1.als").touch()
        (temp_dir / "project2.als").touch()

        files = []
        async for file in list_als_files_async(temp_dir):
            files.append(file)

        assert len(files) == 2
