"""End-to-end tests for the CLI using real markdown files."""

import json
import subprocess
import tempfile
from pathlib import Path


def test_e2e_cli_with_real_markdown_file():
    """Test the CLI command with a real markdown file end-to-end."""
    # Create a real markdown file with comprehensive content
    markdown_content = """# Main Title

This is some introductory text.

## Section One

Content for section one.

### Subsection 1.1

More details here.

## Section Two

```python
# This is code, should be ignored
## Not a heading
```

Content after code block.

### Subsection 2.1

Final section.
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(markdown_content)
        temp_file = f.name

    try:
        # Run the actual CLI command using subprocess
        result = subprocess.run(
            ['md-toc', temp_file],
            capture_output=True,
            text=True,
            check=True
        )

        # Parse the JSON output
        toc = json.loads(result.stdout)

        # Verify the structure
        assert len(toc) == 5, f"Expected 5 TOC items, got {len(toc)}"

        # Verify specific entries
        assert toc[0] == {
            'level': 1,
            'text': 'Main Title',
            'slug': 'main-title'
        }

        assert toc[1] == {
            'level': 2,
            'text': 'Section One',
            'slug': 'section-one'
        }

        # Verify code block heading is NOT included
        heading_texts = [item['text'] for item in toc]
        assert 'Not a heading' not in heading_texts

    finally:
        # Clean up
        Path(temp_file).unlink()


def test_e2e_cli_with_tree_format():
    """Test CLI with --format=tree for visual indentation."""
    markdown_content = """# Title
## Section One
### Subsection 1.1
## Section Two
### Subsection 2.1
#### Deep Item
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(markdown_content)
        temp_file = f.name

    try:
        # Run CLI with tree format
        result = subprocess.run(
            ['md-toc', temp_file, '--format=tree'],
            capture_output=True,
            text=True,
            check=True
        )

        output = result.stdout

        # Verify tree structure with visual indentation
        expected_lines = [
            '# Title',
            '  ## Section One',
            '    ### Subsection 1.1',
            '  ## Section Two',
            '    ### Subsection 2.1',
            '      #### Deep Item'
        ]

        for expected_line in expected_lines:
            assert expected_line in output, f"Expected '{expected_line}' in output"

    finally:
        Path(temp_file).unlink()
