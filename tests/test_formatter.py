"""Tests for youtube_api.formatter module."""

import json
import pytest
from tdd_python_demo.youtube_api.formatter import (
    format_json,
    format_human,
    format_table,
    format_summary,
    format_channel_profile
)


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

    def test_format_json_with_chinese_characters(self):
        """Test format_json properly handles Chinese characters without escaping."""
        data = {"title": "摩的司机徐师傅", "description": "若无闲事挂心头"}
        result = format_json(data)

        # Should contain actual Chinese characters, not Unicode escapes
        assert "摩的司机徐师傅" in result
        assert "若无闲事挂心头" in result
        # Should not contain Unicode escape sequences
        assert "\\u" not in result
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


class TestFormatTable:
    """Tests for format_table function."""

    def test_format_table_basic_video_info(self):
        """Test format_table creates ASCII table with video info."""
        video_info = {
            "title": "Test Video",
            "channel": "Test Channel",
            "views": 1000
        }
        result = format_table(video_info)

        assert isinstance(result, str)
        # Should contain the data
        assert "Test Video" in result
        assert "Test Channel" in result
        # Should have table borders
        assert "|" in result or "+" in result or "-" in result


class TestFormatSummary:
    """Tests for format_summary function."""

    def test_format_summary_basic(self):
        """Test format_summary creates compact summary."""
        video_info = {
            "title": "Test Video",
            "views": 1000
        }
        result = format_summary(video_info)

        assert isinstance(result, str)
        assert "Test Video" in result
        assert "1000" in result or "1,000" in result
        # Should be compact (single line)
        assert "\n" not in result or result.count("\n") <= 1


class TestFormatChannelProfile:
    """Tests for format_channel_profile function."""

    def test_format_channel_profile_basic(self):
        """Test format_channel_profile with basic channel information."""
        channel_data = {
            "id": "UC123",
            "title": "Test Channel",
            "description": "A test channel description",
            "custom_url": "@testchannel",
            "view_count": 100000,
            "subscriber_count": 5000,
            "video_count": 50
        }
        result = format_channel_profile(channel_data)

        assert isinstance(result, str)
        assert "Test Channel" in result
        assert "UC123" in result
        assert "@testchannel" in result
        assert "100" in result or "100,000" in result  # View count formatted
        assert "5000" in result or "5,000" in result   # Subscriber count
        assert "50" in result                           # Video count

    def test_format_channel_profile_with_missing_values(self):
        """Test format_channel_profile handles missing values gracefully."""
        channel_data = {
            "id": "UC456",
            "title": "Minimal Channel",
            "view_count": None,
            "subscriber_count": None
        }
        result = format_channel_profile(channel_data)

        assert isinstance(result, str)
        assert "Minimal Channel" in result
        assert "N/A" in result  # Should show N/A for missing fields

    def test_format_channel_profile_with_recent_videos(self):
        """Test format_channel_profile includes recent videos when provided."""
        channel_data = {
            "id": "UC789",
            "title": "Video Channel",
            "view_count": 50000,
            "recent_videos": [
                {"id": "vid1", "title": "Recent Video 1", "view_count": 1000},
                {"id": "vid2", "title": "Recent Video 2", "view_count": 500}
            ]
        }
        result = format_channel_profile(channel_data)

        assert isinstance(result, str)
        assert "Video Channel" in result
        assert "Recent Video 1" in result
        assert "Recent Video 2" in result
        assert "1000" in result or "1,000" in result
