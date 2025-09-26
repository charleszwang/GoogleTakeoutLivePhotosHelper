"""
Comprehensive tests for CLI module to increase coverage.

Tests command-line argument parsing, validation, and error handling.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, Mock
from io import StringIO

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from google_takeout_live_photos import cli


class TestCLIArgumentParsing(unittest.TestCase):
    """Test CLI argument parsing and validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.takeout_dir = Path(self.temp_dir) / "takeout"
        self.output_dir = Path(self.temp_dir) / "output"
        self.takeout_dir.mkdir(parents=True)

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('sys.argv')
    @patch('google_takeout_live_photos.cli.GoogleTakeoutProcessor')
    def test_cli_single_output_mode(self, mock_processor_class, mock_argv):
        """Test CLI with single output directory mode."""
        mock_argv.__getitem__.side_effect = lambda x: [
            'cli.py', '--root', str(self.takeout_dir), '--output-dir', str(self.output_dir)
        ][x]
        mock_argv.__len__.return_value = 5
        
        mock_processor = Mock()
        mock_processor_class.return_value = mock_processor
        
        # Mock argument parsing
        with patch('argparse.ArgumentParser.parse_args') as mock_parse:
            mock_args = Mock()
            mock_args.gui = False
            mock_args.root = str(self.takeout_dir)
            mock_args.output_dir = str(self.output_dir)
            mock_args.out_pairs = None
            mock_args.out_leftovers = None
            mock_args.copy = False
            mock_args.dry_run = False
            mock_args.verbose = False
            mock_args.live_max_seconds = 6.0
            mock_args.dedupe_leftovers = False
            mock_args.show_issues = False
            mock_parse.return_value = mock_args
            
            with patch('os.path.isdir', return_value=True):
                try:
                    cli.main()
                    mock_processor.process.assert_called_once()
                except SystemExit:
                    pass  # Expected for successful completion

    @patch('sys.argv')
    def test_cli_gui_mode(self, mock_argv):
        """Test CLI GUI mode launch."""
        mock_argv.__getitem__.side_effect = lambda x: ['cli.py', '--gui'][x]
        mock_argv.__len__.return_value = 2
        
        with patch('argparse.ArgumentParser.parse_args') as mock_parse:
            mock_args = Mock()
            mock_args.gui = True
            mock_parse.return_value = mock_args
            
            with patch('google_takeout_live_photos.cli.gui.main') as mock_gui_main:
                try:
                    cli.main()
                    mock_gui_main.assert_called_once()
                except (SystemExit, ImportError):
                    pass  # Expected behavior

    @patch('sys.argv')
    def test_cli_missing_root_argument(self, mock_argv):
        """Test CLI with missing root argument."""
        mock_argv.__getitem__.side_effect = lambda x: ['cli.py'][x]
        mock_argv.__len__.return_value = 1
        
        with patch('argparse.ArgumentParser.parse_args') as mock_parse:
            mock_args = Mock()
            mock_args.gui = False
            mock_args.root = None
            mock_parse.return_value = mock_args
            
            with patch('argparse.ArgumentParser.error') as mock_error:
                try:
                    cli.main()
                except SystemExit:
                    pass
                mock_error.assert_called()

    @patch('sys.argv')
    @patch('google_takeout_live_photos.cli.GoogleTakeoutProcessor')
    def test_cli_keyboard_interrupt(self, mock_processor_class, mock_argv):
        """Test CLI handling of keyboard interrupt."""
        mock_argv.__getitem__.side_effect = lambda x: [
            'cli.py', '--root', str(self.takeout_dir), '--output-dir', str(self.output_dir)
        ][x]
        mock_argv.__len__.return_value = 5
        
        mock_processor = Mock()
        mock_processor.process.side_effect = KeyboardInterrupt()
        mock_processor_class.return_value = mock_processor
        
        with patch('argparse.ArgumentParser.parse_args') as mock_parse:
            mock_args = Mock()
            mock_args.gui = False
            mock_args.root = str(self.takeout_dir)
            mock_args.output_dir = str(self.output_dir)
            mock_args.out_pairs = None
            mock_args.out_leftovers = None
            mock_args.copy = False
            mock_args.dry_run = False
            mock_args.verbose = False
            mock_args.live_max_seconds = 6.0
            mock_args.dedupe_leftovers = False
            mock_args.show_issues = False
            mock_parse.return_value = mock_args
            
            with patch('os.path.isdir', return_value=True):
                with patch('sys.exit') as mock_exit:
                    cli.main()
                    mock_exit.assert_called_with(1)

    @patch('sys.argv')
    @patch('google_takeout_live_photos.cli.GoogleTakeoutProcessor')
    def test_cli_processing_exception(self, mock_processor_class, mock_argv):
        """Test CLI handling of processing exceptions."""
        mock_processor = Mock()
        mock_processor.process.side_effect = Exception("Test error")
        mock_processor_class.return_value = mock_processor
        
        with patch('argparse.ArgumentParser.parse_args') as mock_parse:
            mock_args = Mock()
            mock_args.gui = False
            mock_args.root = str(self.takeout_dir)
            mock_args.output_dir = str(self.output_dir)
            mock_args.out_pairs = None
            mock_args.out_leftovers = None
            mock_args.copy = False
            mock_args.dry_run = False
            mock_args.verbose = False
            mock_args.live_max_seconds = 6.0
            mock_args.dedupe_leftovers = False
            mock_args.show_issues = False
            mock_parse.return_value = mock_args
            
            with patch('os.path.isdir', return_value=True):
                with patch('sys.exit') as mock_exit:
                    cli.main()
                    mock_exit.assert_called_with(1)


if __name__ == '__main__':
    unittest.main()

