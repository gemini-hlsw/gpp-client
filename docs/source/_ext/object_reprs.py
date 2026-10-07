"""
Hide attribute values that are only Python's default object repr.

A field builder's leaf fields render as ``= <...GraphQLField object>``, which
tells the reader nothing and wraps over several lines on a phone. autodoc's
``no-value`` option can't be set on ``automodule``, so the build drops these
values from the rendered signatures instead.
"""

import re

OBJECT_REPR_VALUE = re.compile(r"^\s*=\s*<[\w.]+ object( at 0x[0-9a-f]+)?>$")


def is_object_repr_value(text: str) -> bool:
    """
    Tell whether a signature annotation is an ``= <... object>`` value.

    Parameters
    ----------
    text : str
        The annotation's text, such as ``" = <Foo object>"``.

    Returns
    -------
    bool
        ``True`` when the value is a default object repr.
    """
    return bool(OBJECT_REPR_VALUE.match(text))


def _hide_object_reprs(app, doctree) -> None:
    from sphinx import addnodes

    for desc in doctree.findall(addnodes.desc):
        if desc.get("domain") != "py" or desc.get("objtype") not in {
            "attribute",
            "data",
        }:
            continue
        for signature in desc.findall(addnodes.desc_signature):
            for annotation in list(signature.findall(addnodes.desc_annotation)):
                if is_object_repr_value(annotation.astext()):
                    annotation.parent.remove(annotation)


def setup(app):
    app.connect("doctree-read", _hide_object_reprs)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
