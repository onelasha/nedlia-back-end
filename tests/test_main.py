"""
This module provides a simple greeting function.
"""

# import pytest

from main import add


def test_add():
    """
    Test the add function with sample inputs.
    """
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
