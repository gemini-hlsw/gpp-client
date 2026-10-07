"""
Show the generated ``Available on: ...`` docstring line as a badge.

The codegen plugin ``AvailabilityDocstringsPlugin`` writes that line first in
the docstring of every environment-specific generated part, so the reference
pages and editors read the same source.
"""

import re

LABEL = "Available on: "
AVAILABILITY_LINE = re.compile(rf"^({re.escape(LABEL)}[^.]+)\.$")
ENVIRONMENT_NAME = re.compile(r"^[a-z]+$")


def badge_lines(lines: list[str]) -> None:
    """
    Turn a leading availability line into the ``availability`` role, in place.

    Parameters
    ----------
    lines : list[str]
        A docstring's lines, as autodoc hands them to extensions.
    """
    if lines and (match := AVAILABILITY_LINE.match(lines[0])):
        lines[0] = f":availability:`{match.group(1)}`"


def pills(text: str) -> list[tuple[str, list[str]]]:
    """
    Split an ``availability`` role's text into one pill per environment.

    Parameters
    ----------
    text : str
        The role text, such as ``"Available on: development, production"``.

    Returns
    -------
    list[tuple[str, list[str]]]
        Each environment name with its pill's HTML classes. A plain
        environment name adds ``availability-<environment>``, which picks its
        color in ``availability.css``; anything else gets the neutral pill.
    """
    return [
        (name, _pill_classes(name)) for name in text.removeprefix(LABEL).split(", ")
    ]


def badge_parts(text: str) -> list[tuple[str, list[str]]]:
    """
    Return a badge's pills with a hidden separator between each pair.

    The separator is hidden on screen but copied, so copied text reads
    ``development, production``.

    Parameters
    ----------
    text : str
        The role text, such as ``"Available on: development, production"``.

    Returns
    -------
    list[tuple[str, list[str]]]
        Each part's text with its HTML classes, in order.
    """
    parts = []
    for pill in pills(text):
        if parts:
            parts.append((", ", ["availability-separator"]))
        parts.append(pill)
    return parts


def _pill_classes(name: str) -> list[str]:
    if ENVIRONMENT_NAME.match(name):
        return ["availability-pill", f"availability-{name}"]
    return ["availability-pill"]


def _process_docstring(app, what, name, obj, options, lines) -> None:
    badge_lines(lines)


def _availability_role(
    name, rawtext, text, lineno, inliner, options=None, content=None
):
    from docutils import nodes

    badge = nodes.inline(rawtext, "", nodes.Text(LABEL), classes=["availability"])
    badge += [
        nodes.inline(part, part, classes=classes) for part, classes in badge_parts(text)
    ]
    return [badge], []


def setup(app):
    app.add_role("availability", _availability_role)
    app.add_css_file("availability.css")
    # Before napoleon, which reads "Available on: x." on an attribute as a type.
    app.connect("autodoc-process-docstring", _process_docstring, priority=400)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
