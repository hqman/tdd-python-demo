"""End-to-end tests for yt-channel CLI.

These tests require a valid YouTube API key in environment variables:
- YOUTUBE_API_KEY or YOUTUBE_API_KEYS
Tests will be skipped if no API key is found.
"""

import pytest
import os
import subprocess
import json


@pytest.mark.e2e
class TestCliChannelE2E:
    """E2E tests for yt-channel command."""

    @pytest.fixture
    def api_key(self):
        """Get API key from environment."""
        key = os.getenv('YOUTUBE_API_KEY') or os.getenv('YOUTUBE_API_KEYS')
        if not key:
            pytest.skip("No YouTube API key found in environment")
        return key

    def test_yt_channel_with_handle_json(self, api_key):
        """Test yt-channel with a real YouTube handle."""
        # Using a well-known public channel
        result = subprocess.run(
            ['yt-channel', '--handle', '@YouTube', '--format', 'json'],
            capture_output=True,
            text=True,
            env={**os.environ, 'YOUTUBE_API_KEY': api_key}
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"
        assert result.stdout.strip(), "No output received"

        # Should be valid JSON
        data = json.loads(result.stdout)
        assert 'id' in data
        assert 'title' in data
        assert data['title']  # Should have a title
