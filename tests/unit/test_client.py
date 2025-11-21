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

    @patch('tdd_python_demo.youtube_api.client.time.sleep')
    @patch('tdd_python_demo.youtube_api.client.requests.get')
    def test_request_raises_error_when_all_keys_exhausted(self, mock_get, mock_sleep):
        """Test request raises error when all API keys return 403/429."""
        mock_response_403 = Mock()
        mock_response_403.status_code = 403
        mock_response_403.json.return_value = {"error": {"code": 403, "message": "quotaExceeded"}}

        # All three keys will return 403
        mock_get.side_effect = [mock_response_403, mock_response_403, mock_response_403]

        client = YouTubeClient(api_keys="key1,key2,key3")

        with pytest.raises(Exception) as exc_info:
            client.request("https://api.example.com/test", {})

        assert "quota" in str(exc_info.value).lower() or "exhausted" in str(exc_info.value).lower()
        assert mock_get.call_count == 3

    @patch('tdd_python_demo.youtube_api.client.time.sleep')
    @patch('tdd_python_demo.youtube_api.client.requests.get')
    def test_request_raises_error_on_single_key_quota_exceeded(self, mock_get, mock_sleep):
        """Test request raises error immediately when single API key hits quota."""
        mock_response_403 = Mock()
        mock_response_403.status_code = 403
        mock_response_403.json.return_value = {"error": {"code": 403, "message": "quotaExceeded"}}

        mock_get.return_value = mock_response_403

        client = YouTubeClient(api_keys="single_key")

        with pytest.raises(Exception) as exc_info:
            client.request("https://api.example.com/test", {})

        assert "quota" in str(exc_info.value).lower() or "exhausted" in str(exc_info.value).lower()
        assert mock_get.call_count == 1  # Should only try once with single key


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

    @patch.object(YouTubeClient, 'request')
    def test_get_video_statistics_with_missing_fields(self, mock_request):
        """Test get_video_statistics handles missing statistics fields gracefully."""
        mock_request.return_value = {
            "items": [{
                "statistics": {
                    "viewCount": "1000"
                    # likeCount and commentCount missing
                }
            }]
        }

        client = YouTubeClient(api_keys="test_key")
        result = client.get_video_statistics("test_video_id")

        assert result == {
            "view_count": 1000,
            "like_count": None,
            "comment_count": None
        }

    @patch.object(YouTubeClient, 'request')
    def test_get_video_statistics_raises_error_for_missing_video(self, mock_request):
        """Test get_video_statistics raises error when video not found."""
        mock_request.return_value = {
            "items": []  # Video not found
        }

        client = YouTubeClient(api_keys="test_key")

        with pytest.raises(RuntimeError, match="Video not found"):
            client.get_video_statistics("invalid_video_id")


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

    @patch.object(YouTubeClient, 'request')
    def test_list_comments_with_page_token(self, mock_request):
        """Test list_comments includes page_token when provided."""
        mock_request.return_value = {
            "items": [{"id": "comment3"}],
            "nextPageToken": "next_token_456"
        }

        client = YouTubeClient(api_keys="test_key")
        comments, next_token = client.list_comments("video123", page_token="token_abc")

        assert len(comments) == 1
        mock_request.assert_called_once_with(
            "https://www.googleapis.com/youtube/v3/commentThreads",
            {
                "part": "snippet",
                "videoId": "video123",
                "maxResults": 100,
                "textFormat": "plainText",
                "pageToken": "token_abc"
            }
        )


