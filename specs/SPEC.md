# Project Spec: youtube-api

## Purpose
- Provide a lightweight YouTube Data API v3 client with key rotation, retries, and convenient helpers for video/channel data and comments.
- Ship CLIs (`yt-fetch`, `yt-channel`) for quick retrieval and formatted output.

## Stack & API
- Official API: YouTube Data API v3 (REST HTTP).
- HTTP layer: `requests` against the REST endpoints (no Google SDK dependency).
- Config/keys: `python-dotenv` loads `.env`; API keys supplied via env, not embedded in code.

## Requirements
- Python >= 3.9.
- Runtime deps: `requests`, `python-dotenv`.
- Dev/test: `pytest`, `pytest-cov`; `uv` used in examples/automation.
- API keys via `YOUTUBE_API_KEYS` (comma-separated) or `YOUTUBE_API_KEY`. `.env` in repo root and `youtube_api/.env` are auto-loaded.

## Core Behaviors (youtube_api.client.YouTubeClient)
- `request(url, params, max_retries=5)`: GET with timeout (default 20s), exponential backoff, key rotation on quota errors (403 with “quota/ exceeded” or rate limits), raises `RuntimeError` after exhaust; wraps network errors.
- Key rotation: round-robin across provided keys when quota hit; `key` property exposes current key.
- `get_video_statistics(video_id)`: returns `viewCount/likeCount/commentCount` (ints or None); raises if video missing.
- `get_video_details(video_id)`: returns rich dict (ids, snippet fields, content details, status, topicCategories, statistics with ints).
- `list_comments(video_id, page_size=100, max_comments=200, page_token=None)`: fetch paged top-level comments, returns `(comments, next_page_token)`; stops early if `max_comments` reached.
- `get_all_comments(video_id, page_size=100)`: fetches all pages.
- `resolve_channel_id(input_str)`: accepts channel ID, channel URL, handle (with/without @, or handle URL), resolves via search if needed; raises if not found.
- `get_channel_profile(channel_input, include_recent_videos=False, max_videos=5)`: returns channel metadata, thumbnails, stats (ints), keywords/banner/topics/privacy, optional `recentVideos`.
- `_get_recent_videos(channel_id, max_videos=5)`: pulls latest videos (search + videos endpoint) with basic stats and descriptions.
- Helpers convert numeric strings to int (`_to_int`).

## CLI Spec
- Entrypoints (pyproject tool scripts):
  - `yt-fetch` → `youtube_api.cli:main` (video stats/comments).
  - `yt-channel` → `youtube_api.cli_channel:main` (channel profile).
- Key loading priority: `--keys` > `.env` > env vars; both CLIs rely on `load_api_keys`.

### yt-fetch
- Inputs: `--url` or `--id` (required one).
- Comment controls: `--max-comments` (default 200), `--page-size` (default 100, max 100), `--all-comments` (override to fetch all), `--stats-only` (skip comments).
- Output: `--format` in `{json (default), human, table, summary}`; `--pretty` pretty-prints JSON.
- Behavior: extracts video ID, fetches full details, optionally comments (all or capped), emits chosen format; exits non-zero on invalid input or API failures.

### yt-channel
- Inputs: one of `--id`, `--handle`, `--url` (required one).
- Options: `--include-videos` (fetch recent), `--max-videos` (default 5), `--keys` as above.
- Output: `--format` in `{json (default), human}`; `--pretty` for JSON.
- Behavior: resolves channel, fetches profile, optional recent videos, prints format; exits non-zero on failure.

## Formatting (youtube_api.formatter)
- Human/table/summary renderers for stats and comments; simple ASCII table builder; handles missing values (`N/A`), truncation, date formatting.

## Error Handling & Limits
- Network errors and non-200 responses bubble as `RuntimeError` after retries.
- Quota/rate errors rotate keys when multiple are provided; otherwise retry/backoff until max attempts.
- Missing resources (video/channel) raise `RuntimeError` with descriptive message.

## Testing
- Unit tests: `tests/test_client.py` (mocked requests/time) cover retry/rotation and helper methods.
- Integration (real API; env key required, auto-skip otherwise): `tests/integration/test_integration_client.py`.
- E2E (real API; auto-skip without key): `tests/e2e/test_cli_e2e.py` exercises CLI paths (stats-only JSON, table with comments, channel profile JSON with recent videos).
- Common commands:
  - Unit only w/ coverage: `uv run -m pytest -m "not integration and not e2e" --cov=youtube_api --cov-report=term-missing`
  - Full suite incl. real API (ensure keys set): `uv run -m pytest --cov=youtube_api --cov-report=term-missing --cov-report=html`
