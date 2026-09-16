import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv


load_dotenv()


def review_code(file_path):
    """Review a Python file using Claude."""

    code = Path(file_path).read_text(encoding="utf-8")

    prompt = f"""
You are a Python Code Review Agent.

Review the following Python code.

Look for ONLY these basic issues:

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
4. Return the review summary and corrected code.

Use exactly this format:

## Review Summary
- Issue 1:
- Issue 2:

## Fixed Code
<corrected Python code>

<python_code>
{code}
</python_code>
"""

    client = anthropic.Anthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"]
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    print(response.content[0].text)


if __name__ == "__main__":
    review_code("calculator.py")