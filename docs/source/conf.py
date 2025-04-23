# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# https://eikonomega.medium.com/getting-started-with-sphinx-autodoc-part-1-2cebbbca5365

import os
import sys

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
    if name in {"queries", "default_fields", "resource_id_field"}:
        return True  # skip this member
    return skip


def setup(app):
    app.connect("autodoc-skip-member", skip_member)
