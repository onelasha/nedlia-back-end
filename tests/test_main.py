"""
Tests for main.py
Tests for main.py
"""

from io import StringIO
from unittest import TestCase
from unittest import TestCase
from unittest.mock import patch

from app.main import main


class TestMain(TestCase):
    """Test cases for main.py"""
class TestMain(TestCase):
    """Test cases for main.py"""

    @patch("sys.stdout", new_callable=StringIO)
    def test_main_prints_startup_message(self, mock_stdout):
        """Test that main() prints the startup message"""
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Application started")

    def test_main_execution(self):
        """Test that main() executes without errors"""
        main()
