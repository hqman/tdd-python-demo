"""Formatter functions for YouTube API output."""

import json


def format_json(data, pretty=False):
    """Format data as JSON string.

    Args:
        data: Data to format (dict, list, etc.)
        pretty: If True, format with indentation

    Returns:
        JSON string representation of data
    """
    indent = 2 if pretty else None
    return json.dumps(data, indent=indent)


def format_human(video_info):
    """Format video information as human-readable text.

    Args:
        video_info: Dictionary containing video information

    Returns:
        Human-readable string with video details
    """
    lines = [
        f"Title: {video_info.get('title', 'N/A')}",
        f"Channel: {video_info.get('channel', 'N/A')}",
        f"Views: {video_info.get('views', 'N/A')}",
        f"Likes: {video_info.get('likes', 'N/A')}"
    ]
    return "\n".join(lines)
