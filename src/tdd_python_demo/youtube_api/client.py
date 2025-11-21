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
