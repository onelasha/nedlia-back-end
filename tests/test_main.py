"""
Test module for main.py
"""

import io
import runpy
from contextlib import redirect_stdout


def test_main_output():
    """Test that main.py prints 'Help' to stdout"""
    # Capture stdout
    f = io.StringIO()
    with redirect_stdout(f):
        # Execute main module
        runpy.run_module("main", run_name="__main__")

    # Get the output
    output = f.getvalue().strip()

    # Assert the output is correct
    assert output == "Help"
