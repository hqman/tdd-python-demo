"""Tests for youtube_api.formatter module."""

import json
import pytest
from tdd_python_demo.youtube_api.formatter import format_json, format_human, format_table


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


class TestFormatHuman:
    """Tests for format_human function."""

    def test_format_human_basic_video_info(self):
        """Test format_human with basic video information."""
        video_info = {
            "title": "Test Video",
            "channel": "Test Channel",
            "views": 1000,
            "likes": 50
        }
        result = format_human(video_info)

        # Should be a string
        assert isinstance(result, str)
        # Should contain all the key information
        assert "Test Video" in result
        assert "Test Channel" in result
        assert "1000" in result or "1,000" in result
        assert "50" in result

    def test_format_human_with_missing_values(self):
        """Test format_human handles missing values gracefully."""
        video_info = {
            "title": "Test Video"
            # Other fields missing
        }
        result = format_human(video_info)

        assert isinstance(result, str)
        assert "Test Video" in result
        assert "N/A" in result  # Should show N/A for missing fields
