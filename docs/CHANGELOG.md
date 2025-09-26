# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-XX-XX

### Added
- **🎉 Initial release of Google Takeout Live Photos Helper**
- **🖥️ User-friendly GUI interface** with tkinter
  - Easy directory selection with file dialogs
  - Visual options and controls
  - Real-time progress tracking and logging
  - Results summary with statistics
  - Dry-run preview functionality
- **🔧 Two-pass matching algorithm** for Live Photos pairs
  - Same-directory exact name matching
  - Cross-directory exact name matching with duration filtering
- **📁 Flat directory organization** with numbered prefixes
- **📊 Comprehensive manifest files** (TSV format)
- **🔄 Content-based deduplication** using SHA1 hashes
- **💾 Flexible file handling** (symlinks or copying)
- **🧪 Dry-run mode** for testing without changes
- **📝 Verbose logging** option
- **🎨 Multiple format support**
  - Images: HEIC, JPG, JPEG, PNG
  - Videos: MOV, MP4
- **⏱️ Video duration filtering** using FFmpeg/ffprobe
- **✅ Comprehensive code quality tools** (Python's rubocop equivalent)
  - Pre-commit hooks with multiple linters
  - Black code formatting
  - Pylint static analysis
  - MyPy type checking
  - Bandit security scanning
  - Safety dependency checking
  - Makefile for easy quality checks

### Technical Details
- **🐍 Python 3.8+ support** with comprehensive type hints
- **🏗️ Object-oriented architecture** with GoogleTakeoutProcessor class
- **🛡️ Robust error handling** and logging
- **⚡ Performance optimized** for large datasets
- **💾 Memory efficient** processing
- **🧪 Comprehensive test coverage** (unit + integration + GUI tests)
- **📦 Professional packaging** with pyproject.toml
- **🔄 CI/CD pipeline** with GitHub Actions
- **🌍 Cross-platform support** (Windows, macOS, Linux)

### User Experience
- **🚀 Multiple launch options**:
  - GUI mode: `python google_takeout_live_photos_helper.py --gui`
  - CLI mode: `python google_takeout_live_photos_helper.py --root ...`
  - Dedicated launcher: `python launch_gui.py`
- **📖 Detailed documentation** with usage examples
- **🤝 Contributing guidelines** for open source development
- **📚 API documentation** with comprehensive docstrings
- **🔧 Installation and setup** instructions
- **🐛 Troubleshooting guide** with common solutions

### Files Structure
- `google_takeout_live_photos_helper.py` - Main CLI application
- `gui.py` - Graphical user interface
- `launch_gui.py` - Simple GUI launcher
- `tests/` - Comprehensive test suite
- `Makefile` - Code quality automation
- `.pre-commit-config.yaml` - Pre-commit hooks configuration
- `.pylintrc` - Pylint configuration
