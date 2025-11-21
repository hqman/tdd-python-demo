"""Tests for youtube_api.formatter module."""

import json
import pytest
from tdd_python_demo.youtube_api.formatter import format_json


class TestFormatJson:
    """Tests for format_json function."""

    def test_format_json_simple_data(self):
        """Test format_json with simple data returns valid JSON string."""
        data = {"title": "Test Video", "views": 1000}
        result = format_json(data)

        # Should return a valid JSON string
        assert isinstance(result, str)
        # Should be parseable back to dict
        parsed = json.loads(result)
        assert parsed == data

    def test_format_json_with_pretty_flag(self):
        """Test format_json with pretty=True returns indented JSON."""
        data = {"title": "Test Video", "views": 1000}
        result = format_json(data, pretty=True)

        # Should contain indentation (newlines and spaces)
        assert "\n" in result
        assert "  " in result
        # Should still be valid JSON
        parsed = json.loads(result)
        assert parsed == data