class TestGetAllComments:
    """Test get_all_comments() method."""

    @patch.object(YouTubeClient, 'list_comments')
    def test_get_all_comments_single_page(self, mock_list_comments):
        """Test get_all_comments with no pagination needed."""
        mock_list_comments.return_value = (
            [{"id": "comment1"}, {"id": "comment2"}],
            None
        )

        client = YouTubeClient(api_keys="test_key")
        all_comments = client.get_all_comments("video123")

        assert len(all_comments) == 2
        assert all_comments[0]["id"] == "comment1"
        mock_list_comments.assert_called_once_with("video123", page_size=100, page_token=None)

    @patch.object(YouTubeClient, 'list_comments')
    def test_get_all_comments_with_pagination(self, mock_list_comments):
        """Test get_all_comments fetches all pages when pagination exists."""
        mock_list_comments.side_effect = [
            ([{"id": "comment1"}, {"id": "comment2"}], "token_page2"),
            ([{"id": "comment3"}, {"id": "comment4"}], "token_page3"),
            ([{"id": "comment5"}], None)
        ]

        client = YouTubeClient(api_keys="test_key")
        all_comments = client.get_all_comments("video123")

        assert len(all_comments) == 5
        assert all_comments[0]["id"] == "comment1"
        assert all_comments[4]["id"] == "comment5"
        assert mock_list_comments.call_count == 3

    @patch.object(YouTubeClient, 'list_comments')
    def test_get_all_comments_with_empty_result(self, mock_list_comments):
        """Test get_all_comments handles videos with no comments."""
        mock_list_comments.return_value = ([], None)

        client = YouTubeClient(api_keys="test_key")
        all_comments = client.get_all_comments("video123")

        assert len(all_comments) == 0
        assert all_comments == []
        mock_list_comments.assert_called_once_with("video123", page_size=100, page_token=None)



class TestResolveChannelId:
    """Test resolve_channel_id() method."""

    @patch.object(YouTubeClient, "request")
    def test_resolve_channel_id_with_channel_id(self, mock_request):
        """Test resolve_channel_id returns channel ID when given channel ID."""
        client = YouTubeClient(api_keys="test_key")
        result = client.resolve_channel_id("UCxxxxxxxxxxxxxx")

        assert result == "UCxxxxxxxxxxxxxx"
        mock_request.assert_not_called()

    @patch.object(YouTubeClient, "request")
    def test_resolve_channel_id_with_handle(self, mock_request):
        """Test resolve_channel_id resolves @handle to channel ID."""
        mock_request.return_value = {
            "items": [{"id": "UCyyyy"}]
        }

        client = YouTubeClient(api_keys="test_key")
        result = client.resolve_channel_id("@username")

        assert result == "UCyyyy"
        mock_request.assert_called_once()


