"""Tests for the CLI TOC generator."""

import json
import tempfile
from pathlib import Path

from tdd_python_demo.cli_toc import main


def test_cli_reads_markdown_file_and_outputs_json():
    """Test that CLI reads a markdown file and outputs JSON TOC."""
    # Create a temporary markdown file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write("# Title\n## Section\n")
        temp_file = f.name

    try:
        # Run CLI with the temp file
        import io
        import sys

        captured_output = io.StringIO()
        sys.stdout = captured_output

        result = main([temp_file])

        sys.stdout = sys.__stdout__

        # Check exit code
        assert result == 0

        # Parse output as JSON
        output = captured_output.getvalue()
        toc = json.loads(output)

        # Verify TOC content
        assert len(toc) == 2
        assert toc[0] == {'level': 1, 'text': 'Title', 'slug': 'title'}
        assert toc[1] == {'level': 2, 'text': 'Section', 'slug': 'section'}
    finally:
        # Clean up
        Path(temp_file).unlink()


def test_cli_can_be_called_without_arguments():
    """Test that main() can be called without argv (defaults to sys.argv)."""
    import sys
    import io
    import tempfile

    # Create a temporary markdown file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write("# Test\n")
        temp_file = f.name

    try:
        # Mock sys.argv
        original_argv = sys.argv
        sys.argv = ['tdd-toc', temp_file]

        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call main without arguments
        result = main()

        sys.stdout = sys.__stdout__
        sys.argv = original_argv

        assert result == 0
        output = captured_output.getvalue()
        toc = json.loads(output)
        assert len(toc) == 1
    finally:
        Path(temp_file).unlink()
        sys.argv = original_argv
