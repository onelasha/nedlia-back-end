"""Unit tests for version number validation functionality."""
import re
import unittest
from main import regex


class TestVersionValidation(unittest.TestCase):
    """Test suite for version number validation.

    Tests version strings against minimum version requirements.
    """
    def test_valid_versions(self):
        """Test that valid version numbers are correctly identified."""
        valid_versions = [
            "1.14.56",    # Minimum valid version
            "1.14.57",
            "1.14.99",
            "1.15.0",     # Valid major.minor change
            "1.16.0",
            "2.0.0",      # Valid major version change
            "2.1.0",
            "10.0.0",     # Double digit major
            "1.15.123",   # Triple digit patch
            "1.123.0"     # Triple digit minor
        ]
        
        for version in valid_versions:
            with self.subTest(version=version):
                self.assertTrue(
                    bool(re.match(regex, version)),
                    f"Version {version} should be valid"
                )

    def test_invalid_versions(self):
        """Test that invalid version numbers are correctly rejected."""
        invalid_versions = [
            "1.14.55",    # Too old
            "1.14.0",
            "1.13.99",
            "1.0.0",
            "0.1.0",
            "1.14.55a",   # Invalid format
            "v1.14.56",
            "1.14",
            ".14.56",
            "a.b.c",
            "",          # Empty string
            "1.14.56.0", # Too many segments
            " 1.14.56",  # Leading/trailing spaces
            "1.14.56 "
        ]
        
        for version in invalid_versions:
            with self.subTest(version=version):
                self.assertFalse(
                    bool(re.match(regex, version)),
                    f"Version {version} should be invalid"
                )

if __name__ == '__main__':
    unittest.main() 