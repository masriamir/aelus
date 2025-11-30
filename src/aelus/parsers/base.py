"""Base parser interface and data models for ALS files.

This module defines the abstract base class for ALS parsers and the
data models used to represent parsed project data.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class ALSTrack(BaseModel):
    """Represents a track in an Ableton Live project.

    Attributes:
        name: Display name of the track.
        track_type: Type of track (audio, midi, return, master).
        color: Color index for the track.
        is_frozen: Whether the track is frozen.
        devices: List of devices on the track.
    """

    name: str = Field(..., description="Display name of the track")
    track_type: str = Field(
        ..., description="Type of track (audio, midi, return, master)"
    )
    color: int | None = Field(default=None, description="Color index for the track")
    is_frozen: bool = Field(default=False, description="Whether the track is frozen")
    devices: list[dict[str, Any]] = Field(
        default_factory=list,
        description="List of devices on the track",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "1-Audio",
                "track_type": "audio",
                "color": 5,
                "is_frozen": False,
                "devices": [],
            }
        }
    }


class ALSProject(BaseModel):
    """Represents an Ableton Live project.

    This model contains all the parsed metadata from an .als file,
    including project settings, tracks, samples, and plugins.

    Attributes:
        name: Project name (typically derived from filename).
        version: Ableton Live version that created the project.
        creator: Creator application identifier.
        tempo: Project tempo in BPM.
        time_signature: Tuple of (numerator, denominator).
        tracks: List of tracks in the project.
        created_at: Project creation timestamp.
        modified_at: Last modification timestamp.
        total_time: Total project length in seconds.
        samples: List of sample file paths referenced.
        plugins: List of plugin names used.
    """

    name: str = Field(..., description="Project name")
    version: str = Field(..., description="Ableton Live version")
    creator: str | None = Field(default=None, description="Creator application")
    tempo: float = Field(..., description="Project tempo in BPM")
    time_signature: tuple[int, int] = Field(
        default=(4, 4),
        description="Time signature (numerator, denominator)",
    )
    tracks: list[ALSTrack] = Field(
        default_factory=list,
        description="List of tracks in the project",
    )
    created_at: datetime | None = Field(
        default=None,
        description="Project creation timestamp",
    )
    modified_at: datetime | None = Field(
        default=None,
        description="Last modification timestamp",
    )
    total_time: float | None = Field(
        default=None,
        description="Total project length in seconds",
    )
    samples: list[str] = Field(
        default_factory=list,
        description="Sample file paths referenced",
    )
    plugins: list[str] = Field(
        default_factory=list,
        description="Plugin names used",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "My Project",
                "version": "11.0.0",
                "tempo": 120.0,
                "time_signature": [4, 4],
                "tracks": [],
            }
        }
    }


class BaseALSParser(ABC):
    """Abstract base class for ALS parsers.

    All ALS parser implementations must inherit from this class and
    implement the required abstract methods.
    """

    @abstractmethod
    def parse(self, file_path: Path) -> ALSProject:
        """Parse an ALS file and return project data.

        Args:
            file_path: Path to the .als file.

        Returns:
            Parsed ALS project data.

        Raises:
            FileNotFoundError: If the file does not exist.
            InvalidALSFileError: If the file cannot be parsed.
        """

    @abstractmethod
    async def parse_async(self, file_path: Path) -> ALSProject:
        """Parse an ALS file asynchronously.

        Args:
            file_path: Path to the .als file.

        Returns:
            Parsed ALS project data.

        Raises:
            FileNotFoundError: If the file does not exist.
            InvalidALSFileError: If the file cannot be parsed.
        """

    @abstractmethod
    def validate(self, file_path: Path) -> bool:
        """Validate if file is a valid ALS file.

        Args:
            file_path: Path to the file to validate.

        Returns:
            True if the file appears to be a valid ALS file.
        """
