"""File I/O utilities for Aelus.

This module provides utilities for reading and processing files,
with special support for Ableton Live Set (.als) files which are
gzip-compressed XML documents.
"""

import asyncio
import gzip
import logging
from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING

import aiofiles

from aelus.utils.exceptions import FileOperationError

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

logger = logging.getLogger(__name__)


async def read_file_async(path: Path) -> bytes:
    """Read file contents asynchronously.

    Args:
        path: Path to the file to read.

    Returns:
        Raw bytes content of the file.

    Raises:
        FileOperationError: If the file cannot be read.

    Examples:
        >>> import asyncio
        >>> from pathlib import Path
        >>> # content = asyncio.run(read_file_async(Path("test.txt")))
    """
    try:
        async with aiofiles.open(path, "rb") as f:
            return await f.read()
    except OSError as e:
        raise FileOperationError(f"Failed to read file: {e}", str(path)) from e


def read_gzipped_file(path: Path) -> bytes:
    """Read and decompress a gzipped file.

    Ableton Live Set (.als) files are gzip-compressed XML documents.
    This function reads and decompresses such files.

    Args:
        path: Path to the gzipped file.

    Returns:
        Decompressed content as bytes.

    Raises:
        FileOperationError: If the file cannot be read or decompressed.

    Examples:
        >>> from pathlib import Path
        >>> # content = read_gzipped_file(Path("project.als"))
    """
    if not path.exists():
        raise FileOperationError(f"File not found: {path}", str(path))

    try:
        with gzip.open(path, "rb") as f:
            return f.read()
    except gzip.BadGzipFile as e:
        raise FileOperationError(f"Invalid gzip file: {e}", str(path)) from e
    except EOFError as e:
        raise FileOperationError(f"Truncated gzip file: {e}", str(path)) from e
    except OSError as e:
        raise FileOperationError(f"Failed to read file: {e}", str(path)) from e


async def read_gzipped_file_async(path: Path) -> bytes:
    """Read and decompress a gzipped file asynchronously.

    Performs the gzip decompression in a thread pool to avoid
    blocking the event loop.

    Args:
        path: Path to the gzipped file.

    Returns:
        Decompressed content as bytes.

    Raises:
        FileOperationError: If the file cannot be read or decompressed.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, read_gzipped_file, path)


def list_als_files(directory: Path) -> Iterator[Path]:
    """List all .als files in a directory recursively.

    Searches the given directory and all subdirectories for files
    with the .als extension.

    Args:
        directory: Root directory to search.

    Returns:
        Iterator of Path objects for each .als file found.

    Raises:
        FileOperationError: If the directory cannot be accessed.

    Examples:
        >>> from pathlib import Path
        >>> # for als_file in list_als_files(Path("projects")):
        >>> #     print(als_file)
    """
    if not directory.exists():
        raise FileOperationError(f"Directory not found: {directory}", str(directory))

    if not directory.is_dir():
        raise FileOperationError(f"Not a directory: {directory}", str(directory))

    return directory.rglob("*.als")


async def list_als_files_async(directory: Path) -> "AsyncIterator[Path]":
    """List all .als files in a directory asynchronously.

    Performs directory listing in a thread pool to avoid blocking
    the event loop for large directories.

    Args:
        directory: Root directory to search.

    Yields:
        Path objects for each .als file found.

    Raises:
        FileOperationError: If the directory cannot be accessed.
    """
    loop = asyncio.get_event_loop()
    files = await loop.run_in_executor(None, lambda: list(list_als_files(directory)))
    for file in files:
        yield file
