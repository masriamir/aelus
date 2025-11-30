"""Pytest configuration and fixtures for Aelus tests.

This module provides shared fixtures and configuration for all tests,
including test clients, mock data, and temporary file management.
"""

import gzip
from collections.abc import Generator
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from fastapi.testclient import TestClient

from aelus.api.app import create_app
from aelus.core.config import Settings
from aelus.parsers.base import ALSProject, ALSTrack


@pytest.fixture
def test_settings() -> Settings:
    """Create test settings with overrides.

    Returns settings configured for testing without rate limiting
    to avoid middleware issues in tests.
    """
    return Settings(
        debug=True,
        rate_limit_enabled=False,  # Disabled for most tests
    )


@pytest.fixture
def test_settings_no_rate_limit() -> Settings:
    """Create test settings without rate limiting."""
    return Settings(
        debug=True,
        rate_limit_enabled=False,
    )


@pytest.fixture
def test_app(test_settings: Settings):  # type: ignore[no-untyped-def]
    """Create test FastAPI application."""
    return create_app(test_settings)


@pytest.fixture
def test_app_no_rate_limit(test_settings_no_rate_limit: Settings):  # type: ignore[no-untyped-def]
    """Create test FastAPI application without rate limiting."""
    return create_app(test_settings_no_rate_limit)


@pytest.fixture
def client(test_app) -> Generator[TestClient]:  # type: ignore[no-untyped-def, type-arg]
    """Create test client for sync tests."""
    with TestClient(test_app) as test_client:
        yield test_client


@pytest.fixture
def client_no_rate_limit(test_app_no_rate_limit) -> Generator[TestClient]:  # type: ignore[no-untyped-def, type-arg]
    """Create test client without rate limiting."""
    with TestClient(test_app_no_rate_limit) as test_client:
        yield test_client


@pytest.fixture
def temp_dir() -> Generator[Path]:
    """Create temporary directory for tests."""
    with TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_als_file(temp_dir: Path) -> Path:
    """Create a sample .als file for testing.

    Creates a minimal valid gzipped XML file simulating an
    Ableton Live Set structure.
    """
    xml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
<Ableton Creator="Ableton Live 11.0.0" MajorVersion="5" MinorVersion="11.0">
    <LiveSet>
        <Tempo>
            <Manual Value="120"/>
        </Tempo>
        <TimeSignature>
            <TimeSignatures>
                <RemoteableTimeSignature>
                    <Numerator Value="4"/>
                    <Denominator Value="4"/>
                </RemoteableTimeSignature>
            </TimeSignatures>
        </TimeSignature>
        <Tracks>
            <AudioTrack Id="0">
                <Name>
                    <EffectiveName Value="1-Audio"/>
                    <UserName Value=""/>
                </Name>
                <ColorIndex Value="5"/>
                <Freeze Value="false"/>
            </AudioTrack>
            <MidiTrack Id="1">
                <Name>
                    <EffectiveName Value="2-MIDI"/>
                    <UserName Value=""/>
                </Name>
                <ColorIndex Value="10"/>
                <Freeze Value="false"/>
            </MidiTrack>
        </Tracks>
    </LiveSet>
</Ableton>"""
    als_path = temp_dir / "test.als"
    with gzip.open(als_path, "wb") as f:
        f.write(xml_content)
    return als_path


@pytest.fixture
def invalid_als_file(temp_dir: Path) -> Path:
    """Create an invalid .als file (not gzipped)."""
    invalid_path = temp_dir / "invalid.als"
    invalid_path.write_text("This is not a valid ALS file")
    return invalid_path


@pytest.fixture
def corrupted_gzip_file(temp_dir: Path) -> Path:
    """Create a corrupted gzip file."""
    corrupted_path = temp_dir / "corrupted.als"
    corrupted_path.write_bytes(b"\x1f\x8b\x08\x00invalid")
    return corrupted_path


@pytest.fixture
def mock_als_project() -> ALSProject:
    """Create mock ALS project data."""
    return ALSProject(
        name="Test Project",
        version="11.0.0",
        tempo=120.0,
        time_signature=(4, 4),
        tracks=[
            ALSTrack(name="1-Audio", track_type="audio"),
            ALSTrack(name="2-MIDI", track_type="midi"),
        ],
    )
