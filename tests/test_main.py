"""
Tests for __main__.py
"""

import unittest
from io import StringIO
from unittest.mock import patch

from app.__main__ import main as main_import
from app.main import main


class TestMain(unittest.TestCase):
    """Test the main function"""

    @patch("sys.stdout", new_callable=StringIO)
    def test_main_function(self, mock_stdout):
        """Test that main function prints the expected output"""
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Application started")

    def test_main_import(self):
        """Test that main function is properly imported"""
        self.assertEqual(main_import, main)


if __name__ == "__main__":
    unittest.main()
