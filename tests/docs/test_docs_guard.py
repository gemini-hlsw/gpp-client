"""
Tests that keep the docs site self-contained.

No page may point to the repo docs the site never links.
"""

import re
from pathlib import Path

import pytest

_SOURCE = Path(__file__).resolve().parents[2] / "docs" / "source"
_PAGES = sorted(path.relative_to(_SOURCE).as_posix() for path in _SOURCE.rglob("*.rst"))

# The maintainer's agent workflow owns these files, and they change without
# the site; the site must stand on its own.
_OUTSIDE_REFERENCE = re.compile(
    r"(?:docs|\.\.)/(?:adr|agents)\b|\b(?:GLOSSARY|ARCHITECTURE|OVERVIEW|AGENTS)\.md\b"
)


def outside_references(text: str) -> list[str]:
    """
    Return each reference to a repo doc that the site never points to.

    Parameters
    ----------
    text : str
        The reStructuredText of one page.

    Returns
    -------
    list[str]
        The matched references, in page order.
    """
    return _OUTSIDE_REFERENCE.findall(text)


@pytest.mark.parametrize(
    "reference",
    [
        "`ADR 6 <https://github.com/gemini-hlsw/gpp-client/blob/main/docs/adr/0006.md>`_",
        "See ``docs/agents/schema-update.md``.",
        "`the glossary <../GLOSSARY.md>`_",
        "Read ARCHITECTURE.md first.",
        "`overview <https://github.com/gemini-hlsw/gpp-client/blob/main/docs/OVERVIEW.md>`__",
        "Agents read AGENTS.md.",
        "`ADR 6 <../adr/0006-merged-schema-runtime-environment.md>`_",
        "`schema update <../../agents/schema-update.md>`_",
    ],
)
def test_reference_to_a_repo_doc_outside_the_site_is_found(reference):
    assert outside_references(f"Intro.\n\n{reference}\n") != []


def test_page_without_repo_doc_references_passes():
    text = "See :doc:`environment` and `GPP <https://gpp.gemini.edu>`_.\n"

    assert outside_references(text) == []


@pytest.mark.parametrize("page", _PAGES)
def test_page_never_points_outside_the_site(page):
    assert outside_references((_SOURCE / page).read_text()) == []
