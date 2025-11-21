"""Unit tests for CLI channel command."""

import pytest
import json
from unittest.mock import patch, Mock
from tdd_python_demo.youtube_api.cli_channel import main


class TestCliChannelMain:
    """Test main CLI function."""

    @patch('tdd_python_demo.youtube_api.cli_channel.YouTubeClient')
    @patch('sys.argv', ['yt-channel', '--id', 'UC123', '--format', 'json'])
    def test_main_with_channel_id_json_output(self, mock_client_class):
        """Test main function with channel ID and JSON output."""
        # Mock client instance
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        # Mock get_channel_profile response
        mock_client.get_channel_profile.return_value = {
            "id": "UC123",
            "title": "Test Channel",
            "view_count": 1000
        }

        # Capture stdout
        with patch('sys.stdout') as mock_stdout:
            result = main()

        assert result == 0  # Success exit code
        mock_client.get_channel_profile.assert_called_once_with("UC123", include_recent_videos=False, max_videos=5)
