# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# https://eikonomega.medium.com/getting-started-with-sphinx-autodoc-part-1-2cebbbca5365

import os
import sys
from enum import Enum

sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "gpp_client"
copyright = "2025, NOIRLab"
author = "NOIRLab"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinxcontrib.typer",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_logo = "_static/gemini-logo-words.jpg"
html_title = "GPP Client"
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}


def skip_member(app, what, name, obj, skip, options):
    if name in {}:
        return True  # skip this member
    return skip


def suppress_enum_docstring(app, what, name, obj, options, lines):
    """Remove the default 'An enumeration.' docstring from Enum classes."""
    if what == "class" and isinstance(obj, type) and issubclass(obj, Enum):
        if lines and lines[0].strip() == "An enumeration.":
            lines.clear()


def setup(app):
    app.connect("autodoc-skip-member", skip_member)
    app.connect("autodoc-process-docstring", suppress_enum_docstring)
