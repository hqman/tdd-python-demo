# YouTube Channel CLI Tool - Usage Guide

## Overview

`yt-channel` is a command-line tool for fetching YouTube channel information using the YouTube Data API v3.

## Installation

```bash
# Install the project
uv pip install -e .

# Or using pip
pip install -e .
```

## Configuration

Set your YouTube API key in environment variables:

```bash
# Option 1: Single API key
export YOUTUBE_API_KEY="your_api_key_here"

# Option 2: Multiple API keys (comma-separated for automatic rotation)
export YOUTUBE_API_KEYS="key1,key2,key3"

# Option 3: Use .env file
echo "YOUTUBE_API_KEY=your_api_key_here" > .env
```

## Basic Usage

### Get channel information by ID

```bash
yt-channel --id UC_x5XG1OV2P6uZZ5FSM9Ttw
```

### Get channel information by handle

```bash
yt-channel --handle @YouTube
```

### Get channel information with human-readable format

```bash
yt-channel --handle @YouTube --format human
```

### Include recent videos

```bash
yt-channel --handle @YouTube --include-videos --max-videos 5
```

### Pretty-print JSON output

```bash
yt-channel --handle @YouTube --format json --pretty
```

## Command-Line Options

```
usage: yt-channel [-h] (--id ID | --handle HANDLE | --url URL)
                  [--include-videos] [--max-videos MAX_VIDEOS]
                  [--format {json,human}] [--pretty] [--keys KEYS]

Options:
  -h, --help            Show help message
  --id ID               Channel ID (e.g., UC_x5XG1OV2P6uZZ5FSM9Ttw)
  --handle HANDLE       Channel handle (e.g., @YouTube)
  --url URL             Channel URL
  --include-videos      Include recent videos in output
  --max-videos N        Maximum number of recent videos (default: 5)
  --format FORMAT       Output format: json or human (default: json)
  --pretty              Pretty-print JSON output
  --keys KEYS           Comma-separated API keys (overrides environment)
```

## Output Examples

### JSON Format (default)

```json
{
  "id": "UC_x5XG1OV2P6uZZ5FSM9Ttw",
  "title": "Google Developers",
  "description": "The Google Developers channel...",
  "custom_url": "@GoogleDevelopers",
  "thumbnails": {
    "default": {"url": "https://..."},
    "medium": {"url": "https://..."},
    "high": {"url": "https://..."}
  },
  "view_count": 50000000,
  "subscriber_count": 2000000,
  "video_count": 5000
}
```

### Human-Readable Format

```
============================================================
Channel: Google Developers
============================================================
ID: UC_x5XG1OV2P6uZZ5FSM9Ttw
Custom URL: @GoogleDevelopers
Description: The Google Developers channel...

Statistics:
  Views: 50,000,000
  Subscribers: 2,000,000
  Videos: 5,000
```

### With Recent Videos

```json
{
  "id": "UC_x5XG1OV2P6uZZ5FSM9Ttw",
  "title": "Google Developers",
  ...
  "recent_videos": [
    {
      "id": "dQw4w9WgXcQ",
      "title": "Recent Video Title",
      "description": "Video description...",
      "view_count": 1000000,
      "like_count": 50000
    }
  ]
}
```

## Error Handling

The tool will return non-zero exit codes on errors:

- Missing API key: Exit code 1
- Channel not found: Exit code 1
- API quota exceeded: Exit code 1
- Network errors: Exit code 1

Error messages are printed to stderr.

## Development

### Running Tests

```bash
# Unit tests only
uv run pytest tests/unit/ -v

# All tests (including E2E, requires API key)
uv run pytest -v

# With coverage
uv run pytest --cov=src/tdd_python_demo/youtube_api --cov-report=term-missing
```

### Test Coverage

Current coverage: **94%**
- `client.py`: 97%
- `formatter.py`: 100%
- `cli_channel.py`: 83%

## API Quotas

YouTube Data API v3 has daily quotas. Each request costs quota units:
- Channel information: ~3 units
- Video search: ~100 units
- Video details: ~1 unit per video

Default quota: 10,000 units/day

Use multiple API keys with `YOUTUBE_API_KEYS` for automatic rotation when quota is exceeded.
