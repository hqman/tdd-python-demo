Markdown TOC Generator – Specification / Requirement Document


1. Overview

The goal is to implement a function that parses a Markdown document and produces a structured table of contents (TOC).
The TOC must reflect the heading hierarchy of the document, ordered by appearance.

This spec defines:

required input format

required output format

features

edge cases

constraints

acceptance criteria (for writing tests)

2. Function Interface
2.1 Name

generate_toc

2.2 Input

markdown: str
A string containing Markdown content (full document).

2.3 Output

A list of TOC items:

[
    {
        'level': int,       # heading level (1–6)
        'text': str,        # heading text without hashes
        'slug': str         # URL-friendly slug
    },
    ...
]

3. Heading Rules
3.1 Supported Headings

Only ATX-style headings:

# H1
## H2
### H3
#### H4
##### H5
###### H6

3.2 Extraction Rules

A heading starts with 1–6 consecutive '#' characters

Must be followed by at least one space

Extract the text after the space

Leading and trailing whitespace should be trimmed

Example:

###   Hello World  


Produces:

level: 3

text: "Hello World"

4. Slug Rules

Slugs are created as follows:

Convert to lowercase

Trim whitespace

Replace spaces with dashes

Remove characters other than letters, numbers, and dashes (a-z0-9-)

Collapse multiple spaces to a single dash

Example:

"Hello, World!" → "hello-world"
"   Deep   Title   " → "deep-title"

5. Code Block Handling
5.1 TOC must ignore headings inside fenced code blocks

Example:

# Real Title

```python
# Not a real heading
def foo(): pass

Real Section

TOC should include:

- "Real Title"
- "Real Section"

### 5.2 Detection Rules  
A fenced code block begins and ends with a line starting with:



Language specifiers (like ```python) must be allowed and ignored.

Inside a code block:

all content must be ignored

headings must not be parsed

6. Ordering

TOC items must appear in the same order as the headings appear in the input Markdown.

7. Error Handling

The function must not raise exceptions for malformed markdown

Invalid heading lines should be ignored

Return an empty list if no headings exist

8. Examples
8.1 Single Heading

Input:

# Hello World


Output:

[
    {'level': 1, 'text': 'Hello World', 'slug': 'hello-world'}
]

8.2 Mixed Headings

Input:

# Title
## Section One
### Deep
## Section Two


Output:

[
    {'level': 1, 'text': 'Title', 'slug': 'title'},
    {'level': 2, 'text': 'Section One', 'slug': 'section-one'},
    {'level': 3, 'text': 'Deep', 'slug': 'deep'},
    {'level': 2, 'text': 'Section Two', 'slug': 'section-two'},
]

8.3 Code Block Ignoring

Input:

# A

```bash
## Not Real

B

Output:

```python
[
    {'level': 1, 'text': 'A', 'slug': 'a'},
    {'level': 2, 'text': 'B', 'slug': 'b'},
]

9. Constraints

Must not use external Markdown parsing libraries (pure parsing)

Code should be deterministic and pure (no I/O)

Data structures must be JSON-serializable

10. Acceptance Criteria 

Extract single h1 heading

Extract multiple headings

Extract different levels (h1–h6)

Slug generation rules

Ignore code block headings

Handle malformed lines safely

Handle empty input

Correct ordering

TOC is considered correct only if:

All rules are satisfied

All test cases pass
The implementation produces minimal behavior needed for the tests



CLI Command

11.1 Overview

In addition to the pure function interface, the project must provide a simple command-line interface (CLI) to generate a TOC from a Markdown file on disk.

The CLI is a thin wrapper around generate_toc.

11.2 Command Name

Recommended command name:

markdown-toc

(The exact binary name can be adjusted, but it must be documented and consistent.)

11.3 Usage

Basic usage:


md-toc path/to/file.md
You should implement e2e tests yourself to ensure the command runs, using the real test.md file for testing.

The ultimate goal is for the command to produce the correct TOC.
A visual indentation feature `with_tree_format` is required.