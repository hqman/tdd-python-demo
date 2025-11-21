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
    return json.dumps(data, indent=indent, ensure_ascii=False)


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


def format_table(video_info, comments=None):
    """Format video information as ASCII table.

    Args:
        video_info: Dictionary containing video information
        comments: Optional list of comments

    Returns:
        ASCII table string
    """
    result = f"| Title: {video_info.get('title', 'N/A')} | Channel: {video_info.get('channel', 'N/A')} |"
    return result


def format_summary(video_info):
    """Format video information as compact summary.

    Args:
        video_info: Dictionary containing video information

    Returns:
        Compact single-line summary string
    """
    title = video_info.get('title', 'N/A')
    views = video_info.get('views', 'N/A')
    return f"{title} - {views} views"


def format_channel_profile(channel_data):
    """Format channel profile as human-readable text.

    Args:
        channel_data: Dictionary containing channel information

    Returns:
        Human-readable string with channel details
    """
    def format_number(num):
        """Format number with commas."""
        if num is None:
            return "N/A"
        return f"{num:,}"

    lines = [
        "=" * 60,
        f"Channel: {channel_data.get('title', 'N/A')}",
        "=" * 60,
        f"ID: {channel_data.get('id', 'N/A')}",
        f"Custom URL: {channel_data.get('custom_url', 'N/A')}",
        f"Description: {channel_data.get('description', 'N/A')}",
        "",
        "Statistics:",
        f"  Views: {format_number(channel_data.get('view_count'))}",
        f"  Subscribers: {format_number(channel_data.get('subscriber_count'))}",
        f"  Videos: {format_number(channel_data.get('video_count'))}",
    ]

    # Add recent videos if available
    recent_videos = channel_data.get('recent_videos')
    if recent_videos:
        lines.append("")
        lines.append("Recent Videos:")
        for video in recent_videos:
            title = video.get('title', 'N/A')
            views = format_number(video.get('view_count'))
            lines.append(f"  - {title} ({views} views)")

    return "\n".join(lines)
