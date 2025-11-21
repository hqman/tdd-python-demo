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
                if response.status_code == 403 and self._rotate_key():
                    continue
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
