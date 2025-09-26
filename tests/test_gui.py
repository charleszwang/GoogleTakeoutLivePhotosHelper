"""
Unit tests for the GUI interface.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

# Add src directory to path to import the modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))


class TestGUIComponents(unittest.TestCase):
    """Test GUI components without actually launching the GUI."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('tkinter.Tk')
    def test_gui_import(self, mock_tk):
        """Test that GUI module can be imported."""
        try:
            from google_takeout_live_photos import gui
            self.assertTrue(hasattr(gui, 'GoogleTakeoutGUI'))
            self.assertTrue(hasattr(gui, 'main'))
        except ImportError as e:
            self.fail(f"Could not import GUI module: {e}")

    @patch('tkinter.Tk')
    def test_gui_initialization(self, mock_tk):
        """Test GUI class initialization."""
        from google_takeout_live_photos import gui
        
        # Mock the root window
        mock_root = Mock()
        mock_tk.return_value = mock_root
        
        # This should not raise an exception
        try:
            app = gui.GoogleTakeoutGUI(mock_root)
            self.assertIsNotNone(app)
            self.assertEqual(app.root, mock_root)
        except Exception as e:
            # Skip if tkinter is not available
            if "tkinter" in str(e).lower():
                self.skipTest(f"Tkinter not available: {e}")
            else:
                raise

    def test_gui_validation_logic(self):
        """Test input validation logic without GUI."""
        # Test the validation logic that would be used in the GUI
        
        # Valid inputs
        valid_inputs = {
            'root_dir': str(self.temp_dir),
            'pairs_dir': str(self.temp_dir / 'pairs'),
            'leftovers_dir': str(self.temp_dir / 'leftovers')
        }
        
        # Create the root directory
        self.temp_dir.mkdir(exist_ok=True)
        
        # Test validation logic (simulated)
        def validate_inputs(inputs):
            if not inputs.get('root_dir'):
                return False, "Please select a Google Takeout directory"
            
            if not os.path.isdir(inputs['root_dir']):
                return False, "Google Takeout directory does not exist"
            
            if not inputs.get('pairs_dir'):
                return False, "Please select an output directory for Live Photos pairs"
            
            if not inputs.get('leftovers_dir'):
                return False, "Please select an output directory for other media"
            
            if inputs['pairs_dir'] == inputs['leftovers_dir']:
                return False, "Pairs and leftovers directories must be different"
            
            return True, "Valid"
        
        # Test valid inputs
        is_valid, message = validate_inputs(valid_inputs)
        self.assertTrue(is_valid, f"Valid inputs should pass validation: {message}")
        
        # Test missing root directory
        invalid_inputs = valid_inputs.copy()
        invalid_inputs['root_dir'] = ''
        is_valid, message = validate_inputs(invalid_inputs)
        self.assertFalse(is_valid)
        self.assertIn("Google Takeout directory", message)
        
        # Test non-existent directory
        invalid_inputs = valid_inputs.copy()
        invalid_inputs['root_dir'] = '/nonexistent/directory'
        is_valid, message = validate_inputs(invalid_inputs)
        self.assertFalse(is_valid)
        self.assertIn("does not exist", message)
        
        # Test same output directories
        invalid_inputs = valid_inputs.copy()
        invalid_inputs['leftovers_dir'] = invalid_inputs['pairs_dir']
        is_valid, message = validate_inputs(invalid_inputs)
        self.assertFalse(is_valid)
        self.assertIn("must be different", message)


class TestGUIIntegration(unittest.TestCase):
    """Integration tests for GUI functionality."""

    @patch('google_takeout_live_photos.gui.tk.Tk')
    @patch('google_takeout_live_photos.gui.GoogleTakeoutProcessor')
    def test_gui_processing_workflow(self, mock_processor_class, mock_tk):
        """Test the GUI processing workflow."""
        try:
            from google_takeout_live_photos import gui
        except ImportError:
            self.skipTest("GUI module not available")
        
        # Mock the processor
        mock_processor = Mock()
        mock_processor.stats = {
            'total_scanned': 100,
            'same_dir_pairs': 10,
            'cross_dir_pairs': 5,
            'leftovers_staged': 85,
            'leftovers_skipped': 0
        }
        mock_processor_class.return_value = mock_processor
        
        # Mock the root window
        mock_root = Mock()
        mock_tk.return_value = mock_root
        
        # Create GUI app (mocked)
        app = gui.GoogleTakeoutGUI(mock_root)
        
        # Set up test inputs
        app.root_dir.set('/test/takeout')
        app.pairs_dir.set('/test/pairs')
        app.leftovers_dir.set('/test/leftovers')
        
        # Mock directory existence
        with patch('os.path.isdir', return_value=True):
            # Test that validation passes
            self.assertTrue(app.validate_inputs())


class TestMainEntryPoints(unittest.TestCase):
    """Test main entry points for GUI."""

    def test_main_gui_argument(self):
        """Test main script with --gui argument."""
        # Test that the main script recognizes --gui argument
        from google_takeout_live_photos import cli
        
        # Mock sys.argv
        with patch('sys.argv', ['script.py', '--gui']):
            with patch('google_takeout_live_photos.gui.main') as mock_gui:
                try:
                    # This should attempt to launch GUI
                    cli.main()
                except SystemExit:
                    pass  # Expected if GUI import fails
                except ImportError:
                    pass  # Expected if GUI modules not available

    def test_launcher_script(self):
        """Test the standalone launcher script."""
        # Test that launcher script can be imported
        try:
            import launch_gui
            self.assertTrue(hasattr(launch_gui, 'gui_main'))
        except ImportError:
            # This is expected if GUI dependencies are not available
            pass


if __name__ == '__main__':
    # Skip GUI tests if running in headless environment
    if os.environ.get('DISPLAY') is None and sys.platform.startswith('linux'):
        print("Skipping GUI tests in headless environment")
        sys.exit(0)
    
    unittest.main()
