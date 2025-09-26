# Google Takeout Live Photos Helper

A Python tool to organize Google Takeout exports by matching Live Photos pairs (photo + video) and separating standalone media files into organized directories. Could be used in situations where you have Google Takeout and need to import to Apple Photos or need the live photo to be stitched back together to send back to Google Photos.

## 🎯 What it does

When you export your Google Photos via Google Takeout, Live Photos are split into separate image and video files. This tool:

1. **Scans** your Google Takeout directory for image and video files
2. **Matches** Live Photos pairs using intelligent algorithms:
   - Same-folder exact name matching (e.g., `IMG_1234.HEIC` + `IMG_1234.MOV`)
   - Cross-folder exact name matching with optional duration filtering
3. **Organizes** matched pairs into a flat directory with numbered prefixes
4. **Separates** unmatched files into a "leftovers" directory
5. **Deduplicates** content using SHA1 hashes (optional)
6. **Creates** detailed manifest files tracking all operations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- `ffprobe` (part of FFmpeg) for video duration analysis (optional)
- `tkinter` for GUI (usually included with Python)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/google-takeout-live-photos-helper.git
cd google-takeout-live-photos-helper

# Install development dependencies (optional)
pip install -r requirements-dev.txt

# Install the package
pip install -e .
```

### GUI Usage (Recommended for Most Users)

```bash
# Method 1: Use the installed command
google-takeout-helper-gui

# Method 2: Run as module
python -m google_takeout_live_photos.gui

# Method 3: Use the launcher script
python scripts/launch_gui.py

# Method 4: Backward compatibility
python google_takeout_live_photos_helper.py --gui
```

### Command Line Usage

```bash
# Method 1: Use the installed command
google-takeout-helper --root ./Takeout --out-pairs ./pairs --out-leftovers ./leftovers

# Method 2: Run as module  
python -m google_takeout_live_photos.cli --root ./Takeout --out-pairs ./pairs --out-leftovers ./leftovers

# Method 3: Backward compatibility
python google_takeout_live_photos_helper.py --root ./Takeout --out-pairs ./pairs --out-leftovers ./leftovers
```

## 📁 Project Structure

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

## 📖 Detailed Usage

### GUI Features

The graphical interface provides:

- **📁 Easy Directory Selection**: Browse and select directories with file dialogs
- **⚙️ Visual Options**: Checkboxes and controls for all processing options
- **📊 Real-time Progress**: Progress bar and live logging during processing
- **🔍 Dry Run Preview**: See what will happen before making changes
- **📈 Results Summary**: Detailed statistics and output locations
- **💡 User-friendly Tips**: Built-in help and guidance

### Command Line Options

```
GUI Mode:
  --gui                    Launch the graphical user interface

CLI Mode Arguments:
  --root PATH              Root directory with unzipped Google Takeout data
  --out-pairs PATH         Output directory for matched Live Photos pairs
  --out-leftovers PATH     Output directory for unmatched media files

Optional Arguments:
  --copy                   Copy files instead of creating symlinks
  --dry-run               Show what would be done without making changes
  --verbose               Enable verbose logging
  --live-max-seconds N    Maximum video duration for cross-folder pairing (default: 6.0)
  --dedupe-leftovers      Skip duplicate files in leftovers based on content hash
```

### Multiple Ways to Run

#### 1. As Installed Package (Recommended)
```bash
# After pip install -e .
google-takeout-helper --gui
google-takeout-helper --root ./Takeout --out-pairs ./pairs --out-leftovers ./leftovers
```

#### 2. As Python Module
```bash
python -m google_takeout_live_photos.cli --gui
python -m google_takeout_live_photos.gui  # GUI only
```

#### 3. Direct Script Execution
```bash
python scripts/launch_gui.py  # GUI launcher
python google_takeout_live_photos_helper.py --gui  # Backward compatibility
```

## 🛠️ Development

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

## 🐛 Troubleshooting

### Common Issues

**"Module not found" errors**
- Ensure you're running from the project root
- Install in development mode: `pip install -e .`
- Set PYTHONPATH: `export PYTHONPATH=src:$PYTHONPATH`

**"ffprobe not found"**
- Install FFmpeg: `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Ubuntu)
- Or disable duration checking with `--live-max-seconds 0`

**GUI won't launch**
- Ensure tkinter is installed: `python -c "import tkinter"`
- On Linux: `sudo apt install python3-tk`
- Use CLI mode as fallback

## 🤝 Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the absolute pain the ass live photos from Google Takeout is
- Uses FFmpeg for video analysis