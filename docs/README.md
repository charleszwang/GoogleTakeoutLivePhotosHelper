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

# Install (optional - can also run directly)
pip install .
```

### GUI Usage (Recommended for Most Users)

```bash
# Launch the user-friendly GUI
python google_takeout_live_photos_helper.py --gui

# Or use the dedicated launcher
python launch_gui.py

# Or double-click launch_gui.py in your file manager
```

### Command Line Usage

```bash
# Basic usage with symlinks (recommended for speed)
python google_takeout_live_photos_helper.py --root ./Takeout --out-pairs ./pairs --out-leftovers ./leftovers

# Copy files instead of symlinking (better for some file managers)
python google_takeout_live_photos_helper.py --root ./Takeout --out-pairs ./pairs --out-leftovers ./leftovers --copy

# Dry run to see what would happen
python google_takeout_live_photos_helper.py --root ./Takeout --out-pairs ./pairs --out-leftovers ./leftovers --dry-run --verbose
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

![GUI Screenshot](screenshot.png) *(Screenshot coming soon)*

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

### Examples

#### GUI Mode (Recommended)
```bash
# Launch GUI for easy, visual processing
python google_takeout_live_photos_helper.py --gui
```

#### Process Google Takeout with all features (CLI)
```bash
python google_takeout_live_photos_helper.py \
  --root ~/Downloads/takeout-20231201T120000Z-001/Takeout \
  --out-pairs ~/Pictures/LivePhotos \
  --out-leftovers ~/Pictures/OtherMedia \
  --copy \
  --verbose \
  --dedupe-leftovers
```

#### Quick preview without making changes (CLI)
```bash
python google_takeout_live_photos_helper.py \
  --root ./Takeout \
  --out-pairs ./pairs \
  --out-leftovers ./leftovers \
  --dry-run \
  --verbose
```

## 📁 Output Structure

### Pairs Directory
Matched Live Photos are organized with numbered prefixes:
```
pairs/
├── 00001_IMG_1234__STILL.HEIC
├── 00001_IMG_1234__VIDEO.MOV
├── 00002_IMG_5678__STILL.JPG
├── 00002_IMG_5678__VIDEO.MP4
├── manifest_pairs.tsv
└── ...
```

### Leftovers Directory
Unmatched media files:
```
leftovers/
├── L000001__IMG_9999.JPG
├── L000002__VID_0123.MP4
├── L000003__Screenshot_2023.PNG
├── manifest_leftovers.tsv
└── ...
```

### Manifest Files

**manifest_pairs.tsv** tracks all paired files:
```
pair_id	match_type	basename	still_src	video_src	still_out	video_out
00001_IMG_1234	same_dir	IMG_1234	/path/to/IMG_1234.HEIC	/path/to/IMG_1234.MOV	/pairs/00001_IMG_1234__STILL.HEIC	/pairs/00001_IMG_1234__VIDEO.MOV
```

**manifest_leftovers.tsv** tracks all leftover files:
```
left_id	action	src	out_or_reason
L000001	COPIED	/path/to/IMG_9999.JPG	/leftovers/L000001__IMG_9999.JPG
L000002	SKIP_DUP	/path/to/duplicate.JPG	duplicate-of-pairs-or-leftovers
```

## 🔧 Advanced Features

### Matching Algorithm

The tool uses a two-pass matching algorithm:

1. **Pass A - Same Directory**: Exact 1:1 matching within the same directory
   - `IMG_1234.HEIC` + `IMG_1234.MOV` in `/Photos/2023/January/`

2. **Pass B - Cross Directory**: Exact 1:1 matching across different directories
   - `IMG_1234.HEIC` in `/Photos/2023/January/` + `IMG_1234.MOV` in `/Photos/2023/January/Videos/`
   - Optional duration filtering (default: ≤6 seconds for "Live Photo-like" videos)

### Deduplication

When `--dedupe-leftovers` is enabled:
- Files are hashed using SHA1
- Leftovers that match paired files are skipped
- Duplicate leftovers are skipped (first occurrence wins)

### File Handling

- **Symlinks** (default): Fast, space-efficient, preserves original files
- **Copy** (`--copy`): Slower but works better with some file managers and cloud sync

## 🛠️ Development

### Setting up Development Environment

```bash
# Clone and setup
git clone https://github.com/yourusername/google-takeout-live-photos-helper.git
cd google-takeout-live-photos-helper

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=stage_pairs_flat --cov-report=html

# Run specific test
pytest tests/test_basic_functionality.py -v
```

### Code Quality

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

# Manual quality checks
black google_takeout_live_photos_helper.py gui.py
pylint google_takeout_live_photos_helper.py
mypy google_takeout_live_photos_helper.py
flake8 google_takeout_live_photos_helper.py gui.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass and code is properly formatted
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

**"ffprobe not found"**
- Install FFmpeg: `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Ubuntu)
- Or disable duration checking with `--live-max-seconds 0`

**"Permission denied" errors**
- Ensure you have write permissions to output directories
- Try using `--copy` instead of symlinks

**"No pairs found"**
- Check that your Takeout directory structure is correct
- Use `--verbose --dry-run` to see what files are being scanned
- Verify file extensions are supported (HEIC, JPG, JPEG, PNG, MOV, MP4)

**GUI won't launch**
- Ensure tkinter is installed: `python -c "import tkinter"`
- On Linux: `sudo apt install python3-tk`
- Use CLI mode as fallback: `python google_takeout_live_photos_helper.py --help`

### Getting Help

- Check the [Issues](https://github.com/yourusername/google-takeout-live-photos-helper/issues) page
- Create a new issue with:
  - Your command line
  - Error messages
  - Sample directory structure (without personal info)

## 🙏 Acknowledgments

- Inspired by the absolute pain the ass live photos from Google Takeout is
- Uses FFmpeg for video analysis
