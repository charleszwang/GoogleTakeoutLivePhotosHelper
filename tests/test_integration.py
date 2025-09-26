"""
Integration tests for the Google Takeout Live Photos Helper.

End-to-end tests that verify the complete workflow from command-line
invocation through file processing and output generation.
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow."""

    def setUp(self):
        """Set up test fixtures with realistic directory structure."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.takeout_dir = self.temp_dir / "Takeout"
        self.pairs_dir = self.temp_dir / "pairs"
        self.leftovers_dir = self.temp_dir / "leftovers"
        
        # Create realistic Google Takeout structure
        photos_dir = self.takeout_dir / "Google Photos"
        photos_2023 = photos_dir / "Photos from 2023"
        photos_2023.mkdir(parents=True)
        
        # Create Live Photo pairs (same directory)
        self.create_file(photos_2023 / "IMG_1234.HEIC", b"fake image data 1")
        self.create_file(photos_2023 / "IMG_1234.MOV", b"fake video data 1")
        
        # Create Live Photo pairs (cross directory) 
        videos_dir = photos_2023 / "Videos"
        videos_dir.mkdir()
        self.create_file(photos_2023 / "IMG_5678.JPG", b"fake image data 2")
        self.create_file(videos_dir / "IMG_5678.MP4", b"fake video data 2")
        
        # Create standalone files
        self.create_file(photos_2023 / "IMG_9999.PNG", b"standalone image")
        self.create_file(videos_dir / "VID_0123.MOV", b"standalone video")
        
        # Create duplicate file for dedup testing
        self.create_file(photos_2023 / "IMG_DUPLICATE.JPG", b"fake image data 1")  # Same content as IMG_1234.HEIC
        
        # Create non-media file
        self.create_file(photos_2023 / "metadata.json", b'{"info": "test"}')

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def create_file(self, path: Path, content: bytes):
        """Helper to create a file with content."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    def run_tool(self, extra_args=None):
        """Helper to run the tool with test directories."""
        # Use the new modular approach
        src_path = Path(__file__).parent.parent / "src"
        
        cmd = [
            sys.executable, "-m", "google_takeout_live_photos.cli",
            "--root", str(self.takeout_dir),
            "--out-pairs", str(self.pairs_dir),
            "--out-leftovers", str(self.leftovers_dir)
        ]
        
        # Add src to PYTHONPATH for the subprocess
        env = os.environ.copy()
        env['PYTHONPATH'] = str(src_path) + os.pathsep + env.get('PYTHONPATH', '')
        
        if extra_args:
            cmd.extend(extra_args)
        
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
        return result

    def test_basic_workflow(self):
        """Test the complete workflow without special options."""
        result = self.run_tool()
        
        self.assertEqual(result.returncode, 0, f"Tool failed: {result.stderr}")
        
        # Check that pairs directory was created with expected files
        self.assertTrue(self.pairs_dir.exists())
        pair_files = list(self.pairs_dir.glob("*"))
        
        # Should have 2 pairs (4 files) + 1 manifest = 5 files
        self.assertEqual(len(pair_files), 5)
        
        # Check manifest exists
        manifest = self.pairs_dir / "manifest_pairs.tsv"
        self.assertTrue(manifest.exists())
        
        # Check leftovers directory
        self.assertTrue(self.leftovers_dir.exists())
        leftover_files = list(self.leftovers_dir.glob("L*"))
        
        # Should have standalone files
        self.assertGreaterEqual(len(leftover_files), 2)

    def test_dry_run(self):
        """Test dry run mode."""
        result = self.run_tool(["--dry-run", "--verbose"])
        
        self.assertEqual(result.returncode, 0)
        
        # No directories should be created in dry run
        self.assertFalse(self.pairs_dir.exists())
        self.assertFalse(self.leftovers_dir.exists())
        
        # Should mention dry run in output
        self.assertIn("dry run", result.stdout)

    def test_copy_mode(self):
        """Test copy mode instead of symlinks."""
        result = self.run_tool(["--copy"])
        
        self.assertEqual(result.returncode, 0)
        
        # Check that files were copied (not symlinked)
        pair_files = list(self.pairs_dir.glob("*__STILL*"))
        if pair_files:
            # At least one file should exist and not be a symlink
            self.assertFalse(pair_files[0].is_symlink())

    def test_deduplication(self):
        """Test deduplication feature."""
        result = self.run_tool(["--dedupe-leftovers", "--copy"])
        
        self.assertEqual(result.returncode, 0)
        
        # Check leftovers manifest for skip entries
        leftovers_manifest = self.leftovers_dir / "manifest_leftovers.tsv"
        if leftovers_manifest.exists():
            content = leftovers_manifest.read_text()
            # Should have some SKIP_DUP entries due to duplicate content
            self.assertIn("SKIP_DUP", content)

    def test_verbose_output(self):
        """Test verbose output."""
        result = self.run_tool(["--verbose", "--dry-run"])
        
        self.assertEqual(result.returncode, 0)
        
        # Verbose mode should produce more detailed output
        self.assertIn("[pair:", result.stdout)
        self.assertGreater(len(result.stdout), 100)  # Should be substantial output

    def test_duration_filtering(self):
        """Test video duration filtering."""
        # This test requires ffprobe to be available
        result = self.run_tool(["--live-max-seconds", "1.0", "--dry-run"])
        
        # Should not fail even if ffprobe is not available
        self.assertEqual(result.returncode, 0)

    def test_invalid_root_directory(self):
        """Test handling of invalid root directory."""
        src_path = Path(__file__).parent.parent / "src"
        env = os.environ.copy()
        env['PYTHONPATH'] = str(src_path) + os.pathsep + env.get('PYTHONPATH', '')
        
        cmd = [
            sys.executable, "-m", "google_takeout_live_photos.cli",
            "--root", "/nonexistent/directory",
            "--out-pairs", str(self.pairs_dir),
            "--out-leftovers", str(self.leftovers_dir)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not exist", result.stderr)

    def test_manifest_content(self):
        """Test that manifest files contain expected content."""
        result = self.run_tool(["--copy"])
        
        self.assertEqual(result.returncode, 0)
        
        # Check pairs manifest
        pairs_manifest = self.pairs_dir / "manifest_pairs.tsv"
        self.assertTrue(pairs_manifest.exists())
        
        content = pairs_manifest.read_text()
        lines = content.strip().split('\n')
        
        # Should have header + data lines
        self.assertGreater(len(lines), 1)
        self.assertIn("pair_id", lines[0])  # Header
        self.assertIn("match_type", lines[0])
        
        # Check leftovers manifest
        leftovers_manifest = self.leftovers_dir / "manifest_leftovers.tsv"
        self.assertTrue(leftovers_manifest.exists())
        
        content = leftovers_manifest.read_text()
        lines = content.strip().split('\n')
        
        self.assertGreater(len(lines), 1)
        self.assertIn("left_id", lines[0])  # Header
        self.assertIn("action", lines[0])


if __name__ == '__main__':
    unittest.main()
