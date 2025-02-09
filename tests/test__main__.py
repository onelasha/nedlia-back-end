"""Tests for main.py"""

from unittest import TestCase

from app.__main__ import main


class TestMain(TestCase):
    """Test cases for main.py"""

    def test_main(self):
        """Test that main() runs without errors"""
        main()
