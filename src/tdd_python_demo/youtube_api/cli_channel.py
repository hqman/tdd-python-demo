"""CLI tool for YouTube channel information."""

import sys
import argparse
import os
from dotenv import load_dotenv

from .client import YouTubeClient
from .formatter import format_json, format_channel_profile


def main():
    """Main entry point for yt-channel CLI."""
    load_dotenv()

    parser = argparse.ArgumentParser(description="Get YouTube channel information")
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--id', help='Channel ID')
    input_group.add_argument('--handle', help='Channel handle')
    input_group.add_argument('--url', help='Channel URL')

    parser.add_argument('--include-videos', action='store_true', help='Include recent videos')
    parser.add_argument('--max-videos', type=int, default=5, help='Max recent videos')
    parser.add_argument('--format', choices=['json', 'human'], default='json', help='Output format')
    parser.add_argument('--pretty', action='store_true', help='Pretty print JSON')
    parser.add_argument('--keys', help='API keys')

    args = parser.parse_args()

    api_keys = args.keys or os.getenv('YOUTUBE_API_KEYS') or os.getenv('YOUTUBE_API_KEY')
    if not api_keys:
        print("Error: No API key provided", file=sys.stderr)
        return 1

    channel_input = args.id or args.handle or args.url

    try:
        client = YouTubeClient(api_keys)
        channel_data = client.get_channel_profile(
            channel_input,
            include_recent_videos=args.include_videos,
            max_videos=args.max_videos
        )

        if args.format == 'json':
            output = format_json(channel_data, pretty=args.pretty)
        else:
            output = format_channel_profile(channel_data)

        print(output)
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
