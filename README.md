# 🌬️ Aelus

[![CodeQL](https://github.com/masriamir/aelus/workflows/CodeQL/badge.svg)](https://github.com/masriamir/aelus/actions/workflows/codeql.yml)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0+-00a393.svg)](https://fastapi.tiangolo.com)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A web-based dashboard for viewing and organizing Ableton Live project files.

## 📋 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Development](#-development)
- [API Documentation](#-api-documentation)
- [Configuration](#-configuration)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### Current

- 🚀 **FastAPI Backend** - Modern, fast web framework with automatic OpenAPI documentation
- 📁 **ALS File Parsing** - Read and parse Ableton Live project files (.als)
- 🔌 **Pluggable Parser Architecture** - Hot-swap between custom and third-party parsers
- 🎛️ **Rate Limiting** - Configurable API rate limiting for production use
- 📊 **Health Monitoring** - Comprehensive health check endpoints
- 🧪 **Testing Suite** - Unit and integration tests with coverage reporting

### Planned

- 🎨 Web UI for browsing projects
- 🔍 Search and filter capabilities
- 📈 Project analytics and insights
- 🏷️ Tagging and categorization
- 💾 Database persistence
- 🔐 Authentication and authorization
- 📦 Batch processing
- 🎵 Audio preview functionality

## 📋 Requirements

- **Python** 3.13 or higher
- **uv** - Modern Python package manager ([installation guide](https://github.com/astral-sh/uv))
- **Operating System** - Linux, macOS, or Windows (WSL recommended)
- **Ableton Live** files for testing (optional)

## 📦 Installation

### Development Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/masriamir/aelus.git
   cd aelus
   ```

2. **Ensure uv is installed**

   ```bash
   # Install uv if not already installed
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Run the setup**

   ```bash
   make setup
   ```

   This will:
   - Clean any existing artifacts
   - Install all dependencies (project, dev, test)
   - Create necessary directories
   - Initialize configuration files

4. **Configure environment** (optional)

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Manual Installation

If you prefer not to use Make:

```bash
# Install project with all dependencies
uv sync --all-groups

# Create necessary directories
mkdir -p logs

# Create .env file
touch .env
```

## 🚀 Quick Start

### Starting the API Server

```bash
# Development mode (with auto-reload)
make dev

# Production mode
make run

# Or directly with uv
uv run uvicorn aelus.api.app:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, visit:

- **Interactive API docs**: http://localhost:8000/docs
- **Alternative API docs**: http://localhost:8000/redoc
- **OpenAPI schema**: http://localhost:8000/openapi.json

### Basic Usage

```bash
# Check API health
curl http://localhost:8000/health/

# Response
{
  "status": "healthy",
  "timestamp": "2024-11-27T10:00:00Z",
  "version": "0.1.0",
  "service": "Aelus"
}
```

### Parsing ALS Files (Python)

```python
from pathlib import Path
from aelus.parsers import get_parser, ParserType

# Auto-select best available parser
parser = get_parser()
project = parser.parse(Path("my_project.als"))

print(f"Project: {project.name}")
print(f"Tempo: {project.tempo} BPM")
print(f"Tracks: {len(project.tracks)}")

# Use specific parser
custom_parser = get_parser(ParserType.CUSTOM)
project = custom_parser.parse(Path("my_project.als"))
```

## 🛠️ Development

### Makefile Commands

The project includes a comprehensive Makefile for common tasks:

```bash
# Setup and Installation
make setup          # Complete project setup
make install        # Install project dependencies
make install-dev    # Install development dependencies
make install-all    # Install all dependencies

# Code Quality
make format         # Format code with ruff
make lint           # Run linter
make typecheck      # Run type checking
make check          # Run all quality checks

# Testing
make test           # Run all tests
make test-unit      # Run unit tests only
make test-cov       # Run tests with coverage
make test-watch     # Run tests in watch mode

# Development
make dev            # Start dev server with auto-reload
make debug          # Start server with debugging
make shell          # Start Python REPL

# Utilities
make clean-all      # Clean all artifacts
make help           # Show all available commands
```

### Code Style

This project uses:

- **ruff** for linting and formatting
- **mypy** for type checking
- **Google-style** docstrings
- **Type hints** for all functions

Example:

```python
from pathlib import Path
from aelus.parsers.base import ALSProject

def process_project(
    file_path: Path,
    validate: bool = True,
    parser_type: str | None = None
) -> ALSProject:
    """Process an Ableton Live project file.

    Args:
        file_path: Path to the .als file.
        validate: Whether to validate the file before parsing.
        parser_type: Specific parser to use (optional).

    Returns:
        Parsed ALS project data.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        InvalidALSFileError: If the file is corrupted.
    """
    # Implementation here
    pass
```

### Pre-commit Hooks

Install pre-commit hooks for automatic code quality checks:

```bash
make pre-commit-install
```

## 📚 API Documentation

### Endpoints

#### Health Checks

- `GET /health/` - Basic health status
- `GET /health/ready` - Readiness check
- `GET /health/live` - Liveness probe

#### Projects (Coming Soon)

- `GET /api/v1/projects` - List projects
- `GET /api/v1/projects/{id}` - Get project details
- `POST /api/v1/projects/scan` - Scan directory for projects

### Rate Limiting

The API includes configurable rate limiting:

- Default: 100 requests per 60 seconds
- Configure via environment variables
- Returns 429 status when exceeded

## ⚙️ Configuration

Configuration is managed through environment variables. Create a `.env` file:

```env
# Application
APP_NAME=Aelus
APP_VERSION=0.1.0
DEBUG=false

# Server
HOST=0.0.0.0
PORT=8000

# API
API_V1_PREFIX=/api/v1
DOCS_URL=/docs
REDOC_URL=/redoc

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60

# CORS
CORS_ENABLED=true
CORS_ORIGINS=["*"]

# Parser (optional)
DEFAULT_PARSER=auto  # auto, custom, or third_party
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test markers
make test-marker MARKER=unit
make test-marker MARKER=integration

# Run in watch mode for TDD
make test-watch
```

### Test Structure

```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for workflows
└── fixtures/       # Test data and mocks
```

### Coverage Requirements

- Minimum coverage: 80%
- Coverage report: `htmlcov/index.html`

## 📂 Project Structure

```
aelus/
├── src/aelus/
│   ├── api/            # FastAPI application
│   │   ├── app.py      # App factory
│   │   ├── routes/     # API endpoints
│   │   └── middleware/ # Custom middleware
│   ├── core/           # Core configuration
│   │   └── config.py   # Settings management
│   ├── parsers/        # ALS file parsers
│   │   ├── base.py     # Parser interface
│   │   ├── custom.py   # Custom implementation
│   │   └── factory.py  # Parser factory
│   └── utils/          # Utility modules
│       └── file_io.py  # File operations
├── tests/              # Test suite
├── docs/               # Documentation
├── Makefile            # Development commands
├── pyproject.toml      # Project configuration
└── README.md           # This file
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run quality checks (`make check`)
5. Run tests (`make test`)
6. Commit your changes (following conventional commits)
7. Push to your fork
8. Open a Pull Request

### Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/my-feature

# 2. Make changes and test
make check-fix  # Format and fix issues
make test       # Run tests

# 3. Commit
git add .
git commit -m "feat: add amazing feature"

# 4. Push and create PR
git push origin feature/my-feature
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation
- [uv](https://github.com/astral-sh/uv) for modern Python tooling
- The Ableton Live community

## 📮 Contact

- **Author**: Amir Masri
- **GitHub**: [@masriamir](https://github.com/masriamir)
- **Issues**: [GitHub Issues](https://github.com/masriamir/aelus/issues)

---

Made with ❤️ for the music production community
