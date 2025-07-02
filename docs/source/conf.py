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

source_suffix = ".rst"
master_doc = "index"

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_logo = "_static/gemini-logo-words.jpg"
html_title = "GPP Client"
github_url = "https://github.com/gemini-hlsw/gpp-client"
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#5F392A",
        "color-brand-content": "#5F392A",
        "color-brand-visited": "#3E251B",
    },
    "dark_css_variables": {
        "color-brand-primary": "#f2aa0d",
        "color-brand-content": "#f2aa0d",
        "color-brand-visited": "#ffc23e",
    },
    "announcement": "",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/gemini-hlsw/gpp-client",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
}
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
