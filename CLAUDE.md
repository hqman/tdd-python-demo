# Development Principles

TDD is a non-negotiable engineering standard. All features, changes, and bug fixes must follow the strict Test-Driven workflow: write tests first, confirm tests fail, implement the minimal code required to make them pass, then refactor.

The Red-Green-Refactor cycle must be followed for **every** task. No code may be merged without corresponding tests created beforehand. TDD ensures clarity of requirements, prevents regressions, improves design quality, and guarantees predictable, repeatable delivery. All team members are responsible for applying TDD consistently and rejecting any work that does not meet this standard.

## Refactor Phase
Improve the design while ensuring all tests remain green.
**Goals:**
* Clean up code
* Remove duplication
* Improve structure and readability
* Organize naming, abstractions, and module relationships
* Ensure all tests stay green (no new failures)

The Refactor Phase must be completed independently for every task.

## Additional TDD Rules

* Only **one** test may be developed at a time — write one failing test, then implement the minimal code to make it pass, then refactor.
* Adding multiple new tests at once (for example, adding five new tests simultaneously in a new test file) is strictly prohibited — doing so violates the workflow.
* Even when **adding or updating tests** (for example, additional coverage tests, regression tests, bug-fix tests), the same TDD cycle must be followed:
  1. Write the new test (which should fail).
  2. Write the minimal code change needed to make the test pass.
  3. Refactor as needed. This must be done for every task to check edge cases and improve code robustness. It cannot be skipped.

When executing tasks, display appropriate titles, for example:
🔴 Red Phase
🟢 Green Phase
🔵 Refactor Phase

# TDD Guard Quick Commands
tdd-guard on - Enables TDD Guard enforcement
tdd-guard off - Disables TDD Guard enforcement

# Development Environment

The project uses **uv** to manage the Python environment and dependencies.
Before running tests:

1. Run `source .venv/bin/activate` to activate the virtual environment.
2. Activate the `uv` virtual environment first when you run `pytest`.

# Code Directory Structure

src/                      # All production code lives here
tests/                    # Test code
scripts/                  # Developer utility scripts (optional)

## tests/ Directory
1. unit/ — small, fast, isolated tests
   * Test individual functions or small classes
   * No I/O, no network, no filesystem
   * Uses mocks only when necessary
   * Example: test_core_logic.py, test_utils.py

2. integration/ — components working together
   * Tests interactions between modules
   * Minimal mocking
   * May read small files or use lightweight infrastructure
   * Example: test_markdown_parser.py, test_toc_pipeline.py

3. e2e/ — full application behavior
   * Tests the real user flow end-to-end
   * Calls CLI tools, processes full markdown files, or interacts with external APIs
   * Slowest but most realistic
   * Example: test_cli_commands.py, test_user_flow_generate_toc.py
