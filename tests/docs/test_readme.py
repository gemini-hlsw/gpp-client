"""
Tests that the README's Python quickstart shows the Getting started example.

The README is read on GitHub and PyPI, where it cannot include files, so its
quickstart is a copy of the Getting started page's example. This test fails
when the copy drifts.
"""

import re
from pathlib import Path

from tests.docs.test_doc_examples import python_blocks

_ROOT = Path(__file__).resolve().parents[2]
_README = _ROOT / "README.md"
_GETTING_STARTED = _ROOT / "docs" / "source" / "getting-started.rst"
_PYTHON_FENCE = re.compile(r"^```python\n(.*?)^```", re.MULTILINE | re.DOTALL)


def _code_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def shows_lines(readme: str, lines: list[str]) -> bool:
    """
    Return whether one of the README's Python blocks shows ``lines`` in order.

    The README wraps the snippets in a runnable script, so other lines may sit
    between them.

    Parameters
    ----------
    readme : str
        The README's Markdown.
    lines : list[str]
        Code lines, stripped of indent.

    Returns
    -------
    bool
        Whether a Python block holds every line, in order.
    """
    for block in _PYTHON_FENCE.findall(readme):
        shown = iter(_code_lines(block))
        if all(line in shown for line in lines):
            return True
    return False


_EXAMPLE_LINES = [
    'result = await client.program.get_by_id("p-123")',
    "print(result.program)",
]


def test_readme_showing_the_example_lines_passes():
    readme = (
        "Make a call:\n\n```python\nasync def main():\n"
        "    async with GPPClient() as client:\n"
        '        result = await client.program.get_by_id("p-123")\n\n'
        "        print(result.program)\n```\n"
    )

    assert shows_lines(readme, _EXAMPLE_LINES)


def test_readme_with_a_changed_line_fails():
    readme = (
        "```python\n"
        'result = await client.program.get("p-123")\n'
        "print(result.program)\n```\n"
    )

    assert not shows_lines(readme, _EXAMPLE_LINES)


def test_readme_quickstart_matches_the_getting_started_example():
    blocks = python_blocks(_GETTING_STARTED.read_text())
    lines = _code_lines(blocks[0].code)

    assert shows_lines(_README.read_text(), lines), lines
