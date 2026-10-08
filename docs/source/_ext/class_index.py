"""
Replace ``.. class-index::`` with a table of the classes autodoc put on the page.

The table is built from the rendered page, so it lists exactly the classes the
page documents and changes with the schema, with nothing written by hand.
"""

import re

PLACEHOLDER = "class-index-placeholder"
SENTENCE_END = re.compile(r"(?<=\.)\s+(?=[A-Z])")


def first_sentence(text: str) -> str:
    """
    Return the first sentence of a docstring paragraph, on one line.

    Parameters
    ----------
    text : str
        The paragraph's text.

    Returns
    -------
    str
        Everything up to the first full stop that a capital letter follows, or
        the whole paragraph when there is none.
    """
    return SENTENCE_END.split(" ".join(text.split()), maxsplit=1)[0]


def _summary(desc):
    from docutils import nodes
    from sphinx import addnodes

    content = next(iter(desc.findall(addnodes.desc_content)), None)
    if content is None:
        return []
    cell = []
    for paragraph in content.children:
        if not isinstance(paragraph, nodes.paragraph):
            break
        badges = [
            node.deepcopy()
            for node in paragraph.findall(nodes.inline)
            if "availability" in node["classes"]
        ]
        if badges:
            cell += badges
            continue
        cell.append(nodes.Text(first_sentence(paragraph.astext())))
        break
    return cell


def _top_level_classes(doctree):
    from sphinx import addnodes

    for desc in doctree.findall(addnodes.desc):
        if desc.get("domain") != "py" or desc.get("objtype") not in {
            "class",
            "exception",
        }:
            continue
        parent = desc.parent
        while parent is not None and not isinstance(parent, addnodes.desc):
            parent = parent.parent
        if parent is None:
            yield desc


def _row(desc):
    from docutils import nodes

    signature = desc[0]
    link = nodes.reference(
        "",
        "",
        nodes.literal("", signature["fullname"]),
        internal=True,
        refid=signature["ids"][0],
    )
    row = nodes.row()
    row += nodes.entry("", nodes.paragraph("", "", link))
    row += nodes.entry("", nodes.paragraph("", "", *_summary(desc)))
    return row


def _table(doctree):
    from docutils import nodes

    group = nodes.tgroup(cols=2)
    group += nodes.colspec(colwidth=40)
    group += nodes.colspec(colwidth=60)
    body = nodes.tbody()
    body += [_row(desc) for desc in _top_level_classes(doctree)]
    group += body
    return nodes.table("", group, classes=["class-index"])


def _replace_placeholders(app, doctree) -> None:
    from docutils import nodes

    for placeholder in list(doctree.findall(nodes.container)):
        if PLACEHOLDER in placeholder["classes"]:
            table = _table(doctree)
            placeholder.replace_self(table)
            table["classes"] = ["class-index"]


def setup(app):
    from docutils import nodes
    from sphinx.util.docutils import SphinxDirective

    class ClassIndex(SphinxDirective):
        def run(self):
            return [nodes.container(classes=[PLACEHOLDER])]

    app.add_directive("class-index", ClassIndex)
    app.add_css_file("class-index.css")
    app.connect("doctree-read", _replace_placeholders)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
