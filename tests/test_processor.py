"""
Unit tests for GoogleTakeoutProcessor class.
"""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, mock_open

import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from google_takeout_live_photos.processor import GoogleTakeoutProcessor, STILL_EXTENSIONS, VIDEO_EXTENSIONS


class TestGoogleTakeoutProcessor(unittest.TestCase):
    """Test cases for GoogleTakeoutProcessor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.root_dir = Path(self.temp_dir) / "takeout"
        self.pairs_dir = Path(self.temp_dir) / "pairs"
        self.leftovers_dir = Path(self.temp_dir) / "leftovers"
        
        # Create test directory structure
        self.root_dir.mkdir(parents=True)
        
        self.processor = GoogleTakeoutProcessor(
            root_dir=self.root_dir,
            pairs_dir=self.pairs_dir,
            leftovers_dir=self.leftovers_dir,
            dry_run=True,  # Use dry run for most tests
            verbose=False
        )

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initialization(self):
        """Test processor initialization."""
        self.assertEqual(self.processor.root_dir, self.root_dir)
        self.assertEqual(self.processor.pairs_dir, self.pairs_dir)
        self.assertEqual(self.processor.leftovers_dir, self.leftovers_dir)
        self.assertTrue(self.processor.dry_run)
        self.assertFalse(self.processor.verbose)
        self.assertEqual(self.processor.max_video_duration, 6.0)

    def test_calculate_sha1(self):
        """Test SHA1 calculation."""
        test_file = self.root_dir / "test.txt"
        test_content = b"Hello, World!"
        test_file.write_bytes(test_content)
        
        expected_hash = "0a0a9f2a6772942557ab5355d76af442f8f65e01"  # SHA1 of "Hello, World!"
        actual_hash = GoogleTakeoutProcessor.calculate_sha1(test_file)
        self.assertEqual(actual_hash, expected_hash)

    def test_calculate_sha1_file_not_found(self):
        """Test SHA1 calculation with non-existent file."""
        non_existent = self.root_dir / "nonexistent.txt"
        with self.assertRaises(IOError):
            GoogleTakeoutProcessor.calculate_sha1(non_existent)

    @patch('subprocess.run')
    def test_get_video_duration_success(self, mock_run):
        """Test successful video duration extraction."""
        mock_run.return_value.stdout = "5.5\n"
        
        duration = GoogleTakeoutProcessor.get_video_duration("test.mov")
        self.assertEqual(duration, 5.5)
        
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_get_video_duration_failure(self, mock_run):
        """Test video duration extraction failure."""
        mock_run.side_effect = FileNotFoundError()
        
        duration = GoogleTakeoutProcessor.get_video_duration("test.mov")
        self.assertIsNone(duration)

    def test_scan_media_files_empty_directory(self):
        """Test scanning an empty directory."""
        by_dir_base, stills_by_base, videos_by_base = self.processor.scan_media_files()
        
        self.assertEqual(len(by_dir_base), 0)
        self.assertEqual(len(stills_by_base), 0)
        self.assertEqual(len(videos_by_base), 0)
        self.assertEqual(self.processor.stats['total_scanned'], 0)

    def test_scan_media_files_with_files(self):
        """Test scanning directory with media files."""
        # Create test files
        (self.root_dir / "IMG_001.HEIC").touch()
        (self.root_dir / "IMG_001.MOV").touch()
        (self.root_dir / "IMG_002.JPG").touch()
        (self.root_dir / "document.pdf").touch()  # Non-media file
        
        by_dir_base, stills_by_base, videos_by_base = self.processor.scan_media_files()
        
        # Check stats
        self.assertEqual(self.processor.stats['total_scanned'], 4)  # All files scanned
        
        # Check indexing
        self.assertEqual(len(stills_by_base), 2)  # IMG_001, IMG_002
        self.assertEqual(len(videos_by_base), 1)   # IMG_001
        
        self.assertIn("IMG_001", stills_by_base)
        self.assertIn("IMG_002", stills_by_base)
        self.assertIn("IMG_001", videos_by_base)

    def test_find_pairs_same_directory(self):
        """Test finding pairs in the same directory."""
        # Create test structure
        (self.root_dir / "IMG_001.HEIC").touch()
        (self.root_dir / "IMG_001.MOV").touch()
        (self.root_dir / "IMG_002.JPG").touch()  # No matching video
        
        by_dir_base, stills_by_base, videos_by_base = self.processor.scan_media_files()
        pairs, used_files = self.processor.find_pairs(by_dir_base, stills_by_base, videos_by_base)
        
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][0], "same_dir")  # match_type
        self.assertEqual(pairs[0][1], "IMG_001")   # base_name
        self.assertEqual(len(used_files), 2)

    def test_find_pairs_cross_directory(self):
        """Test finding pairs across directories."""
        # Create test structure
        subdir = self.root_dir / "subdir"
        subdir.mkdir()
        
        (self.root_dir / "IMG_001.HEIC").touch()
        (subdir / "IMG_001.MOV").touch()
        
        by_dir_base, stills_by_base, videos_by_base = self.processor.scan_media_files()
        pairs, used_files = self.processor.find_pairs(by_dir_base, stills_by_base, videos_by_base)
        
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][0], "cross_dir")  # match_type
        self.assertEqual(pairs[0][1], "IMG_001")    # base_name

    @patch.object(GoogleTakeoutProcessor, 'get_video_duration')
    def test_find_pairs_duration_filter(self, mock_duration):
        """Test duration filtering for cross-directory pairs."""
        # Setup processor with duration limit
        self.processor.max_video_duration = 5.0
        
        # Create test structure
        subdir = self.root_dir / "subdir"
        subdir.mkdir()
        
        (self.root_dir / "IMG_001.HEIC").touch()
        (subdir / "IMG_001.MOV").touch()
        (self.root_dir / "IMG_002.HEIC").touch()
        (subdir / "IMG_002.MOV").touch()
        
        # Mock duration responses
        def duration_side_effect(path):
            if "IMG_001" in str(path):
                return 3.0  # Under limit
            else:
                return 10.0  # Over limit
        
        mock_duration.side_effect = duration_side_effect
        
        by_dir_base, stills_by_base, videos_by_base = self.processor.scan_media_files()
        pairs, used_files = self.processor.find_pairs(by_dir_base, stills_by_base, videos_by_base)
        
        # Only IMG_001 should be paired (under duration limit)
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][1], "IMG_001")

    def test_safe_link_or_copy_dry_run(self):
        """Test safe_link_or_copy in dry run mode."""
        src = self.root_dir / "source.txt"
        dst = self.root_dir / "dest.txt"
        src.write_text("test content")
        
        # Should not create destination file in dry run
        self.processor.safe_link_or_copy(src, dst)
        self.assertFalse(dst.exists())

    def test_safe_link_or_copy_real_copy(self):
        """Test safe_link_or_copy with actual copying."""
        processor = GoogleTakeoutProcessor(
            root_dir=self.root_dir,
            pairs_dir=self.pairs_dir,
            leftovers_dir=self.leftovers_dir,
            copy_files=True,
            dry_run=False
        )
        
        src = self.root_dir / "source.txt"
        dst = self.root_dir / "dest.txt"
        src.write_text("test content")
        
        processor.safe_link_or_copy(src, dst)
        
        self.assertTrue(dst.exists())
        self.assertEqual(dst.read_text(), "test content")
        # Should be a copy, not a symlink
        self.assertFalse(dst.is_symlink())


class TestConstants(unittest.TestCase):
    """Test constants and module-level functionality."""

    def test_file_extensions(self):
        """Test file extension constants."""
        self.assertIn(".heic", STILL_EXTENSIONS)
        self.assertIn(".jpg", STILL_EXTENSIONS)
        self.assertIn(".jpeg", STILL_EXTENSIONS)
        self.assertIn(".png", STILL_EXTENSIONS)
        
        self.assertIn(".mov", VIDEO_EXTENSIONS)
        self.assertIn(".mp4", VIDEO_EXTENSIONS)
        
        # Ensure no overlap
        self.assertEqual(len(STILL_EXTENSIONS & VIDEO_EXTENSIONS), 0)


if __name__ == '__main__':
    unittest.main()
