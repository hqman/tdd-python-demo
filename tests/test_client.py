"""Unit tests for YouTubeClient."""

import pytest
import requests
from unittest.mock import Mock, patch
from tdd_python_demo.youtube_api.client import YouTubeClient


class TestYouTubeClientInitialization:
    """Test YouTubeClient initialization and API Key management."""

    def test_init_with_single_key(self):
        """Test initialization with a single API key."""
        client = YouTubeClient(api_keys="test_key_123")
        assert client.key == "test_key_123"
        assert client.keys == ["test_key_123"]

    def test_init_with_multiple_keys(self):
        """Test initialization with multiple API keys (comma-separated string)."""
        client = YouTubeClient(api_keys="key1,key2,key3")
        assert client.key == "key1"
        assert client.keys == ["key1", "key2", "key3"]

    def test_init_with_keys_containing_whitespace(self):
        """Test initialization handles keys with whitespace correctly."""
        client = YouTubeClient(api_keys=" key1 , key2 , key3 ")
        assert client.key == "key1"
        assert client.keys == ["key1", "key2", "key3"]


class TestUtilityMethods:
    """Test utility methods."""

    def test_to_int_with_valid_string(self):
        """Test _to_int converts valid numeric string to int."""
        client = YouTubeClient(api_keys="test_key")
        assert client._to_int("12345") == 12345

    def test_to_int_with_invalid_string(self):
        """Test _to_int returns None for invalid input."""
        client = YouTubeClient(api_keys="test_key")
        assert client._to_int("not_a_number") is None


class TestRequestMethod:
    """Test request() method with retry and backoff."""

    @patch('tdd_python_demo.youtube_api.client.requests.get')
    def test_request_success(self, mock_get):
        """Test successful API request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        client = YouTubeClient(api_keys="test_key")
        result = client.request("https://api.example.com/test", {"param": "value"})

        assert result == {"items": []}
        mock_get.assert_called_once_with(
            "https://api.example.com/test",
            params={"param": "value", "key": "test_key"},
            timeout=20
        )

    @patch('tdd_python_demo.youtube_api.client.time.sleep')
    @patch('tdd_python_demo.youtube_api.client.requests.get')
    def test_request_retry_on_network_error(self, mock_get, mock_sleep):
        """Test request retries on network errors with exponential backoff."""
        mock_get.side_effect = [
            requests.exceptions.RequestException("Network error"),
            requests.exceptions.RequestException("Network error"),
            Mock(status_code=200, json=lambda: {"success": True})
        ]

        client = YouTubeClient(api_keys="test_key")
        result = client.request("https://api.example.com/test", {})

        assert result == {"success": True}
        assert mock_get.call_count == 3
        assert mock_sleep.call_count == 2

    @patch('tdd_python_demo.youtube_api.client.time.sleep')
    @patch('tdd_python_demo.youtube_api.client.requests.get')
    def test_request_rotates_key_on_quota_error(self, mock_get, mock_sleep):
        """Test request rotates to next API key on 403 quota error."""
        mock_response_403 = Mock()
        mock_response_403.status_code = 403
        mock_response_403.json.return_value = {"error": {"code": 403}}

        mock_response_success = Mock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = {"success": True}

        mock_get.side_effect = [mock_response_403, mock_response_success]

        client = YouTubeClient(api_keys="key1,key2,key3")
        result = client.request("https://api.example.com/test", {})

        assert result == {"success": True}
        assert client.key == "key2"
        assert mock_get.call_count == 2

    @patch('tdd_python_demo.youtube_api.client.time.sleep')
    @patch('tdd_python_demo.youtube_api.client.requests.get')
    def test_request_rotates_key_on_429_rate_limit(self, mock_get, mock_sleep):
        """Test request rotates to next API key on 429 rate limit error."""
        mock_response_429 = Mock()
        mock_response_429.status_code = 429
        mock_response_429.json.return_value = {"error": {"code": 429}}

        mock_response_success = Mock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = {"success": True}

        mock_get.side_effect = [mock_response_429, mock_response_success]

        client = YouTubeClient(api_keys="key1,key2,key3")
        result = client.request("https://api.example.com/test", {})

        assert result == {"success": True}
        assert client.key == "key2"
        assert mock_get.call_count == 2


@pytest.mark.skip(reason="Not part of current task - will implement later")
class TestGetVideoStatistics:
    """Test get_video_statistics() method."""

    @patch.object(YouTubeClient, 'request')
    def test_get_video_statistics_returns_basic_stats(self, mock_request):
        """Test get_video_statistics returns view, like, and comment counts."""
        mock_request.return_value = {
            "items": [{
                "statistics": {
                    "viewCount": "1000",
                    "likeCount": "50",
                    "commentCount": "10"
                }
            }]
        }

        client = YouTubeClient(api_keys="test_key")
        result = client.get_video_statistics("test_video_id")

        assert result == {
            "view_count": 1000,
            "like_count": 50,
            "comment_count": 10
        }
        mock_request.assert_called_once_with(
            "https://www.googleapis.com/youtube/v3/videos",
            {"part": "statistics", "id": "test_video_id"}
        )


@pytest.mark.skip(reason="Not part of current task - will implement later")
class TestListComments:
    """Test list_comments() method."""

    @patch.object(YouTubeClient, 'request')
    def test_list_comments_basic(self, mock_request):
        """Test list_comments returns comments list and next_page_token."""
        mock_request.return_value = {
            "items": [
                {"id": "comment1", "snippet": {"topLevelComment": {"snippet": {"textDisplay": "Great video!"}}}},
                {"id": "comment2", "snippet": {"topLevelComment": {"snippet": {"textDisplay": "Thanks!"}}}}
            ],
            "nextPageToken": "next_token_123"
        }

        client = YouTubeClient(api_keys="test_key")
        comments, next_token = client.list_comments("video123")

        assert len(comments) == 2
        assert comments[0]["id"] == "comment1"
        assert next_token == "next_token_123"
        mock_request.assert_called_once_with(
            "https://www.googleapis.com/youtube/v3/commentThreads",
            {
                "part": "snippet",
                "videoId": "video123",
                "maxResults": 100,
                "textFormat": "plainText"
            }
        )
