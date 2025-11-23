# Copilot Instructions for Aelus

## Project Overview

Aelus is a web-based dashboard for viewing and organizing Ableton Live project files. The project aims to provide an intuitive interface for managing `.als` files, understanding project structure, and organizing audio production workflows.

**Repository:** https://github.com/masriamir/aelus

## Development Standards

### Python Version

- **Target:** Python 3.13+
- Use modern Python features appropriate for Python 3.13
- Type hints are mandatory for all function parameters and return values
- Follow the syntax and features available in Python 3.13

### Code Style

Follow the Ruff configuration defined in `pyproject.toml`:

- **Line length:** 88 characters
- **Quote style:** Double quotes for strings
- **Indentation:** 4 spaces (no tabs)
- **Import organization:** Use isort conventions with `src` as first-party package
- **Docstring format:** Format code blocks in docstrings
- **Trailing whitespace:** Remove all trailing whitespace from all files
- **File endings:** All files must end with a single newline character

#### Enabled Ruff Rules

The project enforces the following linting rules:
- `S` - flake8-bandit (security)
- `B` - flake8-bugbear (bug detection)
- `A` - flake8-builtins (avoid shadowing builtins)
- `COM` - flake8-commas
- `C4` - flake8-comprehensions
- `T20` - flake8-print (no print statements except in CLI tools)
- `PTH` - flake8-use-pathlib (use pathlib for file operations)
- `I` - isort (import sorting)
- `C90` - mccabe (complexity checking)
- `N` - pep8-naming
- `E` - pycodestyle-error
- `W` - pycodestyle-warning
- `F` - Pyflakes
- `PL` - Pylint
- `UP` - pyupgrade
- `RUF` - Ruff-specific rules

### Type Checking

Follow mypy configuration defined in `mypy.ini`:

- **Type hints required:** All function definitions must have type hints
- Disallow untyped definitions (`disallow_untyped_defs = true`)
- Check untyped definitions (`check_untyped_defs = true`)
- Use strict optional checking (`strict_optional = true`)
- Enable all warnings for unused ignores

Example:
```python
from pathlib import Path
from typing import Any

def read_project_file(file_path: Path) -> dict[str, Any]:
    """Read and parse an Ableton Live project file.

    Args:
        file_path: Path to the .als file

    Returns:
        Dictionary containing parsed project data

    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file is not a valid .als file
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Project file not found: {file_path}")
    ...
```

### Testing

Use the pytest framework with the configuration defined in `pytest.toml`:

#### Test Structure

- Place all tests in the `tests/` directory
- Follow naming conventions:
  - Test files: `test_*.py` or `*_test.py`
  - Test classes: `Test*`
  - Test functions: `test_*`

#### Test Markers

Use appropriate markers to categorize tests:

- `@pytest.mark.unit` - Unit tests that do not require external dependencies
- `@pytest.mark.integration` - Integration tests that test multiple components together
- `@pytest.mark.functional` - Functional tests that test the application end-to-end
- `@pytest.mark.slow` - Tests that take a long time to run
- `@pytest.mark.network` - Tests that require network access
- `@pytest.mark.database` - Tests that interact with a database
- `@pytest.mark.api` - Tests for API endpoints
- `@pytest.mark.ui` - Tests for UI components
- `@pytest.mark.smoke` - Basic smoke tests for critical functionality
- `@pytest.mark.concurrent` - Tests that involve concurrent execution
- `@pytest.mark.load` - Load testing and performance tests

#### Test Example

```python
import pytest
from pathlib import Path
from aelus.parser import parse_als_file

@pytest.mark.unit
def test_parse_als_file_basic() -> None:
    """Test basic parsing of a valid .als file."""
    test_file = Path("tests/fixtures/basic_project.als")
    result = parse_als_file(test_file)
    assert result is not None
    assert "tracks" in result

@pytest.mark.integration
def test_project_dashboard_integration() -> None:
    """Test integration between parser and dashboard."""
    ...
```

### File Structure

The project follows this structure:

```
aelus/
├── .github/
│   ├── copilot-instructions.md
│   └── dependabot.yml
├── src/
│   └── aelus/
│       ├── __init__.py
│       ├── _version.py
│       └── ... (application modules)
├── tests/
│   ├── test_*.py
│   └── fixtures/
├── pyproject.toml
├── pytest.toml
├── mypy.ini
├── README.md
└── LICENSE
```

### Documentation Standards

#### Docstrings

Use Google-style docstrings for all public functions, classes, and modules:

```python
from pathlib import Path
from typing import Any

def process_audio_file(
    audio_path: Path,
    sample_rate: int = 44100,
) -> dict[str, Any]:
    """Process an audio file referenced in an Ableton Live project.

    This function analyzes audio files to extract metadata and prepare
    them for display in the dashboard.

    Args:
        audio_path: Path to the audio file to process
        sample_rate: Target sample rate for processing (default: 44100)

    Returns:
        Dictionary containing audio metadata with keys:
            - duration: Length of audio in seconds
            - channels: Number of audio channels
            - format: Audio file format (wav, mp3, etc.)

    Raises:
        FileNotFoundError: If audio file does not exist
        ValueError: If sample_rate is not positive

    Examples:
        >>> audio_path = Path("samples/kick.wav")
        >>> metadata = process_audio_file(audio_path)
        >>> print(metadata['duration'])
        2.5
    """
    if sample_rate <= 0:
        raise ValueError("Sample rate must be positive")
    ...
```

#### Inline Comments

- Keep inline comments minimal and meaningful
- Explain *why*, not *what* (code should be self-explanatory)
- Update comments when code changes

### Error Handling

