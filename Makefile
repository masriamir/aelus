# Makefile for Aelus project
# All Python commands executed through uv

SHELL := /bin/bash
.DEFAULT_GOAL := help

# Colors for output
RESET := \033[0m
BOLD := \033[1m
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
RED := \033[31m

# Project variables
PROJECT_NAME := aelus
SOURCE_DIR := src
TEST_DIR := tests
PYTHON_VERSION := 3.13

# Check if uv is installed
UV := $(shell command -v uv 2> /dev/null)
ifndef UV
    $(error "uv is not installed. Please install it first: https://github.com/astral-sh/uv")
endif

.PHONY: help
help: ## Show this help message
	@echo -e "$(BOLD)$(BLUE)Aelus Development Commands$(RESET)"
	@echo -e "$(GREEN)Usage:$(RESET) make $(YELLOW)[target]$(RESET)\n"
	@echo -e "$(BOLD)Available targets:$(RESET)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-20s$(RESET) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""

# ============= Setup & Installation =============

.PHONY: install
install: ## Install project dependencies
	@echo -e "$(GREEN)Installing project dependencies...$(RESET)"
	uv sync
	@echo -e "$(GREEN)✓ Dependencies installed$(RESET)"

.PHONY: install-dev
install-dev: ## Install development dependencies
	@echo -e "$(GREEN)Installing development dependencies...$(RESET)"
	uv sync --group dev
	@echo -e "$(GREEN)✓ Development dependencies installed$(RESET)"

.PHONY: install-test
install-test: ## Install test dependencies
	@echo -e "$(GREEN)Installing test dependencies...$(RESET)"
	uv sync --group test
	@echo -e "$(GREEN)✓ Test dependencies installed$(RESET)"

.PHONY: install-all
install-all: ## Install all dependencies (project, dev, test, quality)
	@echo -e "$(GREEN)Installing all dependencies...$(RESET)"
	uv sync --all-groups
	@echo -e "$(GREEN)✓ All dependencies installed$(RESET)"

.PHONY: setup
setup: clean-all install-all ## Complete project setup (clean + install everything)
	@echo -e "$(GREEN)Creating necessary directories...$(RESET)"
	@mkdir -p logs
	@touch .env
	@echo -e "$(BOLD)$(GREEN)✓ Project setup complete!$(RESET)"
	@echo -e "$(YELLOW)Next steps:$(RESET)"
	@echo -e "  1. Configure your .env file"
	@echo -e "  2. Run 'make test' to verify setup"
	@echo -e "  3. Run 'make dev' to start development server"

.PHONY: sync
sync: ## Sync dependencies with pyproject.toml
	@echo -e "$(GREEN)Syncing dependencies...$(RESET)"
	uv sync
	@echo -e "$(GREEN)✓ Dependencies synced$(RESET)"

# ============= Code Quality =============

.PHONY: format
format: ## Format code with ruff
	@echo -e "$(GREEN)Formatting code...$(RESET)"
	uv run ruff format $(SOURCE_DIR) $(TEST_DIR)
	@echo -e "$(GREEN)✓ Code formatted$(RESET)"

.PHONY: lint
lint: ## Run ruff linter
	@echo -e "$(GREEN)Running linter...$(RESET)"
	uv run ruff check $(SOURCE_DIR) $(TEST_DIR)
	@echo -e "$(GREEN)✓ Linting complete$(RESET)"

.PHONY: lint-fix
lint-fix: ## Run ruff linter with auto-fix
	@echo -e "$(GREEN)Running linter with fixes...$(RESET)"
	uv run ruff check --fix $(SOURCE_DIR) $(TEST_DIR)
	@echo -e "$(GREEN)✓ Linting with fixes complete$(RESET)"

.PHONY: typecheck
typecheck: ## Run mypy type checking
	@echo -e "$(GREEN)Running type checker...$(RESET)"
	uv run mypy $(SOURCE_DIR)
	@echo -e "$(GREEN)✓ Type checking complete$(RESET)"

.PHONY: check
check: lint typecheck ## Run all quality checks (lint + typecheck)
	@echo -e "$(BOLD)$(GREEN)✓ All quality checks passed!$(RESET)"

.PHONY: check-fix
check-fix: format lint-fix typecheck ## Run all quality checks with fixes
	@echo -e "$(BOLD)$(GREEN)✓ All quality checks passed with fixes!$(RESET)"

# ============= Testing =============

.PHONY: test
test: ## Run all tests
	@echo -e "$(GREEN)Running all tests...$(RESET)"
	uv run pytest $(TEST_DIR) -v
	@echo -e "$(GREEN)✓ All tests complete$(RESET)"

.PHONY: test-unit
test-unit: ## Run unit tests only
	@echo -e "$(GREEN)Running unit tests...$(RESET)"
	uv run pytest $(TEST_DIR) -v -m unit
	@echo -e "$(GREEN)✓ Unit tests complete$(RESET)"

.PHONY: test-integration
test-integration: ## Run integration tests only
	@echo -e "$(GREEN)Running integration tests...$(RESET)"
	uv run pytest $(TEST_DIR) -v -m integration
	@echo -e "$(GREEN)✓ Integration tests complete$(RESET)"

.PHONY: test-cov
test-cov: ## Run tests with coverage report
	@echo -e "$(GREEN)Running tests with coverage...$(RESET)"
	uv run pytest $(TEST_DIR) --cov=$(SOURCE_DIR)/$(PROJECT_NAME) --cov-report=term-missing --cov-report=html
	@echo -e "$(GREEN)✓ Coverage report generated$(RESET)"
	@echo -e "$(YELLOW)HTML report available at:$(RESET) htmlcov/index.html"

.PHONY: test-watch
test-watch: ## Run tests in watch mode
	@echo -e "$(GREEN)Starting test watch mode...$(RESET)"
	uv run pytest-watch $(TEST_DIR) -- -v

.PHONY: test-failed
test-failed: ## Run only previously failed tests
	@echo -e "$(GREEN)Running failed tests...$(RESET)"
	uv run pytest $(TEST_DIR) -v --lf

.PHONY: test-marker
test-marker: ## Run tests with specific marker (use MARKER=name)
	@if [ -z "$(MARKER)" ]; then \
		echo -e "$(RED)Error: MARKER not specified$(RESET)"; \
		echo -e "Usage: make test-marker MARKER=unit"; \
		exit 1; \
	fi
	@echo -e "$(GREEN)Running tests marked as '$(MARKER)'...$(RESET)"
	uv run pytest $(TEST_DIR) -v -m $(MARKER)

# ============= Development =============

.PHONY: run
run: ## Start the API server
	@echo -e "$(GREEN)Starting Aelus API server...$(RESET)"
	uv run uvicorn aelus.api.app:app --host 0.0.0.0 --port 8000

.PHONY: dev
dev: ## Start server in development mode with auto-reload
	@echo -e "$(GREEN)Starting Aelus API in development mode...$(RESET)"
	uv run uvicorn aelus.api.app:app --host 0.0.0.0 --port 8000 --reload --log-level debug

.PHONY: debug
debug: ## Start server with debugging enabled
	@echo -e "$(GREEN)Starting Aelus API with debugging...$(RESET)"
	PYTHONDONTWRITEBYTECODE=1 uv run python -m debugpy --listen 5678 --wait-for-client -m uvicorn aelus.api.app:app --host 0.0.0.0 --port 8000 --reload

.PHONY: shell
shell: ## Start interactive Python shell with project context
	@echo -e "$(GREEN)Starting Python shell...$(RESET)"
	uv run python

.PHONY: ipython
ipython: ## Start IPython shell with project context
	@echo -e "$(GREEN)Starting IPython shell...$(RESET)"
	uv run ipython

# ============= Database (Future) =============

.PHONY: db-upgrade
db-upgrade: ## Apply database migrations (future)
	@echo -e "$(YELLOW)Database migrations not yet implemented$(RESET)"

.PHONY: db-downgrade
db-downgrade: ## Rollback database migration (future)
	@echo -e "$(YELLOW)Database migrations not yet implemented$(RESET)"

# ============= Documentation =============

.PHONY: docs
docs: ## Generate API documentation
	@echo -e "$(GREEN)Generating documentation...$(RESET)"
	@echo -e "$(YELLOW)Documentation generation not yet implemented$(RESET)"
	@echo -e "API docs available at: http://localhost:8000/docs"

.PHONY: docs-serve
docs-serve: ## Serve documentation locally
	@echo -e "$(GREEN)Starting documentation server...$(RESET)"
	@echo -e "Run 'make dev' and visit http://localhost:8000/docs"

# ============= Cleaning =============

.PHONY: clean
clean: ## Remove build artifacts
	@echo -e "$(GREEN)Cleaning build artifacts...$(RESET)"
	rm -rf build/ dist/ *.egg-info
	@echo -e "$(GREEN)✓ Build artifacts removed$(RESET)"

.PHONY: clean-pyc
clean-pyc: ## Remove Python cache files
	@echo -e "$(GREEN)Cleaning Python cache files...$(RESET)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo -e "$(GREEN)✓ Python cache files removed$(RESET)"

.PHONY: clean-test
clean-test: ## Remove test artifacts
	@echo -e "$(GREEN)Cleaning test artifacts...$(RESET)"
	rm -rf .coverage htmlcov/ .pytest_cache/ .mypy_cache/
	rm -rf logs/pytest-logs.log
	@echo -e "$(GREEN)✓ Test artifacts removed$(RESET)"

.PHONY: clean-all
clean-all: clean clean-pyc clean-test ## Complete cleanup (all artifacts)
	@echo -e "$(BOLD)$(GREEN)✓ All artifacts cleaned!$(RESET)"

# ============= Utilities =============

.PHONY: version
version: ## Show project version
	@uv run python -c "from aelus import __version__; print(__version__)" 2>/dev/null || echo "0.0.0+unknown"

.PHONY: deps
deps: ## Show project dependencies
	@echo -e "$(BOLD)Project Dependencies:$(RESET)"
	@uv pip list

.PHONY: outdated
outdated: ## Check for outdated dependencies
	@echo -e "$(GREEN)Checking for outdated dependencies...$(RESET)"
	@uv pip list --outdated

.PHONY: env
env: ## Show environment information
	@echo -e "$(BOLD)Environment Information:$(RESET)"
	@echo -e "$(YELLOW)Python:$(RESET) $$(uv run python --version)"
	@echo -e "$(YELLOW)uv:$(RESET) $$(uv --version)"
	@echo -e "$(YELLOW)Platform:$(RESET) $$(uname -s)"
	@echo -e "$(YELLOW)Directory:$(RESET) $$(pwd)"

.PHONY: tree
tree: ## Show project structure
	@echo -e "$(BOLD)Project Structure:$(RESET)"
	@tree -I "__pycache__|*.pyc|*.pyo|.git|.mypy_cache|.pytest_cache|htmlcov|*.egg-info" -L 3 2>/dev/null || find . -type f -name "*.py" | head -20

# ============= Git Hooks =============

.PHONY: pre-commit-install
pre-commit-install: ## Install pre-commit hooks
	@echo -e "$(GREEN)Installing pre-commit hooks...$(RESET)"
	uv run pre-commit install
	@echo -e "$(GREEN)✓ Pre-commit hooks installed$(RESET)"

.PHONY: pre-commit-run
pre-commit-run: ## Run pre-commit on all files
	@echo -e "$(GREEN)Running pre-commit on all files...$(RESET)"
	uv run pre-commit run --all-files

# ============= CI/CD =============

.PHONY: ci
ci: check test ## Run CI pipeline locally (checks + tests)
	@echo -e "$(BOLD)$(GREEN)✓ CI pipeline passed!$(RESET)"

.PHONY: ci-full
ci-full: check test-cov ## Run full CI pipeline locally (checks + tests with coverage)
	@echo -e "$(BOLD)$(GREEN)✓ Full CI pipeline passed!$(RESET)"

# ============= Shortcuts =============

.PHONY: f
f: format ## Shortcut for format

.PHONY: l
l: lint ## Shortcut for lint

.PHONY: t
t: test ## Shortcut for test

.PHONY: r
r: run ## Shortcut for run

.PHONY: d
d: dev ## Shortcut for dev

.PHONY: c
c: check ## Shortcut for check
