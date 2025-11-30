"""Unit tests for parser base models."""

import pytest

from aelus.parsers.base import ALSProject, ALSTrack


@pytest.mark.unit
class TestALSTrack:
    """Test ALSTrack model."""

    def test_create_track_minimal(self) -> None:
        """Test creating track with minimal fields."""
        track = ALSTrack(name="Test Track", track_type="audio")
        assert track.name == "Test Track"
        assert track.track_type == "audio"
        assert track.color is None
        assert track.is_frozen is False
        assert track.devices == []

    def test_create_track_full(self) -> None:
        """Test creating track with all fields."""
        track = ALSTrack(
            name="Full Track",
            track_type="midi",
            color=5,
            is_frozen=True,
            devices=[{"name": "EQ Eight"}],
        )
        assert track.name == "Full Track"
        assert track.track_type == "midi"
        assert track.color == 5
        assert track.is_frozen is True
        assert len(track.devices) == 1


@pytest.mark.unit
class TestALSProject:
    """Test ALSProject model."""

    def test_create_project_minimal(self) -> None:
        """Test creating project with minimal fields."""
        project = ALSProject(
            name="Test Project",
            version="11.0.0",
            tempo=120.0,
        )
        assert project.name == "Test Project"
        assert project.version == "11.0.0"
        assert project.tempo == 120.0
        assert project.time_signature == (4, 4)
        assert project.tracks == []
        assert project.samples == []
        assert project.plugins == []

    def test_create_project_with_tracks(self) -> None:
        """Test creating project with tracks."""
        tracks = [
            ALSTrack(name="1-Audio", track_type="audio"),
            ALSTrack(name="2-MIDI", track_type="midi"),
        ]
        project = ALSProject(
            name="Test Project",
            version="11.0.0",
            tempo=128.0,
            tracks=tracks,
        )
        assert len(project.tracks) == 2
        assert project.tracks[0].name == "1-Audio"

    def test_project_time_signature(self) -> None:
        """Test project with custom time signature."""
        project = ALSProject(
            name="Test",
            version="11.0.0",
            tempo=120.0,
            time_signature=(6, 8),
        )
        assert project.time_signature == (6, 8)

    def test_project_json_serialization(self) -> None:
        """Test project can be serialized to JSON."""
        project = ALSProject(
            name="Test",
            version="11.0.0",
            tempo=120.0,
        )
        json_data = project.model_dump_json()
        assert "Test" in json_data
        assert "11.0.0" in json_data
