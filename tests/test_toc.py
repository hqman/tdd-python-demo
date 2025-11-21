"""Tests for the Markdown TOC generator."""

from tdd_python_demo.toc import generate_toc


def test_empty_input_returns_empty_list():
    """Test that empty markdown returns an empty TOC list."""
    result = generate_toc("")
    assert result == []


def test_single_h1_heading():
    """Test that a single H1 heading is correctly extracted."""
    markdown = "# Hello World"
    result = generate_toc(markdown)
    expected = [
        {
            'level': 1,
            'text': 'Hello World',
            'slug': 'hello-world'
        }
    ]
    assert result == expected


def test_heading_with_extra_whitespace():
    """Test that leading and trailing whitespace is trimmed from heading text."""
    markdown = "###   Hello World  "
    result = generate_toc(markdown)
    expected = [
        {
            'level': 3,
            'text': 'Hello World',
            'slug': 'hello-world'
        }
    ]
    assert result == expected


def test_multiple_headings_in_order():
    """Test that multiple headings are extracted and maintain order."""
    markdown = """# Title
## Section One
### Deep
## Section Two"""
    result = generate_toc(markdown)
    expected = [
        {'level': 1, 'text': 'Title', 'slug': 'title'},
        {'level': 2, 'text': 'Section One', 'slug': 'section-one'},
        {'level': 3, 'text': 'Deep', 'slug': 'deep'},
        {'level': 2, 'text': 'Section Two', 'slug': 'section-two'},
    ]
    assert result == expected


def test_all_heading_levels():
    """Test that all heading levels 1-6 are correctly identified."""
    markdown = """# Level 1
## Level 2
### Level 3
#### Level 4
##### Level 5
###### Level 6"""
    result = generate_toc(markdown)
    expected = [
        {'level': 1, 'text': 'Level 1', 'slug': 'level-1'},
        {'level': 2, 'text': 'Level 2', 'slug': 'level-2'},
        {'level': 3, 'text': 'Level 3', 'slug': 'level-3'},
        {'level': 4, 'text': 'Level 4', 'slug': 'level-4'},
        {'level': 5, 'text': 'Level 5', 'slug': 'level-5'},
        {'level': 6, 'text': 'Level 6', 'slug': 'level-6'},
    ]
    assert result == expected


def test_slug_removes_special_characters():
    """Test that special characters are removed from slugs."""
    markdown = "# Hello, World!"
    result = generate_toc(markdown)
    expected = [
        {
            'level': 1,
            'text': 'Hello, World!',
            'slug': 'hello-world'
        }
    ]
    assert result == expected


def test_slug_collapses_multiple_spaces():
    """Test that multiple spaces are collapsed to a single dash in slugs."""
    markdown = "## Deep   Title"
    result = generate_toc(markdown)
    expected = [
        {
            'level': 2,
            'text': 'Deep   Title',
            'slug': 'deep-title'
        }
    ]
    assert result == expected


def test_ignore_headings_in_code_blocks():
    """Test that headings inside code blocks are ignored."""
    markdown = """# A

```bash
## Not Real
```

## B"""
    result = generate_toc(markdown)
    expected = [
        {'level': 1, 'text': 'A', 'slug': 'a'},
        {'level': 2, 'text': 'B', 'slug': 'b'},
    ]
    assert result == expected


def test_code_block_with_various_language_specifiers():
    """Test that code blocks with different language specifiers are handled."""
    markdown = """# Title

```python
# Not a heading
def foo(): pass
```

## Section

```javascript
## Also not a heading
```

### Subsection"""
    result = generate_toc(markdown)
    expected = [
        {'level': 1, 'text': 'Title', 'slug': 'title'},
        {'level': 2, 'text': 'Section', 'slug': 'section'},
        {'level': 3, 'text': 'Subsection', 'slug': 'subsection'},
    ]
    assert result == expected


def test_malformed_headings_are_ignored():
    """Test that malformed heading syntax is safely ignored."""
    markdown = """# Valid Heading
##No space after hashes
#######Too many hashes
##
# Valid One Word
## Also Valid"""
    result = generate_toc(markdown)
    expected = [
        {'level': 1, 'text': 'Valid Heading', 'slug': 'valid-heading'},
        {'level': 1, 'text': 'Valid One Word', 'slug': 'valid-one-word'},
        {'level': 2, 'text': 'Also Valid', 'slug': 'also-valid'},
    ]
    assert result == expected


def test_edge_cases_leading_trailing_dashes():
    """Test edge cases: slugs with leading/trailing dashes are cleaned up."""
    markdown = """# --Title--
## (Parentheses)
### !Special!"""
    result = generate_toc(markdown)
    expected = [
        {'level': 1, 'text': '--Title--', 'slug': 'title'},
        {'level': 2, 'text': '(Parentheses)', 'slug': 'parentheses'},
        {'level': 3, 'text': '!Special!', 'slug': 'special'},
    ]
    assert result == expected
