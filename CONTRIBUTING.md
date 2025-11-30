# Contributing to Aelus

Thank you for your interest in contributing to Aelus! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Commit Message Format](#commit-message-format)
- [Branch Naming Conventions](#branch-naming-conventions)
- [Pull Request Process](#pull-request-process)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)

## Code of Conduct

Please be respectful and considerate in all interactions. We are committed to providing a welcoming and inclusive environment for all contributors.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Set up the development environment
4. Create a feature branch
5. Make your changes
6. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/aelus.git
cd aelus

# Set up the project
make setup

# Verify setup
make test
```

## Code Style Guidelines

### General Principles

- Write clear, self-documenting code
- Follow the principle of least surprise
- Keep functions small and focused
- Avoid premature optimization

### Python Style

All code must pass `ruff` checks and `mypy` type checking.

#### Type Hints

Type hints are **required** for all function signatures:

```python
from pathlib import Path
from typing import Any

def process_file(
    file_path: Path,
    options: dict[str, Any] | None = None,
    validate: bool = True
) -> dict[str, Any]:
    """Process a file and return results."""
    ...
```

#### Docstrings

Use Google-style docstrings for all public modules, functions, and classes:

```python
def parse_als_file(file_path: Path) -> ALSProject:
    """Parse an Ableton Live Set file.

    Reads and parses a .als file, extracting project metadata,
    tracks, samples, and plugin information.

    Args:
        file_path: Path to the .als file to parse.

    Returns:
        ALSProject containing all parsed data.

    Raises:
        FileNotFoundError: If the file does not exist.
        InvalidALSFileError: If the file cannot be parsed.

    Examples:
        >>> project = parse_als_file(Path("my_project.als"))
        >>> print(project.tempo)
        120.0
    """
    ...
```

#### Import Sorting

Imports are sorted using `isort` configuration in `pyproject.toml`:

```python
# Standard library imports
import logging
from pathlib import Path
from typing import Any

# Third-party imports
import pytest
from fastapi import FastAPI
from pydantic import BaseModel

# First-party imports
from aelus.core.config import Settings
from aelus.parsers import get_parser
```

#### Naming Conventions

- **Variables and functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private attributes**: `_leading_underscore`
- **Type variables**: `PascalCase` (e.g., `T`, `ParserType`)

### File Organization

```python
"""Module docstring describing purpose.

Extended description if needed.
"""

# Imports (sorted)
import logging
from pathlib import Path

from pydantic import BaseModel

from aelus.utils import helper

# Module-level constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# Module-level logger
logger = logging.getLogger(__name__)


# Class definitions
class MyClass:
    """Class docstring."""

    def __init__(self) -> None:
        """Initialize instance."""
        pass


# Function definitions
def my_function() -> None:
    """Function docstring."""
    pass
```

## Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(parser): add support for Live 12 file format

fix(api): correct rate limit header values

docs(readme): update installation instructions

test(parser): add integration tests for async parsing
```

## Branch Naming Conventions

Use descriptive branch names following this pattern:

```
<type>/<short-description>
```

### Examples

- `feature/als-parser-v2`
- `fix/rate-limit-reset`
- `docs/api-documentation`
- `refactor/settings-module`

## Pull Request Process

### Before Submitting

1. **Update your branch** with the latest `main`:

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run quality checks**:

   ```bash
   make check-fix
   ```

3. **Run tests**:

   ```bash
   make test
   ```

4. **Ensure coverage** meets the minimum threshold (80%)

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added for new functionality
```

### Review Process

1. At least one maintainer approval required
2. All CI checks must pass
3. No merge conflicts
4. Documentation updated if needed

## Testing Guidelines

### Test Structure

```
tests/
├── conftest.py          # Shared fixtures
├── unit/                # Unit tests
│   ├── api/
│   ├── parsers/
│   └── utils/
├── integration/         # Integration tests
└── fixtures/            # Test data
```

### Writing Tests

- Use `pytest.mark.unit` for unit tests
- Use `pytest.mark.integration` for integration tests
- Follow AAA pattern (Arrange, Act, Assert)
- One assertion per test when possible
- Use descriptive test names

```python
@pytest.mark.unit
def test_parse_valid_als_file_extracts_tempo(
    parser: CustomALSParser,
    sample_als_file: Path,
) -> None:
    """Test that parsing extracts tempo correctly."""
    # Arrange - done via fixtures

    # Act
    project = parser.parse(sample_als_file)

    # Assert
    assert project.tempo == 120.0
```

### Running Tests

```bash
# All tests
make test

# Unit tests only
make test-unit

# With coverage
make test-cov

# Watch mode
make test-watch
```

## Documentation

### When to Update Documentation

- Adding new features
- Changing existing behavior
- Adding new dependencies
- Modifying configuration options

### Documentation Locations

- **README.md**: Project overview and quick start
- **CONTRIBUTING.md**: This file
- **Docstrings**: API documentation
- **Comments**: Complex code explanations

### Writing Documentation

- Use clear, concise language
- Include code examples where helpful
- Keep examples up-to-date
- Test documentation examples

## Questions?

If you have questions about contributing, please:

1. Check existing issues and discussions
2. Open a new issue with the `question` label
3. Reach out to maintainers

Thank you for contributing to Aelus! 🎉
