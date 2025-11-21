# Project Specification: youtube-api - Channel Features

## Goal
- Provide a lightweight YouTube Data API v3 client: supports key rotation, retry/backoff, and convenient retrieval of channel information.
- Provide a command-line tool `yt-channel` for convenient output and formatted viewing of channel information.

## Underlying Tech Stack
- Official API: YouTube Data API v3 (REST HTTP).
- HTTP Client: `requests` directly requesting official REST endpoints, without relying on the Google Official Python SDK.
- Configuration & Authentication: `python-dotenv` loads `.env`, API Keys are passed via environment variables (not hardcoded in code).

## Dependencies & Environment
- Python >= 3.9
- Runtime: `requests`, `python-dotenv`
- Development/Test: `pytest`, `pytest-cov` (example uses `uv` to run)
- API Key: Environment variable `YOUTUBE_API_KEYS` (comma separated) or `YOUTUBE_API_KEY`. The project root `.env` and `youtube_api/.env` will be automatically loaded.

## Core Functionality (`youtube_api.client.YouTubeClient` - Channel Related)

### Basic Request Methods
- `request(url, params, max_retries=5)`: GET request, default 20s timeout; exponential backoff; upon 403 Quota/429/Rate Limit, attempt to rotate Key; throws `RuntimeError` when retries are exhausted; network exceptions are also wrapped and thrown.
- Key Rotation: Sequential switching when multiple Keys are present; `key` property exposes the current Key.
- `_to_int`: Converts string numbers to int, returns None if conversion fails.

### Channel Resolution Methods
- `resolve_channel_id(input_str)`: Supports Channel ID, Channel URL, handle (including @ or URL), throws error if not found.

### Channel Information Methods
- `get_channel_profile(channel_input, include_recent_videos=False, max_videos=5)`: Returns channel metadata, thumbnails, statistics (int), keywords/banner/topic/privacy, optionally includes recent videos.
- `_get_recent_videos(channel_id, max_videos=5)`: Search + videos to fetch the latest videos and basic statistics.

## CLI Specification - yt-channel (Channel)

### Entry Point
- Entry (pyproject script): `yt-channel` → `youtube_api.cli_channel:main`
- Key Loading Priority: Command line `--keys` > `.env` (auto-loaded) > Environment variables.

### Command Line Arguments
- Input: `--id`|`--handle`|`--url` (one is required).
- Options: `--include-videos` (include recent videos), `--max-videos` (default 5), `--keys`.
- Output: `--format`=`json`|`human` (default json), `--pretty` only affects json.
- Behavior: Resolves channel, fetches profile, optionally recent videos; outputs according to format; exits with non-zero code on error.

## Formatting (`youtube_api.formatter` - Channel Related)
- Human-readable output, handling missing values (N/A), text truncation, date formatting.
- Supports formatted display of channel information and recent videos.

## Errors & Quotas
- Network/Non-200 Response: Throws `RuntimeError` after retries.
- Quota/Rate Limit: Rotates Key if multiple Keys exist, otherwise continues backoff retries until exhausted.
- Channel Missing: Throws `RuntimeError` with description.

## Testing
- Unit: `tests/test_client.py`, Mock requests/time, covers retry/rotation and channel related methods.
- Integration (Real API, skips automatically if Key is missing): `tests/integration/test_integration_client.py`.
- End-to-End E2E (Real API, skips automatically if Key is missing): `tests/e2e/test_cli_e2e.py` covers CLI paths (Channel JSON+Recent Videos).
- Common Commands:
  - Unit + Coverage only: `uv run -m pytest -m "not integration and not e2e" --cov=youtube_api --cov-report=term-missing`
  - Full (including real API, watch quota): `uv run -m pytest --cov=youtube_api --cov-report=term-missing --cov-report=html`
