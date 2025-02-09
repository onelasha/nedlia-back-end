"""Tests for main.py"""

from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from app.__main__ import main as mainFunction


class TestMain(TestCase):
    """Test cases for main.py"""

    @patch("sys.stdout", new_callable=StringIO)
    def test_main_prints_startup_message(self, mock_stdout):
        """Test that main() prints the startup message"""
        mainFunction()
        self.assertEqual(mock_stdout.getvalue().strip(), "Application started")

    @patch("sys.stdout", new_callable=StringIO)
    def test_main_execution(self, mock_stdout):
        """Test that main() executes without errors"""
        mainFunction()
        self.assertEqual(mock_stdout.getvalue().strip(), "Application started")
