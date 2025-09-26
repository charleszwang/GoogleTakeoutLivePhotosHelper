# Makefile for Google Takeout Live Photos Helper
# Python equivalent of Ruby's rake tasks

.PHONY: help install install-dev test lint format check security clean all

# Default target
help:
	@echo "Available targets:"
	@echo "  install      - Install the package"
	@echo "  install-dev  - Install development dependencies"
	@echo "  test         - Run tests"
	@echo "  lint         - Run all linting tools"
	@echo "  format       - Format code"
	@echo "  check        - Run all quality checks"
	@echo "  security     - Run security checks"
	@echo "  clean        - Clean build artifacts"
	@echo "  all          - Run format, lint, test, and security checks"

# Installation
install:
	pip install -e .

install-dev:
	pip install -r requirements-dev.txt
	pre-commit install

# Testing
test:
	PYTHONPATH=src pytest tests/ -v --cov=google_takeout_live_photos --cov-report=term-missing --cov-report=html

test-quick:
	pytest tests/ -x -v

# Code formatting
format:
	@echo "Running code formatters..."
	black src/ tests/ scripts/
	isort src/ tests/ scripts/

# Linting (equivalent to rubocop)
lint:
	@echo "Running linting tools..."
	flake8 src/ tests/ scripts/
	PYTHONPATH=src pylint src/google_takeout_live_photos/
	PYTHONPATH=src mypy src/google_takeout_live_photos/ --ignore-missing-imports

# Style checks
style:
	@echo "Running style checks..."
	pycodestyle src/ tests/ scripts/
	pydocstyle src/google_takeout_live_photos/

# Security checks
security:
	@echo "Running security checks..."
	bandit -r . -x tests/
	safety check

# Dead code detection
deadcode:
	@echo "Checking for dead code..."
	vulture src/google_takeout_live_photos/

# All quality checks
check: format lint style security deadcode
	@echo "All quality checks completed!"

# Pre-commit hooks
pre-commit:
	pre-commit run --all-files

# Build package
build:
	python -m build

# Build standalone executable
build-exe:
	@echo "Building standalone executable..."
	pip install pyinstaller>=6.0
	python build_executable.py

# Build executable for distribution
build-exe-dist: build-exe
	@echo "Creating distribution package..."
	mkdir -p dist/release
	cp dist/GoogleTakeoutHelper* dist/release/
	@echo "✅ Executable ready for distribution in dist/release/"

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Run everything (equivalent to rubocop + tests)
all: format check test
	@echo "All checks passed! 🎉"

# Development workflow
dev-setup: install-dev
	@echo "Development environment setup complete!"
	@echo "Run 'make all' to run all quality checks"

# Quick development check
quick: format lint test-quick
	@echo "Quick development check completed!"
