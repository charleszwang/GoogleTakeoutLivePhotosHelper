# Developer Guide

This guide is for developers who want to contribute to or build upon the Google Takeout Live Photos Helper.

## 📊 Project Status

![Coverage](https://img.shields.io/badge/coverage-44%25-yellow)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)

> **Note**: Build status badge will appear automatically once you push to GitHub and the CI workflow runs.

## 📊 Current Coverage Status

- **Overall Coverage**: 44% (Target: 90%+) 📈 **Improved!**
- **Core Processor**: 89% coverage ✅ **Excellent!**
- **CLI Module**: 76% coverage ✅ **Good!**
- **GUI Module**: 11% coverage (GUI testing is complex)

**Coverage Breakdown:**
- ✅ **File operations**: Excellently tested (89%)
- ✅ **Core processing**: Comprehensive coverage
- ✅ **Validation methods**: Well tested
- ✅ **CLI interface**: Good integration coverage (76%)
- ⚠️ **GUI components**: Minimal coverage (expected for GUI)
- ✅ **Edge cases**: Much improved coverage

## 🏗️ Project Structure

This project follows Python best practices with a clean, modular structure:

```
GoogleTakeoutLivePhotosHelper/
├── 📦 Source Code
│   └── src/google_takeout_live_photos/
│       ├── __init__.py              # Package initialization
│       ├── __main__.py              # Module entry point
│       ├── cli.py                   # Command line interface
│       ├── gui.py                   # Graphical user interface
│       └── processor.py             # Core processing logic
│
├── 🧪 Testing & Quality
│   ├── tests/                       # Comprehensive test suite
│   ├── Makefile                     # Development automation
│   ├── .pre-commit-config.yaml     # Code quality hooks
│   └── .pylintrc                    # Linting configuration
│
├── 🔧 Scripts & Tools
│   └── scripts/
│       └── launch_gui.py            # Simple GUI launcher
│
├── 📖 Documentation
│   └── docs/
│       ├── README.md                # This file
│       ├── CONTRIBUTING.md          # Developer guidelines
│       └── CHANGELOG.md             # Version history
│
├── ⚙️ Configuration
│   ├── pyproject.toml               # Modern Python packaging
│   ├── requirements.txt             # Runtime dependencies
│   ├── requirements-dev.txt         # Development dependencies
│   └── .gitignore                   # Git ignore rules
│
└── 🔄 Entry Points
    ├── google_takeout_live_photos_helper.py  # Backward compatibility
    └── .github/workflows/ci.yml              # CI/CD pipeline
```

## 🛠️ Development Setup

### Setting up Development Environment

```bash
# Clone and setup
git clone https://github.com/yourusername/google-takeout-live-photos-helper.git
cd google-takeout-live-photos-helper

# Install development dependencies
make dev-setup

# Or manually:
pip install -r requirements-dev.txt
pre-commit install
```

### Code Quality Tools

This project includes comprehensive code quality tools (Python's equivalent to rubocop):

```bash
# Run all quality checks
make all

# Individual tools
make format      # Format code with black and isort
make lint        # Run flake8, pylint, mypy
make security    # Run bandit and safety checks
make test        # Run test suite with coverage

# Pre-commit hooks (run automatically on commit)
pre-commit run --all-files
```

### Running Tests

```bash
# Run all tests with coverage
make test

# Quick test run
make test-quick

# Generate coverage report only
make coverage

# Generate coverage with badge
make coverage-badge

# Manual testing commands
PYTHONPATH=src pytest tests/ --cov=google_takeout_live_photos --cov-report=html
PYTHONPATH=src pytest tests/test_processor.py -v
```

### 📊 Code Coverage

The project maintains high code coverage standards:

- **Target**: 90%+ coverage
- **Current**: ![Coverage](https://img.shields.io/codecov/c/github/yourusername/google-takeout-live-photos-helper)
- **Reports**: Generated in `htmlcov/` directory
- **CI Integration**: Automatic coverage reporting on every commit

#### Coverage Reports

After running tests, you can view detailed coverage reports:

```bash
# Generate coverage report
make coverage

# Open HTML report in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

#### Coverage Requirements

- **New code**: Must have 95%+ coverage
- **Overall project**: Target 90%+ coverage (currently 38%)
- **Critical paths**: 100% coverage required for:
  - File processing logic
  - Data validation
  - Error handling paths

#### Coverage Improvement Plan

**Phase 1 (Target: 60%)**
- [ ] Add more processor tests for edge cases
- [ ] Test error handling paths
- [ ] Test validation methods

**Phase 2 (Target: 80%)**
- [ ] Add CLI integration tests
- [ ] Test configuration edge cases
- [ ] Add performance tests

**Phase 3 (Target: 90%+)**
- [ ] Mock-based GUI testing
- [ ] End-to-end workflow tests
- [ ] Error recovery testing

**Note**: GUI testing is inherently complex and may not reach high coverage percentages. Focus on testing the core business logic comprehensively.

## 🏗️ Architecture

### Modular Design

The codebase is organized into focused modules:

- **`processor.py`**: Core business logic for file processing
- **`cli.py`**: Command-line interface and argument parsing  
- **`gui.py`**: Graphical user interface using tkinter
- **`__init__.py`**: Package initialization and public API
- **`__main__.py`**: Module entry point for `python -m` execution

### Benefits of This Structure

1. **🧩 Separation of Concerns**: Each module has a single responsibility
2. **🔧 Easy Testing**: Isolated components are easier to test
3. **📦 Proper Packaging**: Follows Python packaging standards
4. **🔄 Reusability**: Core logic can be imported and used by other tools
5. **🚀 Multiple Entry Points**: CLI, GUI, and programmatic access
6. **📈 Scalability**: Easy to add new features and interfaces

## 🚀 Multiple Ways to Run

### As Installed Package (Recommended)
```bash
# After pip install -e .
google-takeout-helper --gui
google-takeout-helper --root ./Takeout --out-pairs ./pairs --out-leftovers ./leftovers
```

### As Python Module
```bash
python -m google_takeout_live_photos.cli --gui
python -m google_takeout_live_photos.gui  # GUI only
```

### Direct Script Execution
```bash
python scripts/launch_gui.py  # GUI launcher
python google_takeout_live_photos_helper.py --gui  # Backward compatibility
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📦 Building Executables

See [EXECUTABLE_GUIDE.md](EXECUTABLE_GUIDE.md) for creating standalone executables.
