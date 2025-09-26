# Contributing to Google Takeout Live Photos Helper

Thank you for your interest in contributing! This document outlines the process for contributing to this project.

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/google-takeout-live-photos-helper.git
   cd google-takeout-live-photos-helper
   ```

2. **Set up Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements-dev.txt
   ```

3. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

## Making Changes

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Run Tests**
   ```bash
   # Run all tests
   pytest

   # Run with coverage
   pytest --cov=stage_pairs_flat --cov-report=html

   # Run specific test
   pytest tests/test_processor.py::TestGoogleTakeoutProcessor::test_initialization -v
   ```

4. **Check Code Quality**
   ```bash
   # Run all quality checks
   make all

   # Or individual checks
   make format                    # Format code
   make lint                      # Run linting tools  
   make security                  # Security checks
   make test                      # Run tests

   # Manual checks
   black google_takeout_live_photos_helper.py gui.py tests/
   mypy google_takeout_live_photos_helper.py gui.py
   flake8 google_takeout_live_photos_helper.py gui.py tests/
   pylint google_takeout_live_photos_helper.py gui.py
   ```

## Code Standards

### Python Style
- Follow PEP 8
- Use Black for code formatting (line length: 100)
- Use type hints for all function parameters and return values
- Write descriptive docstrings for classes and methods

### Testing
- Write unit tests for all new functionality
- Maintain or improve test coverage
- Use descriptive test names that explain what is being tested
- Include both positive and negative test cases

### Documentation
- Update README.md for user-facing changes
- Add docstrings to new classes and methods
- Include examples for complex functionality

## Submitting Changes

1. **Ensure All Tests Pass**
   ```bash
   make all  # Runs format, lint, security, and tests
   
   # Or manually:
   pytest
   flake8 google_takeout_live_photos_helper.py gui.py
   mypy google_takeout_live_photos_helper.py gui.py
   pylint google_takeout_live_photos_helper.py gui.py
   ```

2. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add feature: descriptive commit message"
   ```

3. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request**
   - Use a descriptive title
   - Explain what changes you made and why
   - Reference any related issues
   - Include screenshots for UI changes

## Pull Request Guidelines

### Title Format
Use one of these prefixes:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test additions/changes
- `refactor:` for code refactoring
- `chore:` for maintenance tasks

### Description Template
```markdown
## Description
Brief description of the changes.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
```

## Issue Reporting

### Bug Reports
Please include:
- Python version
- Operating system
- Command line used
- Expected behavior
- Actual behavior
- Error messages (full stack trace)
- Sample directory structure (anonymized)

### Feature Requests
Please include:
- Clear description of the feature
- Use case/motivation
- Proposed implementation (if you have ideas)
- Any alternatives considered

## Development Tips

### Testing with Real Data
Create a test directory structure:
```
test_takeout/
├── Google Photos/
│   ├── Photos from 2023/
│   │   ├── IMG_001.HEIC
│   │   ├── IMG_001.MOV
│   │   └── IMG_002.JPG
│   └── Videos/
│       └── VID_003.MP4
```

### Debugging
Use verbose mode for debugging:
```bash
python stage_pairs_flat.py --root test_takeout --out-pairs pairs --out-leftovers leftovers --verbose --dry-run
```

### Performance Testing
For large datasets, consider:
- Memory usage with many files
- Processing time for deep directory structures
- I/O performance with different storage types

## Code Architecture

### Key Components
- `GoogleTakeoutProcessor`: Main processing class
- `scan_media_files()`: File discovery and indexing
- `find_pairs()`: Matching algorithm
- `process_pairs()` / `process_leftovers()`: File staging

### Design Principles
- **Separation of concerns**: Each method has a single responsibility
- **Testability**: Methods are pure functions where possible
- **Error handling**: Graceful failure with informative messages
- **Performance**: Efficient algorithms for large datasets

## Questions?

Feel free to:
- Open an issue for discussion
- Join our discussions in GitHub Discussions
- Contact the maintainers

Thank you for contributing!
