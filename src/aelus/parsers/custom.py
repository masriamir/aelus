"""Custom ALS file parser implementation.

This module provides a custom implementation for parsing Ableton Live Set
files using Python's built-in XML parsing capabilities.
"""

import asyncio
import logging
import xml.etree.ElementTree as ET
from pathlib import Path

import defusedxml.ElementTree as DefusedET

from aelus.parsers.base import ALSProject, ALSTrack, BaseALSParser
from aelus.utils.exceptions import FileOperationError, InvalidALSFileError
from aelus.utils.file_io import read_gzipped_file

logger = logging.getLogger(__name__)


class CustomALSParser(BaseALSParser):
    """Custom implementation of ALS file parser.

    This parser uses Python's built-in gzip and xml modules to parse
    Ableton Live Set files without external dependencies.
    """

    def parse(self, file_path: Path) -> ALSProject:
        """Parse ALS file using custom XML parsing logic.

        Reads, decompresses, and parses an Ableton Live Set file,
        extracting project metadata, tracks, samples, and plugins.

        Args:
            file_path: Path to the .als file.

        Returns:
            Parsed ALS project data.

        Raises:
            FileNotFoundError: If the file does not exist.
            InvalidALSFileError: If file cannot be parsed.

        Examples:
            >>> from pathlib import Path
            >>> parser = CustomALSParser()
            >>> # project = parser.parse(Path("my_project.als"))
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        logger.debug("Parsing ALS file: %s", file_path)

        try:
            content = read_gzipped_file(file_path)
        except FileOperationError as e:
            raise InvalidALSFileError(f"Failed to read file: {e}") from e

        try:
            root = DefusedET.fromstring(content)
        except ET.ParseError as e:
            raise InvalidALSFileError(f"Failed to parse XML: {e}") from e

        return self._extract_project_data(root, file_path)

    async def parse_async(self, file_path: Path) -> ALSProject:
        """Async version of parse.

        Runs the synchronous parse method in a thread pool executor
        to avoid blocking the event loop.

        Args:
            file_path: Path to the .als file.

        Returns:
            Parsed ALS project data.

        Raises:
            FileNotFoundError: If the file does not exist.
            InvalidALSFileError: If file cannot be parsed.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.parse, file_path)

    def validate(self, file_path: Path) -> bool:
        """Check if file is a valid ALS format.

        Attempts to read and parse the file to verify it contains
        valid Ableton Live Set data.

        Args:
            file_path: Path to the file to validate.

        Returns:
            True if the file appears to be a valid ALS file.

        Examples:
            >>> from pathlib import Path
            >>> parser = CustomALSParser()
            >>> # is_valid = parser.validate(Path("project.als"))
        """
        try:
            content = read_gzipped_file(file_path)
            root = DefusedET.fromstring(content)
            return root.tag == "Ableton"
        except Exception:
            return False

    def _extract_project_data(self, root: ET.Element, file_path: Path) -> ALSProject:
        """Extract project data from XML root element.

        Parses the XML structure to extract all project metadata.

        Args:
            root: Root XML element of the ALS file.
            file_path: Original file path for deriving project name.

        Returns:
            Populated ALSProject instance.
        """
        # Verify root element
        if root.tag != "Ableton":
            raise InvalidALSFileError("Root element is not 'Ableton'")

        # Extract version info
        version = root.get("Creator", "Unknown")
        major_version = root.get("MajorVersion", "")
        minor_version = root.get("MinorVersion", "")

        if major_version and minor_version:
            version_str = f"{major_version}.{minor_version}"
        else:
            version_str = version

        # Extract tempo
        tempo = self._extract_tempo(root)

        # Extract time signature
        time_signature = self._extract_time_signature(root)

        # Extract tracks
        tracks = self._extract_tracks(root)

        # Extract samples
        samples = self._extract_samples(root)

        # Extract plugins
        plugins = self._extract_plugins(root)

        return ALSProject(
            name=file_path.stem,
            version=version_str,
            creator=version,
            tempo=tempo,
            time_signature=time_signature,
            tracks=tracks,
            samples=samples,
            plugins=plugins,
        )

    def _extract_tempo(self, root: ET.Element) -> float:
        """Extract tempo from the Live Set.

        Args:
            root: Root XML element.

        Returns:
            Project tempo in BPM, defaults to 120.0.
        """
        # Navigate to Tempo element
        # LiveSet -> MasterTrack -> DeviceChain -> Mixer -> Tempo
        live_set = root.find(".//LiveSet")
        if live_set is None:
            return 120.0

        # Try to find tempo in various locations
        tempo_elem = live_set.find(".//Tempo/Manual")
        if tempo_elem is not None:
            value = tempo_elem.get("Value")
            if value:
                try:
                    return float(value)
                except ValueError:
                    pass

        return 120.0

    def _extract_time_signature(self, root: ET.Element) -> tuple[int, int]:
        """Extract time signature from the Live Set.

        Args:
            root: Root XML element.

        Returns:
            Tuple of (numerator, denominator), defaults to (4, 4).
        """
        live_set = root.find(".//LiveSet")
        if live_set is None:
            return (4, 4)

        # Try to find time signature
        numerator = 4
        denominator = 4

        num_elem = live_set.find(
            ".//TimeSignature/TimeSignatures/RemoteableTimeSignature/Numerator"
        )
        if num_elem is not None:
            value = num_elem.get("Value")
            if value:
                try:
                    numerator = int(value)
                except ValueError:
                    pass

        denom_elem = live_set.find(
            ".//TimeSignature/TimeSignatures/RemoteableTimeSignature/Denominator"
        )
        if denom_elem is not None:
            value = denom_elem.get("Value")
            if value:
                try:
                    denominator = int(value)
                except ValueError:
                    pass

        return (numerator, denominator)

    def _extract_tracks(self, root: ET.Element) -> list[ALSTrack]:
        """Extract track information from the Live Set.

        Args:
            root: Root XML element.

        Returns:
            List of ALSTrack objects.
        """
        tracks: list[ALSTrack] = []
        live_set = root.find(".//LiveSet")
        if live_set is None:
            return tracks

        # Find all track types
        track_elements = live_set.findall(".//Tracks/*")

        for track_elem in track_elements:
            track_type = self._get_track_type(track_elem.tag)
            name = self._get_track_name(track_elem)
            color = self._get_track_color(track_elem)
            is_frozen = self._get_track_frozen(track_elem)

            tracks.append(
                ALSTrack(
                    name=name,
                    track_type=track_type,
                    color=color,
                    is_frozen=is_frozen,
                )
            )

        return tracks

    def _get_track_type(self, tag: str) -> str:
        """Determine track type from XML tag name.

        Args:
            tag: XML element tag name.

        Returns:
            Track type string.
        """
        if "Audio" in tag:
            return "audio"
        elif "Midi" in tag:
            return "midi"
        elif "Return" in tag:
            return "return"
        elif "Group" in tag:
            return "group"
        else:
            return "unknown"

    def _get_track_name(self, track_elem: ET.Element) -> str:
        """Extract track name from track element.

        Args:
            track_elem: Track XML element.

        Returns:
            Track name or default.
        """
        name_elem = track_elem.find(".//Name/EffectiveName")
        if name_elem is not None:
            value = name_elem.get("Value")
            if value:
                return value

        name_elem = track_elem.find(".//Name/UserName")
        if name_elem is not None:
            value = name_elem.get("Value")
            if value:
                return value

        return "Untitled Track"

    def _get_track_color(self, track_elem: ET.Element) -> int | None:
        """Extract track color index from track element.

        Args:
            track_elem: Track XML element.

        Returns:
            Color index or None.
        """
        color_elem = track_elem.find(".//ColorIndex")
        if color_elem is not None:
            value = color_elem.get("Value")
            if value:
                try:
                    return int(value)
                except ValueError:
                    pass
        return None

    def _get_track_frozen(self, track_elem: ET.Element) -> bool:
        """Check if track is frozen.

        Args:
            track_elem: Track XML element.

        Returns:
            True if track is frozen.
        """
        freeze_elem = track_elem.find(".//Freeze")
        if freeze_elem is not None:
            value = freeze_elem.get("Value")
            return value == "true"
        return False

    def _extract_samples(self, root: ET.Element) -> list[str]:
        """Extract sample file references from the Live Set.

        Args:
            root: Root XML element.

        Returns:
            List of sample file paths.
        """
        samples: list[str] = []
        seen: set[str] = set()

        # Find all file references
        for file_ref in root.findall(".//FileRef"):
            path_elem = file_ref.find("Path")
            if path_elem is not None:
                value = path_elem.get("Value")
                if value and value not in seen:
                    samples.append(value)
                    seen.add(value)

            name_elem = file_ref.find("Name")
            if name_elem is not None:
                value = name_elem.get("Value")
                if value and value not in seen:
                    samples.append(value)
                    seen.add(value)

        return samples

    def _extract_plugins(self, root: ET.Element) -> list[str]:
        """Extract plugin names from the Live Set.

        Args:
            root: Root XML element.

        Returns:
            List of unique plugin names.
        """
        plugins: list[str] = []
        seen: set[str] = set()

        # Find VST plugins
        for plugin in root.findall(".//PluginDesc/VstPluginInfo/PlugName"):
            value = plugin.get("Value")
            if value and value not in seen:
                plugins.append(value)
                seen.add(value)

        # Find AU plugins
        for plugin in root.findall(".//PluginDesc/AuPluginInfo/Name"):
            value = plugin.get("Value")
            if value and value not in seen:
                plugins.append(value)
                seen.add(value)

        return plugins