class TestGetChannelProfile:
    """Test get_channel_profile() method."""

    @patch.object(YouTubeClient, "request")
    @patch.object(YouTubeClient, "resolve_channel_id")
    def test_get_channel_profile_basic(self, mock_resolve, mock_request):
        """Test get_channel_profile returns basic channel information."""
        mock_resolve.return_value = "UC123"
        mock_request.return_value = {
            "items": [{
                "snippet": {
                    "title": "Test Channel",
                    "description": "A test channel description",
                    "customUrl": "@testchannel",
                    "thumbnails": {
                        "default": {"url": "https://example.com/thumb.jpg"}
                    }
                },
                "statistics": {
                    "viewCount": "10000",
                    "subscriberCount": "500",
                    "videoCount": "50"
                }
            }]
        }

        client = YouTubeClient(api_keys="test_key")
        result = client.get_channel_profile("@testchannel")

        assert result["id"] == "UC123"
        assert result["title"] == "Test Channel"
        assert result["description"] == "A test channel description"
        assert result["custom_url"] == "@testchannel"
        assert result["thumbnails"]["default"]["url"] == "https://example.com/thumb.jpg"
        assert result["view_count"] == 10000
        assert result["subscriber_count"] == 500
        assert result["video_count"] == 50

        mock_resolve.assert_called_once_with("@testchannel")
        mock_request.assert_called_once()

    @patch.object(YouTubeClient, "request")
    @patch.object(YouTubeClient, "resolve_channel_id")
    def test_get_channel_profile_not_found(self, mock_resolve, mock_request):
        """Test get_channel_profile raises error when channel not found."""
        mock_resolve.return_value = "UC999"
        mock_request.return_value = {"items": []}

        client = YouTubeClient(api_keys="test_key")

        with pytest.raises(RuntimeError, match="Channel not found"):
            client.get_channel_profile("@nonexistent")

    @patch.object(YouTubeClient, "request")
    @patch.object(YouTubeClient, "resolve_channel_id")
    def test_get_channel_profile_with_missing_fields(self, mock_resolve, mock_request):
        """Test get_channel_profile handles missing optional fields gracefully."""
        mock_resolve.return_value = "UC456"
        mock_request.return_value = {
            "items": [{
                "snippet": {
                    "title": "Minimal Channel"
                    # Missing: description, customUrl, thumbnails
                },
                "statistics": {
                    "viewCount": "1000"
                    # Missing: subscriberCount, videoCount
                }
            }]
        }

        client = YouTubeClient(api_keys="test_key")
        result = client.get_channel_profile("UC456")

        assert result["id"] == "UC456"
        assert result["title"] == "Minimal Channel"
        assert result["description"] is None
        assert result["custom_url"] is None
        assert result["thumbnails"] == {}
        assert result["view_count"] == 1000
        assert result["subscriber_count"] is None
        assert result["video_count"] is None

    @patch.object(YouTubeClient, "_get_recent_videos")
    @patch.object(YouTubeClient, "request")
    @patch.object(YouTubeClient, "resolve_channel_id")
    def test_get_channel_profile_with_recent_videos(self, mock_resolve, mock_request, mock_get_videos):
        """Test get_channel_profile includes recent videos when requested."""
        mock_resolve.return_value = "UC789"
        mock_request.return_value = {
            "items": [{
                "snippet": {
                    "title": "Test Channel",
                    "description": "Test description"
                },
                "statistics": {
                    "viewCount": "5000",
                    "subscriberCount": "100",
                    "videoCount": "20"
                }
            }]
        }
        mock_get_videos.return_value = [
            {"id": "video1", "title": "Recent Video 1", "view_count": 1000},
            {"id": "video2", "title": "Recent Video 2", "view_count": 500}
        ]

        client = YouTubeClient(api_keys="test_key")
        result = client.get_channel_profile("@testchannel", include_recent_videos=True, max_videos=2)

        assert result["id"] == "UC789"
        assert "recent_videos" in result
        assert len(result["recent_videos"]) == 2
        assert result["recent_videos"][0]["id"] == "video1"
        assert result["recent_videos"][1]["id"] == "video2"

        mock_get_videos.assert_called_once_with("UC789", max_videos=2)


class TestGetRecentVideos:
    """Test _get_recent_videos() helper method."""

    @patch.object(YouTubeClient, "request")
    def test_get_recent_videos_basic(self, mock_request):
        """Test _get_recent_videos returns recent videos with statistics."""
        # Mock search API response
        search_response = {
            "items": [
                {"id": {"videoId": "vid1"}},
                {"id": {"videoId": "vid2"}}
            ]
        }
        # Mock videos API response
        videos_response = {
            "items": [
                {
                    "id": "vid1",
                    "snippet": {"title": "Video 1", "description": "Description 1"},
                    "statistics": {"viewCount": "1000", "likeCount": "50"}
                },
                {
                    "id": "vid2",
                    "snippet": {"title": "Video 2", "description": "Description 2"},
                    "statistics": {"viewCount": "500", "likeCount": "25"}
                }
            ]
        }
        mock_request.side_effect = [search_response, videos_response]

        client = YouTubeClient(api_keys="test_key")
        result = client._get_recent_videos("UC123", max_videos=2)

        assert len(result) == 2
        assert result[0]["id"] == "vid1"
        assert result[0]["title"] == "Video 1"
        assert result[0]["view_count"] == 1000
        assert result[0]["like_count"] == 50
        assert result[1]["id"] == "vid2"

        # Verify API calls
        assert mock_request.call_count == 2

    @patch.object(YouTubeClient, "request")
    def test_get_recent_videos_empty_channel(self, mock_request):
        """Test _get_recent_videos returns empty list when channel has no videos."""
        mock_request.return_value = {"items": []}

        client = YouTubeClient(api_keys="test_key")
        result = client._get_recent_videos("UC_EMPTY", max_videos=5)

        assert result == []
        # Should only call search API once, not videos API
        assert mock_request.call_count == 1

