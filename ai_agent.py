import os
import re
from pathlib import Path

import anthropic
from dotenv import load_dotenv


load_dotenv()


def review_code(file_path):
    """Review and safely fix a Python file using Claude."""

    path = Path(file_path)

    if not path.exists():
        print(f"File not found: {file_path}")
        return

    original_code = path.read_text(encoding="utf-8")

    prompt = f"""
You are a Python Code Review Agent.

Review the following Python code and look ONLY for these basic issues:

- Unused imports
- Unused variables
- Missing function docstrings
- Poor variable names such as a, b, x, y, temp
- Simple PEP8 style issues
- Missing blank lines between functions
- Obvious code readability improvements

Rules:
1. Keep the existing functionality unchanged.
2. Make only safe improvements.
3. Do not add new functionality.
4. Do not remove functionality.
5. Return a short review summary.
6. Return the complete corrected Python code.
7. If no changes are required, return the original code unchanged.

Use exactly this format:

## Review Summary
- Issue 1: <issue>
- Issue 2: <issue>

## Fixed Code
```python
<complete corrected Python code>