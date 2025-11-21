"""Markdown Table of Contents (TOC) generator."""

import re


def _create_slug(text: str) -> str:
    """
    Create a URL-friendly slug from heading text.

    Args:
        text: The heading text.

    Returns:
        A slugified version of the text.
    """
    # Convert to lowercase and replace spaces with dashes
    slug = text.lower().replace(' ', '-')
    # Remove all characters except alphanumeric and dashes
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    # Collapse multiple dashes into a single dash
    slug = re.sub(r'-+', '-', slug)
    # Strip leading and trailing dashes
    slug = slug.strip('-')
    return slug


def generate_toc(markdown: str) -> list:
    """
    Generate a table of contents from Markdown content.

    Parses ATX-style headings (# through ######) and creates a structured
    TOC with heading levels, text, and URL-friendly slugs. Ignores headings
    inside fenced code blocks.

    Args:
        markdown: A string containing Markdown content.

    Returns:
        A list of TOC items, where each item is a dict with:
        - 'level': int (1-6)
        - 'text': str (heading text without hashes)
        - 'slug': str (URL-friendly slug)
    """
    if not markdown:
        return []

    toc = []
    lines = markdown.split('\n')
    in_code_block = False

    for line in lines:
        # Check for code block fences (with or without language specifiers)
        if line.startswith('```'):
            in_code_block = not in_code_block
            continue

        # Skip lines inside code blocks
        if in_code_block:
            continue

        # Match ATX-style headings: 1-6 '#' followed by space and text
        match = re.match(r'^(#{1,6}) (.+)$', line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            slug = _create_slug(text)

            toc.append({
                'level': level,
                'text': text,
                'slug': slug
            })

    return toc
