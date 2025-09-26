# Developer Guide

This guide is for developers who want to contribute to or build upon the Google Takeout Live Photos Helper.

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
# Run all tests
make test

# Run with coverage
PYTHONPATH=src pytest tests/ --cov=google_takeout_live_photos --cov-report=html

# Run specific test
PYTHONPATH=src pytest tests/test_processor.py -v
```

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
