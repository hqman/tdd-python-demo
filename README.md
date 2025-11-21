# TDD Python Demo

A pedagogical project demonstrating strict **Test-Driven Development (TDD)** workflows in Python using `pytest` and `tdd-guard`.

## 🚀 TDD Methodology

This project enforces the **Red-Green-Refactor** cycle. Every feature or fix must follow these steps:

1.  🔴 **Red Phase**: Write **ONE** failing test that describes the desired behavior.
2.  🟢 **Green Phase**: Write the **MINIMAL** code required to make that test pass.
3.  🔵 **Refactor Phase**: Improve code structure without changing behavior, ensuring all tests remain green.

### Key Rules
*   **One test at a time**: Do not add multiple tests simultaneously.
*   **No implementation without tests**: Every line of production code must be justified by a failing test.
*   **Incremental design**: Build complex logic step-by-step through simple, focused tests.

---

## 🛠️ Environment Setup

This project uses [uv](https://github.com/astral-sh/uv) for fast Python package management.

### 1. Install uv
```bash
# MacOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Create Virtual Environment
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
uv sync
```

---

## 🛡️ TDD Guard Setup

To enforce the TDD cycle, this project uses `tdd-guard`.

### 1. Install CLI Tool
**Using npm:**
```bash
npm install -g tdd-guard
```
**Or using Homebrew:**
```bash
brew install tdd-guard
```

### 2. Python Adapter
The `tdd-guard-pytest` adapter is installed automatically via `uv sync`.

**Configuration:**
Update `pyproject.toml` with your absolute project path:
```toml
[tool.pytest.ini_options]
# ⚠️ IMPORTANT: Replace this path with your actual project root absolute path!
tdd_guard_project_root = "/Users/yourname/projects/tdd-python-demo"
```

### 3. Configure Hooks
To automatically enforce TDD rules during development, configure hooks in `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit|TodoWrite",
        "hooks": [
          {
            "type": "command",
            "command": "tdd-guard"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "tdd-guard"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup|resume|clear",
        "hooks": [
          {
            "type": "command",
            "command": "tdd-guard"
          }
        ]
      }
    ]
  }
}
```

---

## 📂 Demo Projects

This repository contains three distinct examples of TDD implementation:

### 1. Calculator
*   **Spec**: `specs/calculator.md`
*   **Goal**: A simple class implementing basic arithmetic operations.
*   **Focus**: Basics of TDD, unit testing class methods.

### 2. Markdown TOC Generator
*   **Spec**: `specs/markdown_toc.md`
*   **Goal**: A pure function that parses Markdown to generate a Table of Contents (TOC) and a CLI tool `md-toc`.
*   **Focus**: String processing, edge cases, functional testing, and CLI wrapping.

### 3. YouTube API Client (`yt-fetch` & `yt-channel`)
*   **Spec**: `specs/youtube_channel.md`, `specs/youtube_video.md`
*   **Goal**: A robust API client with key rotation, exponential backoff/retries, and CLI tools for fetching channel/video data.
*   **Focus**: Integration testing, mocking network requests, handling API quotas/errors, and complex CLI arguments.

---

## 🧪 Running Tests

Run all tests:
```bash
uv run pytest -v
```

Run specific tests (e.g., for the YouTube project):
```bash
uv run pytest tests/unit/test_client.py
```

Run with coverage:
```bash
uv run pytest --cov=src
```
