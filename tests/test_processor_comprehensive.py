"""
Comprehensive tests for GoogleTakeoutProcessor to increase coverage.

This test file focuses on testing the methods that aren't covered by the basic tests,
including validation, duplicate detection, and edge cases.
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, Mock

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from google_takeout_live_photos.processor import GoogleTakeoutProcessor


class TestProcessorValidation(unittest.TestCase):
    """Test validation methods in GoogleTakeoutProcessor."""

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
            dry_run=True,
            verbose=True
        )

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_validate_takeout_structure_valid(self):
        """Test validation with valid Google Takeout structure."""
        # Create typical Google Takeout structure
        google_photos_dir = self.root_dir / "Google Photos"
        photos_2023_dir = google_photos_dir / "Photos from 2023"
        photos_2023_dir.mkdir(parents=True)
        
        result = self.processor.validate_takeout_structure()
        self.assertTrue(result)
        self.assertGreater(self.processor.stats['takeout_folders_found'], 0)

    def test_validate_takeout_structure_invalid(self):
        """Test validation with invalid structure."""
        # Create non-Takeout structure
        random_dir = self.root_dir / "random_folder"
        random_dir.mkdir()
        
        result = self.processor.validate_takeout_structure()
        self.assertFalse(result)
        self.assertGreater(len(self.processor.issues['structure_warnings']), 0)

    def test_detect_duplicate_names_stills(self):
        """Test duplicate name detection for still images."""
        stills_by_base = {
            'IMG_001': ['/path1/IMG_001.jpg', '/path2/IMG_001.heic'],
            'IMG_002': ['/path1/IMG_002.png']
        }
        videos_by_base = {}
        
        self.processor.detect_duplicate_names(stills_by_base, videos_by_base)
        
        self.assertEqual(self.processor.stats['duplicate_names'], 1)
        self.assertEqual(len(self.processor.issues['duplicate_names']), 1)
        self.assertEqual(self.processor.issues['duplicate_names'][0]['type'], 'still')
        self.assertEqual(self.processor.issues['duplicate_names'][0]['base_name'], 'IMG_001')

    def test_detect_duplicate_names_videos(self):
        """Test duplicate name detection for videos."""
        stills_by_base = {}
        videos_by_base = {
            'VID_001': ['/path1/VID_001.mov', '/path2/VID_001.mp4'],
            'VID_002': ['/path1/VID_002.mov']
        }
        
        self.processor.detect_duplicate_names(stills_by_base, videos_by_base)
        
        self.assertEqual(self.processor.stats['duplicate_names'], 1)
        self.assertEqual(len(self.processor.issues['duplicate_names']), 1)
        self.assertEqual(self.processor.issues['duplicate_names'][0]['type'], 'video')

    def test_detect_matching_conflicts(self):
        """Test matching conflict detection."""
        stills_by_base = {
            'IMG_001': ['/path1/IMG_001.jpg', '/path2/IMG_001.heic']  # Multiple stills
        }
        videos_by_base = {
            'IMG_001': ['/path1/IMG_001.mov']  # Single video
        }
        
        self.processor.detect_matching_conflicts(stills_by_base, videos_by_base)
        
        self.assertEqual(self.processor.stats['potential_issues'], 1)
        self.assertEqual(len(self.processor.issues['matching_conflicts']), 1)
        conflict = self.processor.issues['matching_conflicts'][0]
        self.assertEqual(conflict['base_name'], 'IMG_001')
        self.assertEqual(conflict['still_count'], 2)
        self.assertEqual(conflict['video_count'], 1)

    @patch.object(GoogleTakeoutProcessor, 'get_video_duration')
    def test_detect_orphaned_videos(self, mock_duration):
        """Test orphaned video detection."""
        mock_duration.return_value = 3.0  # Short video (likely Live Photo)
        
        videos_by_base = {
            'VID_ORPHAN': ['/path/VID_ORPHAN.mov'],
            'VID_NORMAL': ['/path/VID_NORMAL.mov']
        }
        used_files = set()  # No files are used (paired)
        
        # Mock different durations
        def duration_side_effect(path):
            if 'ORPHAN' in str(path):
                return 3.0  # Short video
            else:
                return 30.0  # Long video
        
        mock_duration.side_effect = duration_side_effect
        
        self.processor.detect_orphaned_videos(videos_by_base, used_files)
        
        self.assertEqual(len(self.processor.issues['orphaned_videos']), 1)
        orphan = self.processor.issues['orphaned_videos'][0]
        self.assertEqual(orphan['base_name'], 'VID_ORPHAN')
        self.assertEqual(orphan['duration'], 3.0)

    def test_print_summary_with_warnings(self):
        """Test summary printing with warnings."""
        # Set up some stats and issues
        self.processor.stats['duplicate_names'] = 2
        self.processor.stats['potential_issues'] = 1
        self.processor.issues['orphaned_videos'] = [{'base_name': 'test', 'duration': 3.0}]
        self.processor.issues['structure_warnings'] = ['Test warning']
        
        # This should not raise an exception
        try:
            self.processor.print_summary()
        except Exception as e:
            self.fail(f"print_summary raised an exception: {e}")

    def test_print_detailed_issues(self):
        """Test detailed issues printing."""
        # Set up test issues
        self.processor.issues['duplicate_names'] = [{
            'type': 'still',
            'base_name': 'IMG_001',
            'files': ['/path1/IMG_001.jpg', '/path2/IMG_001.heic'],
            'count': 2
        }]
        self.processor.issues['matching_conflicts'] = [{
            'base_name': 'IMG_002',
            'still_count': 2,
            'video_count': 1,
            'still_files': ['/path1/IMG_002.jpg', '/path2/IMG_002.heic'],
            'video_files': ['/path1/IMG_002.mov']
        }]
        self.processor.issues['orphaned_videos'] = [{
            'base_name': 'VID_ORPHAN',
            'video_path': '/path/VID_ORPHAN.mov',
            'duration': 3.0
        }]
        
        # This should not raise an exception
        try:
            self.processor.print_detailed_issues()
        except Exception as e:
            self.fail(f"print_detailed_issues raised an exception: {e}")


class TestProcessorFileOperations(unittest.TestCase):
    """Test file operation methods."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.root_dir = Path(self.temp_dir) / "takeout"
        self.pairs_dir = Path(self.temp_dir) / "pairs"
        self.leftovers_dir = Path(self.temp_dir) / "leftovers"
        
        self.root_dir.mkdir(parents=True)
        
        self.processor = GoogleTakeoutProcessor(
            root_dir=self.root_dir,
            pairs_dir=self.pairs_dir,
            leftovers_dir=self.leftovers_dir,
            dry_run=False,
            copy_files=True
        )

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_process_pairs_with_files(self):
        """Test processing pairs with actual files."""
        # Create test files
        still_file = self.root_dir / "IMG_001.jpg"
        video_file = self.root_dir / "IMG_001.mov"
        still_file.write_bytes(b"fake image data")
        video_file.write_bytes(b"fake video data")
        
        pairs = [("same_dir", "IMG_001", str(still_file), str(video_file))]
        
        pair_hashes = self.processor.process_pairs(pairs)
        
        # Check that files were processed
        self.assertTrue(self.pairs_dir.exists())
        pair_files = list(self.pairs_dir.glob("*"))
        self.assertGreaterEqual(len(pair_files), 2)  # At least 2 files + manifest

    def test_process_leftovers_with_deduplication(self):
        """Test leftover processing with deduplication."""
        # Create test files
        leftover_file = self.root_dir / "IMG_LEFTOVER.jpg"
        leftover_file.write_bytes(b"unique content")
        
        used_files = set()  # No used files
        pair_hashes = set()  # No pair hashes
        
        # Enable deduplication
        self.processor.dedupe_leftovers = True
        
        self.processor.process_leftovers(used_files, pair_hashes)
        
        # Check that leftovers were processed
        self.assertTrue(self.leftovers_dir.exists())
        leftover_files = list(self.leftovers_dir.glob("L*"))
        self.assertGreaterEqual(len(leftover_files), 1)

    def test_safe_link_or_copy_symlink_mode(self):
        """Test symlink creation mode."""
        processor = GoogleTakeoutProcessor(
            root_dir=self.root_dir,
            pairs_dir=self.pairs_dir,
            leftovers_dir=self.leftovers_dir,
            copy_files=False  # Symlink mode
        )
        
        src = self.root_dir / "source.txt"
        dst = self.pairs_dir / "dest.txt"
        src.write_text("test content")
        
        processor.safe_link_or_copy(src, dst)
        
        self.assertTrue(dst.exists())
        # On systems that support symlinks, this should be a symlink
        # On Windows, it might fall back to copy

    def test_safe_link_or_copy_existing_file(self):
        """Test behavior when destination already exists."""
        src = self.root_dir / "source.txt"
        dst = self.pairs_dir / "dest.txt"
        src.write_text("source content")
        
        # Create destination first
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text("existing content")
        
        self.processor.safe_link_or_copy(src, dst)
        
        # Should not overwrite existing file
        self.assertEqual(dst.read_text(), "existing content")


class TestProcessorEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.root_dir = Path(self.temp_dir) / "takeout"
        self.pairs_dir = Path(self.temp_dir) / "pairs"
        self.leftovers_dir = Path(self.temp_dir) / "leftovers"
        
        self.root_dir.mkdir(parents=True)

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_process_nonexistent_directory(self):
        """Test processing with non-existent root directory."""
        nonexistent_dir = Path(self.temp_dir) / "nonexistent"
        
        processor = GoogleTakeoutProcessor(
            root_dir=nonexistent_dir,
            pairs_dir=self.pairs_dir,
            leftovers_dir=self.leftovers_dir
        )
        
        with self.assertRaises(FileNotFoundError):
            processor.process()

    def test_scan_empty_directory(self):
        """Test scanning an empty directory."""
        processor = GoogleTakeoutProcessor(
            root_dir=self.root_dir,
            pairs_dir=self.pairs_dir,
            leftovers_dir=self.leftovers_dir
        )
        
        by_dir_base, stills_by_base, videos_by_base = processor.scan_media_files()
        
        self.assertEqual(len(by_dir_base), 0)
        self.assertEqual(len(stills_by_base), 0)
        self.assertEqual(len(videos_by_base), 0)

    def test_scan_with_non_media_files(self):
        """Test scanning directory with non-media files."""
        # Create non-media files
        (self.root_dir / "document.pdf").touch()
        (self.root_dir / "readme.txt").touch()
        (self.root_dir / "data.json").touch()
        
        processor = GoogleTakeoutProcessor(
            root_dir=self.root_dir,
            pairs_dir=self.pairs_dir,
            leftovers_dir=self.leftovers_dir
        )
        
        by_dir_base, stills_by_base, videos_by_base = processor.scan_media_files()
        
        # Should ignore non-media files
        self.assertEqual(len(stills_by_base), 0)
        self.assertEqual(len(videos_by_base), 0)
        self.assertGreater(processor.stats['total_scanned'], 0)  # Files were scanned

    @patch.object(GoogleTakeoutProcessor, 'get_video_duration')
    def test_find_pairs_with_duration_filter(self, mock_duration):
        """Test pair finding with video duration filtering."""
        # Create test files
        (self.root_dir / "IMG_001.HEIC").touch()
        (self.root_dir / "IMG_001.MOV").touch()
        (self.root_dir / "IMG_002.HEIC").touch()
        (self.root_dir / "IMG_002.MOV").touch()
        
        # Mock duration responses
        def duration_side_effect(path):
            if "IMG_001" in str(path):
                return 3.0  # Under limit
            else:
                return 10.0  # Over limit
        
        mock_duration.side_effect = duration_side_effect
        
        # Set duration limit
        processor = GoogleTakeoutProcessor(
            root_dir=self.root_dir,
            pairs_dir=self.pairs_dir,
            leftovers_dir=self.leftovers_dir,
            max_video_duration=5.0
        )
        
        by_dir_base, stills_by_base, videos_by_base = processor.scan_media_files()
        pairs, used_files = processor.find_pairs(by_dir_base, stills_by_base, videos_by_base)
        
        # Only IMG_001 should be paired (under duration limit)
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][1], "IMG_001")

    def test_calculate_sha1_large_file(self):
        """Test SHA1 calculation with larger file."""
        test_file = self.root_dir / "large_test.jpg"
        # Create a file larger than one chunk
        test_content = b"A" * (2 * 1024 * 1024)  # 2MB
        test_file.write_bytes(test_content)
        
        hash_result = GoogleTakeoutProcessor.calculate_sha1(test_file)
        
        # Verify it's a valid SHA1 hash
        self.assertEqual(len(hash_result), 40)  # SHA1 is 40 hex characters
        self.assertTrue(all(c in '0123456789abcdef' for c in hash_result))

    def test_calculate_sha1_nonexistent_file(self):
        """Test SHA1 calculation with non-existent file."""
        nonexistent_file = self.root_dir / "nonexistent.jpg"
        
        with self.assertRaises(IOError):
            GoogleTakeoutProcessor.calculate_sha1(nonexistent_file)

    @patch('subprocess.run')
    def test_get_video_duration_timeout(self, mock_run):
        """Test video duration with timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired('ffprobe', 30)
        
        duration = GoogleTakeoutProcessor.get_video_duration("test.mov")
        self.assertIsNone(duration)

    @patch('subprocess.run')
    def test_get_video_duration_invalid_output(self, mock_run):
        """Test video duration with invalid ffprobe output."""
        mock_run.return_value.stdout = "invalid_duration"
        
        duration = GoogleTakeoutProcessor.get_video_duration("test.mov")
        self.assertIsNone(duration)

    def test_process_with_verbose_mode(self):
        """Test processing in verbose mode."""
        # Create a simple test structure
        (self.root_dir / "IMG_001.HEIC").touch()
        (self.root_dir / "IMG_001.MOV").touch()
        
        processor = GoogleTakeoutProcessor(
            root_dir=self.root_dir,
            pairs_dir=self.pairs_dir,
            leftovers_dir=self.leftovers_dir,
            verbose=True,
            dry_run=True
        )
        
        # This should not raise an exception
        try:
            processor.process()
        except Exception as e:
            self.fail(f"Processing in verbose mode failed: {e}")

    def test_process_with_deduplication(self):
        """Test processing with deduplication enabled."""
        # Create duplicate content files
        content = b"duplicate content"
        (self.root_dir / "IMG_001.jpg").write_bytes(content)
        (self.root_dir / "IMG_002.jpg").write_bytes(content)  # Same content
        (self.root_dir / "IMG_003.jpg").write_bytes(b"different content")
        
        processor = GoogleTakeoutProcessor(
            root_dir=self.root_dir,
            pairs_dir=self.pairs_dir,
            leftovers_dir=self.leftovers_dir,
            dedupe_leftovers=True,
            dry_run=True
        )
        
        try:
            processor.process()
            # Should detect duplicates
            self.assertGreaterEqual(processor.stats['total_scanned'], 3)
        except Exception as e:
            self.fail(f"Processing with deduplication failed: {e}")


if __name__ == '__main__':
    unittest.main()
