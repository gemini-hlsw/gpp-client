"""
Tests that every Python example in the docs type-checks against the client.

Each Python block on a page becomes the body of
``async def _example(client: GPPClient) -> None``, and one ty run checks them
all. A renamed method, a wrong argument or a name the block never defines
fails here. Examples never run, so a wrong return shape is not caught. A block
that should not be checked sits right under a
``.. docs-guard: skip - <reason>`` comment.
"""

import re
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import NamedTuple

import pytest

_ROOT = Path(__file__).resolve().parents[2]

_CODE_DIRECTIVE = re.compile(r"^\s*\.\. (?:code-block|code|sourcecode)::\s*(\S*)")
_DIRECTIVE_OPTION = re.compile(r"^\s+:[\w-]+:")
# Sphinx's default highlight language is Python, so a bare block counts.
_PYTHON_LANGUAGES = {"", "default", "python", "python3", "py", "py3", "pycon"}
_SKIP_MARKER = ".. docs-guard: skip"
_EXAMPLE_HEADER = (
    "from gpp_client import GPPClient\n\n\n"
    "async def _example(client: GPPClient) -> None:\n"
)
_DIAGNOSTIC = re.compile(
    r"^(?P<path>.+?\.py):(?P<line>\d+):(?P<column>\d+): (?P<rest>.*)$"
)


class Block(NamedTuple):
    """
    One Python block on a page.
    """

    line: int
    code: str


def python_blocks(text: str) -> list[Block]:
    """
    Return the page's Python blocks that are not marked skip.

    Parameters
    ----------
    text : str
        The reStructuredText of one page.

    Returns
    -------
    list[Block]
        Each block's code, dedented, with the one-based page line of its first
        code line.
    """
    lines = text.splitlines()
    blocks = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not _opens_code_content(line):
            index += 1
            continue
        end = _content_end(lines, index)
        first = _first_code_line(lines, index, end)
        if first < end and _is_python(line) and not _marked_skip(lines, index):
            code = textwrap.dedent("\n".join(lines[first:end]))
            blocks.append(Block(first + 1, code))
        # A code block's content is sample text, so directives shown in it
        # (an ``rst`` sample, say) are not blocks of this page.
        index = end
    return blocks


def _is_python(line: str) -> bool:
    directive = _CODE_DIRECTIVE.match(line)
    if directive is not None:
        return directive[1] in _PYTHON_LANGUAGES
    return True


def _is_literal_block(line: str) -> bool:
    stripped = line.strip()
    return stripped.endswith("::") and not stripped.startswith("..")


def _opens_code_content(line: str) -> bool:
    return _CODE_DIRECTIVE.match(line) is not None or _is_literal_block(line)


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip())


def _content_end(lines: list[str], index: int) -> int:
    end = index + 1
    while end < len(lines) and (
        not lines[end].strip() or _indent(lines[end]) > _indent(lines[index])
    ):
        end += 1
    while end > index + 1 and not lines[end - 1].strip():
        end -= 1
    return end


def _first_code_line(lines: list[str], index: int, end: int) -> int:
    first = index + 1
    while first < end and (
        not lines[first].strip() or _DIRECTIVE_OPTION.match(lines[first])
    ):
        first += 1
    return first


def _marked_skip(lines: list[str], index: int) -> bool:
    # A literal block opens on its paragraph's last line, but the marker
    # goes above the whole paragraph.
    while index > 0 and lines[index - 1].strip():
        index -= 1
    previous = [line.strip() for line in lines[:index] if line.strip()]
    return bool(previous) and previous[-1].startswith(_SKIP_MARKER)


def type_errors(source: Path, work: Path) -> list[str]:
    """
    Type-check every Python block under ``source`` in one ty run.

    Parameters
    ----------
    source : Path
        The docs source folder.
    work : Path
        An empty folder for the wrapped examples.

    Returns
    -------
    list[str]
        One ``<page>:<line>: <diagnostic>`` per ty error, or ty's whole output
        when it failed without naming a file.
    """
    work.mkdir(parents=True, exist_ok=True)
    origins = {}
    for page in sorted(source.rglob("*.rst")):
        name = page.relative_to(source).as_posix()
        for block in python_blocks(page.read_text()):
            module = work / f"example_{len(origins)}.py"
            module.write_text(_EXAMPLE_HEADER + textwrap.indent(block.code, "    "))
            origins[module.name] = (name, block.line)
    if not origins:
        return []
    ty = [sys.executable, "-m", "ty", "check", "--error-on-warning"]
    options = ["--project", str(_ROOT), "--python", sys.prefix]
    result = subprocess.run(
        [*ty, *options, "--output-format", "concise", str(work)],
        capture_output=True,
        text=True,
        check=False,
    )
    errors = []
    for line in result.stdout.splitlines():
        diagnostic = _DIAGNOSTIC.match(line)
        if diagnostic is None:
            continue
        page, first = origins[Path(diagnostic["path"]).name]
        page_line = first + int(diagnostic["line"]) - _EXAMPLE_HEADER.count("\n") - 1
        errors.append(f"{page}:{page_line}: {diagnostic['rest']}")
    if result.returncode != 0 and not errors:
        return [result.stdout + result.stderr]
    return errors


