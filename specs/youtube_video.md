# Project Specification: youtube-api - Video Features

## Goal
- Provide a lightweight YouTube Data API v3 client: supports key rotation, retry/backoff, and convenient retrieval of video information and comments.
- Provide a command-line tool `yt-fetch`, for convenient output and formatted viewing of video information.

## Underlying Tech Stack
- Official API: YouTube Data API v3 (REST HTTP).
- HTTP Client: `requests` directly requesting official REST endpoints, without relying on the Google Official Python SDK.
- Configuration & Authentication: `python-dotenv` loads `.env`, API Keys are passed via environment variables (not hardcoded in code).

## Dependencies & Environment
- Python >= 3.9
- Runtime: `requests`, `python-dotenv`
- Development/Test: `pytest`, `pytest-cov` (example uses `uv` to run)
- API Key: Environment variable `YOUTUBE_API_KEYS` (comma separated) or `YOUTUBE_API_KEY`. The project root `.env` and `youtube_api/.env` will be automatically loaded.

## Core Functionality (`youtube_api.client.YouTubeClient` - Video Related)

### Basic Request Methods
- `request(url, params, max_retries=5)`: GET request, default 20s timeout; exponential backoff; upon 403 Quota/429/Rate Limit, attempt to rotate Key; throws `RuntimeError` when retries are exhausted; network exceptions are also wrapped and thrown.
- Key Rotation: Sequential switching when multiple Keys are present; `key` property exposes the current Key.
- `_to_int`: Converts string numbers to int, returns None if conversion fails.

### Video Information Methods
- `get_video_statistics(video_id)`: Returns view/like/comment counts (int or None), throws error if video is missing.
- `get_video_details(video_id)`: Returns complete dictionary containing snippet/contentDetails/status/topicDetails/statistics, numbers converted to int.

### Comment Methods
- `list_comments(video_id, page_size=100, max_comments=200, page_token=None)`: Paginates top-level comments, returns (comments, next_page_token), stops when `max_comments` is reached.
- `get_all_comments(video_id, page_size=100)`: Fetches all comments.

## CLI Specification - yt-fetch (Video)

### Entry Point
- Entry (pyproject script): `yt-fetch` → `youtube_api.cli:main`
- Key Loading Priority: Command line `--keys` > `.env` (auto-loaded) > Environment variables.

### Command Line Arguments
- Input: `--url` or `--id` (one is required).
- Comments: `--max-comments` (default 200), `--page-size` (default 100), `--all-comments` (full fetch), `--stats-only` (statistics only).
- Output: `--format`=`json`|`human`|`table`|`summary` (default json); `--pretty` beautifies JSON.
- Behavior: Parses video ID, fetches full details; fetches comments based on options; outputs according to format; exits with non-zero code on error.

## Formatting (`youtube_api.formatter` - Video Related)
- Human-readable/Table/Summary output, simple ASCII tables; handles missing values (N/A), text truncation, date formatting.
- Supports formatted display of video information and comments.

## Errors & Quotas
- Network/Non-200 Response: Throws `RuntimeError` after retries.
- Quota/Rate Limit: Rotates Key if multiple Keys exist, otherwise continues backoff retries until exhausted.
- Video Missing: Throws `RuntimeError` with description.

## Testing
- Unit: `tests/test_client.py`, Mock requests/time, covers retry/rotation and video related methods.
- Integration (Real API, skips automatically if Key is missing): `tests/integration/test_integration_client.py`.
- End-to-End E2E (Real API, skips automatically if Key is missing): `tests/e2e/test_cli_e2e.py` covers CLI paths (stats-only JSON, table+comments).
- Common Commands:
  - Unit + Coverage only: `uv run -m pytest -m "not integration and not e2e" --cov=youtube_api --cov-report=term-missing`
  - Full (including real API, watch quota): `uv run -m pytest --cov=youtube_api --cov-report=term-missing --cov-report=html`
