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
    if pretty:
        return json.dumps(data, indent=2)
    return json.dumps(data)