def _write_page(source: Path, text: str) -> None:
    page = source / "guides" / "page.rst"
    page.parent.mkdir(parents=True)
    page.write_text(text)


@pytest.mark.parametrize(
    ("call", "rule"),
    [
        ('await client.program.get_by_idx("p-123")', "unresolved-attribute"),
        ('await client.program.get_by_id("p-123", limit=1)', "unknown-argument"),
        ("print(program)", "unresolved-reference"),
    ],
)
def test_block_with_a_type_error_fails_naming_page_and_line(tmp_path, call, rule):
    _write_page(
        tmp_path / "source",
        f"Intro.\n\n.. code-block:: python\n\n   x = 1\n   {call}\n",
    )

    errors = type_errors(tmp_path / "source", tmp_path / "work")

    assert len(errors) == 1
    assert errors[0].startswith("guides/page.rst:6:")
    assert rule in errors[0]


@pytest.mark.parametrize(
    "code",
    [
        'result = await client.program.get_by_id("p-123")\n   print(result.program)',
        "from gpp_client import GPPClient\n\n"
        "   async with GPPClient() as client:\n"
        '       result = await client.program.get_by_id("p-123")',
    ],
)
def test_correct_block_passes(tmp_path, code):
    _write_page(tmp_path / "source", f".. code-block:: python\n\n   {code}\n")

    assert type_errors(tmp_path / "source", tmp_path / "work") == []


def test_block_marked_skip_is_not_checked(tmp_path):
    _write_page(
        tmp_path / "source",
        ".. docs-guard: skip - shows a renamed method on purpose\n\n"
        ".. code-block:: python\n\n"
        '   await client.program.get_by_idx("p-123")\n',
    )

    assert type_errors(tmp_path / "source", tmp_path / "work") == []


@pytest.mark.parametrize(
    "directive",
    [
        ".. code-block:: python",
        ".. code:: python",
        ".. sourcecode:: py",
        ".. code-block:: pycon",
        ".. code-block:: python3",
        ".. code-block::",
    ],
)
def test_python_directive_block_is_found(directive):
    text = f"Intro.\n\n{directive}\n\n   x = 1\n"

    assert python_blocks(text) == [Block(5, "x = 1")]


@pytest.mark.parametrize(
    ("paragraph", "line"), [("Run this::", 3), ("Run this:\n\n::", 5)]
)
def test_literal_block_is_found(paragraph, line):
    text = f"{paragraph}\n\n   x = 1\n"

    assert python_blocks(text) == [Block(line, "x = 1")]


def test_block_drops_its_options_and_indent():
    text = (
        "- Item:\n\n"
        "  .. code-block:: python\n     :caption: Example\n\n"
        "     if x:\n         y = 1\n\n"
        "Next paragraph.\n"
    )

    assert python_blocks(text) == [Block(6, "if x:\n    y = 1")]


def test_directive_without_arguments_is_not_a_literal_block():
    assert python_blocks(".. note::\n\n   Read this.\n") == []


def test_block_marked_skip_above_its_paragraph_is_skipped():
    text = (
        "Intro.\n\n.. docs-guard: skip - shows invalid code on purpose\n\n"
        "Some words\nthen run this::\n\n   x = 1\n"
    )

    assert python_blocks(text) == []


def test_block_marked_skip_inside_a_directive_is_skipped():
    text = (
        ".. tip::\n\n"
        "   .. docs-guard: skip - shows invalid code on purpose\n\n"
        "   .. code-block:: python\n\n      x = 1\n"
    )

    assert python_blocks(text) == []


def test_skip_marker_covers_only_the_next_block():
    text = (
        ".. docs-guard: skip - shows invalid code on purpose\n\n"
        ".. code-block:: python\n\n   x = 1\n\n"
        ".. code-block:: python\n\n   y = 2\n"
    )

    assert python_blocks(text) == [Block(9, "y = 2")]


@pytest.mark.parametrize(
    "sample", [".. code-block:: python\n\n      x = 1", "Run this::\n\n      x = 1"]
)
def test_block_shown_inside_an_rst_sample_is_not_a_block(sample):
    text = f"Write this:\n\n.. code-block:: rst\n\n   {sample}\n\nThen build.\n"

    assert python_blocks(text) == []


def test_block_after_an_rst_sample_is_still_found():
    text = (
        ".. code-block:: rst\n\n   .. note::\n\n      Text.\n\n"
        ".. code-block:: python\n\n   x = 1\n"
    )

    assert python_blocks(text) == [Block(9, "x = 1")]


def test_shell_block_is_not_python():
    text = "Install:\n\n.. code-block:: bash\n\n   pip install gpp-client\n"

    assert python_blocks(text) == []


def test_every_docs_example_type_checks(tmp_path):
    errors = type_errors(_ROOT / "docs" / "source", tmp_path)

    assert errors == [], "\n".join(errors)
