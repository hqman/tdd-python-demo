"""Command-line interface for the Markdown TOC generator."""

import argparse
import json
import sys
from pathlib import Path

from .toc import generate_toc


def format_as_tree(toc):
    """Format TOC as a tree with visual indentation."""
    lines = []
    for item in toc:
        indent = '  ' * (item['level'] - 1)
        hashes = '#' * item['level']
        lines.append(f"{indent}{hashes} {item['text']}")
    return '\n'.join(lines)


def main(argv=None):
    """Main entry point for the tdd-toc CLI command."""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Generate TOC from Markdown')
    parser.add_argument('input', type=str, help='Path to Markdown file')
    parser.add_argument('--format', choices=['json', 'tree'], default='json',
                        help='Output format (default: json)')

    args = parser.parse_args(argv)

    markdown_content = Path(args.input).read_text(encoding='utf-8')
    toc = generate_toc(markdown_content)

    if args.format == 'tree':
        print(format_as_tree(toc))
    else:
        print(json.dumps(toc, indent=2, ensure_ascii=False))

    return 0
