"""YouTube Data API v3 client implementation."""

import time
import requests


class YouTubeClient:
    def __init__(self, api_keys):
        if ',' in api_keys:
            self.keys = [k.strip() for k in api_keys.split(',')]
        else:
            self.keys = [api_keys]
        self.key = self.keys[0]
        self._current_key_index = 0

    def _to_int(self, value):
        """Convert string to int, return None if conversion fails."""
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    def request(self, url, params, max_retries=5):
        """Make GET request with timeout and retry logic."""
        params = params.copy()

        for attempt in range(max_retries):
            params['key'] = self.key
            try:
                response = requests.get(url, params=params, timeout=20)
                if response.status_code in (403, 429):
                    if self._rotate_key():
                        continue
                    else:
                        raise Exception(f"All API keys exhausted. Quota limit reached.")
                return response.json()
            except requests.exceptions.RequestException:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise

    def _rotate_key(self):
        """Rotate to next API key. Returns True if rotated, False if no more keys."""
        if len(self.keys) > 1 and self._current_key_index < len(self.keys) - 1:
            self._current_key_index += 1
            self.key = self.keys[self._current_key_index]
            return True
        return False

    def list_comments(self, video_id, page_size=100, max_comments=200, page_token=None):
        """Fetch comments for a video with pagination support."""
        url = "https://www.googleapis.com/youtube/v3/commentThreads"
        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": page_size,
            "textFormat": "plainText"
        }
        if page_token:
            params["pageToken"] = page_token
        response = self.request(url, params)
        comments = response.get("items", [])
        next_page_token = response.get("nextPageToken")
        return comments, next_page_token

    def get_all_comments(self, video_id, page_size=100):
        """Fetch all comments for a video using pagination."""
        all_comments = []
        page_token = None

        while True:
            comments, page_token = self.list_comments(video_id, page_size=page_size, page_token=page_token)
            all_comments.extend(comments)

            if not page_token:
                break

        return all_comments

    def get_video_statistics(self, video_id):
        """Get video statistics (view, like, comment counts)."""
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {"part": "statistics", "id": video_id}
        response = self.request(url, params)

        if not response.get("items"):
            raise RuntimeError("Video not found")

        stats = response["items"][0]["statistics"]
        return {
            "view_count": self._to_int(stats.get("viewCount")),
            "like_count": self._to_int(stats.get("likeCount")),
            "comment_count": self._to_int(stats.get("commentCount"))
        }

    def resolve_channel_id(self, input_str):
        """Resolve channel input to channel ID."""
        # If it's already a channel ID (starts with UC), return it
        if input_str.startswith("UC"):
            return input_str

        # If it's a handle (starts with @), resolve it via API
        if input_str.startswith("@"):
            handle = input_str[1:]
            response = self.request("https://www.googleapis.com/youtube/v3/channels",
                                   {"part": "id", "forHandle": handle})
            if response.get("items"):
                return response["items"][0]["id"]
            raise RuntimeError(f"Channel not found for handle: {input_str}")

        raise RuntimeError(f"Unable to resolve channel ID from: {input_str}")

    def _get_recent_videos(self, channel_id, max_videos=5):
        """Get recent videos for a channel."""
        search_response = self.request(
            "https://www.googleapis.com/youtube/v3/search",
            {
                "part": "id",
                "channelId": channel_id,
                "order": "date",
                "type": "video",
                "maxResults": max_videos
            }
        )

        video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]
        if not video_ids:
            return []

        videos_response = self.request(
            "https://www.googleapis.com/youtube/v3/videos",
            {
                "part": "snippet,statistics",
                "id": ",".join(video_ids)
            }
        )

        results = []
        for item in videos_response.get("items", []):
            snippet = item.get("snippet", {})
            statistics = item.get("statistics", {})
            results.append({
                "id": item.get("id"),
                "title": snippet.get("title"),
                "description": snippet.get("description"),
                "view_count": self._to_int(statistics.get("viewCount")),
                "like_count": self._to_int(statistics.get("likeCount"))
            })

        return results

    def get_channel_profile(self, channel_input, include_recent_videos=False, max_videos=5):
        """Get channel profile information."""
        channel_id = self.resolve_channel_id(channel_input)
        response = self.request("https://www.googleapis.com/youtube/v3/channels",
                               {"part": "snippet,statistics", "id": channel_id})

        if not response.get("items"):
            raise RuntimeError(f"Channel not found: {channel_input}")

        item = response["items"][0]
        snippet = item.get("snippet", {})
        statistics = item.get("statistics", {})

        result = {
            "id": channel_id,
            "title": snippet.get("title"),
            "description": snippet.get("description"),
            "custom_url": snippet.get("customUrl"),
            "thumbnails": snippet.get("thumbnails", {}),
            "view_count": self._to_int(statistics.get("viewCount")),
            "subscriber_count": self._to_int(statistics.get("subscriberCount")),
            "video_count": self._to_int(statistics.get("videoCount"))
        }

        if include_recent_videos:
            result["recent_videos"] = self._get_recent_videos(channel_id, max_videos=max_videos)

        return result