- Use specific exception types rather than generic `Exception`
- Provide clear error messages with context
- Handle expected errors gracefully
- Let unexpected errors propagate with informative messages

Example:
```python
from pathlib import Path

class InvalidProjectFileError(ValueError):
    """Raised when a project file is invalid or corrupted."""
    pass

def validate_als_file(file_path: Path) -> None:
    """Validate that a file is a valid Ableton Live project.

    Args:
        file_path: Path to the file to validate

    Raises:
        FileNotFoundError: If the file does not exist
        InvalidProjectFileError: If the file is not a valid .als file
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.suffix != ".als":
        raise InvalidProjectFileError(
            f"Expected .als file, got {file_path.suffix}"
        )
```

### Path Handling

**Always use `pathlib.Path` for file system operations** (enforced by PTH Ruff rule):

✅ **Do:**
```python
from pathlib import Path

project_dir = Path("/path/to/projects")
als_file = project_dir / "my_project.als"

if als_file.exists():
    content = als_file.read_text()
```

❌ **Don't:**
```python
import os

project_dir = "/path/to/projects"
als_file = os.path.join(project_dir, "my_project.als")

if os.path.exists(als_file):
    with open(als_file) as f:
        content = f.read()
```

### Dependencies

- **Minimize external dependencies** - only add when absolutely necessary
- When adding a dependency, provide justification in the PR description
- No dependencies are currently defined in `pyproject.toml` - keep it minimal
- Use Python standard library when possible

## Ableton Live Specific Guidelines

### .als File Format

- `.als` files are gzipped XML files containing project structure
- Handle file decompression and XML parsing properly
- Consider version compatibility (different Ableton Live versions)

### Project Structure Considerations

- Ableton Live projects reference external audio files
- Audio file paths can be absolute or relative
- Handle missing audio file references gracefully
- Respect different track types: Audio, MIDI, Return, Master

### Version Compatibility

- Be aware that different Ableton Live versions may use different XML schemas
- Document which Ableton Live versions are supported
- Provide informative error messages for unsupported versions

Example:
```python
from pathlib import Path
import gzip
import xml.etree.ElementTree as ET

def parse_als_file(als_path: Path) -> ET.Element:
    """Parse an Ableton Live project file.

    Args:
        als_path: Path to the .als file

    Returns:
        Root element of the parsed XML tree

    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file cannot be parsed as valid XML
    """
    if not als_path.exists():
        raise FileNotFoundError(f"Project file not found: {als_path}")

    try:
        with gzip.open(als_path, 'rb') as f:
            tree = ET.parse(f)
            return tree.getroot()
    except (OSError, ET.ParseError) as e:
        raise ValueError(f"Invalid .als file: {e}") from e
```

## Common Patterns

### Configuration Management

Use `pyproject.toml` for project configuration. Access version dynamically:

```python
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("aelus")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"
```

### Logging

Use Python's standard logging module instead of print statements:

```python
import logging

logger = logging.getLogger(__name__)

def process_project(project_path: Path) -> None:
    """Process an Ableton Live project."""
    logger.info("Processing project: %s", project_path)
    try:
        # ... processing logic
        logger.debug("Successfully processed project")
    except Exception as e:
        logger.error("Failed to process project: %s", e)
        raise
```

## Do's and Don'ts

### Do:

✅ Use `pathlib.Path` for all file system operations
✅ Include type hints for all function parameters and return values
✅ Write comprehensive tests with appropriate markers
✅ Use Google-style docstrings for all public APIs
✅ Handle errors with specific exception types
✅ Use logging instead of print statements (except in CLI entry points)
✅ Follow the Ruff configuration in `pyproject.toml`
✅ Keep dependencies minimal and justified
✅ Write self-documenting code with clear variable names
✅ Validate input parameters and provide clear error messages
✅ Consider edge cases in your implementation

### Don't:

❌ Use `os.path` module - use `pathlib.Path` instead
❌ Leave functions without type hints
❌ Use generic `Exception` - use specific exception types
❌ Use `print()` statements outside of CLI tools
❌ Add dependencies without clear justification
❌ Write tests without appropriate markers
❌ Ignore mypy type checking errors
❌ Commit code that doesn't pass `ruff check` and `ruff format`
❌ Shadow built-in names (enforced by `flake8-builtins`)
❌ Create overly complex functions (watch mccabe complexity)
❌ Skip error handling for file operations
❌ Leave trailing whitespace in files
❌ Commit files that don't end with a newline

## Development Workflow

1. **Before coding:**
   - Understand the requirement clearly
   - Check existing code patterns in the repository
   - Plan your implementation

2. **While coding:**
   - Write type hints as you write code
   - Add docstrings immediately after function definitions
   - Use `pathlib` for file operations
   - Handle errors appropriately

3. **Before committing:**
   - Run `ruff check .` to check for linting issues
   - Run `ruff format .` to format code
   - Run `mypy .` to check type hints
   - Run `pytest` to ensure all tests pass
   - Verify test coverage for new code

4. **Writing tests:**
   - Write tests alongside new features
   - Use appropriate test markers
   - Aim for high test coverage
   - Test both happy paths and error cases

## Additional Resources

- **Repository:** https://github.com/masriamir/aelus
- **Ruff documentation:** https://docs.astral.sh/ruff/
- **pytest documentation:** https://docs.pytest.org/
- **mypy documentation:** https://mypy.readthedocs.io/
- **Python Type Hints:** https://docs.python.org/3/library/typing.html
- **Ableton Live File Format:** Community-documented XML structure

---

**Note:** These instructions should be reviewed and updated as the project evolves. Always ensure Copilot-generated code adheres to these standards.

