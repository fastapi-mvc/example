# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
from fastapi_mvc_example import __version__
from pallets_sphinx_themes import ProjectLink

# Project --------------------------------------------------------------

project = "fastapi-mvc-example"
copyright = "2022, Radosław Szamszur"
author = "Radosław Szamszur"
release = __version__

# General --------------------------------------------------------------

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "pallets_sphinx_themes",
    "myst_parser",
]

autodoc_typehints = "description"
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "click": ("https://click.palletsprojects.com/en/8.1.x/", None),
}
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = True
napoleon_attr_annotations = True


templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# HTML -----------------------------------------------------------------

html_theme = "click"
html_context = {
    "project_links": [
        ProjectLink("Source Code", "https://github.com/rszamszur/fastapi-mvc-example"),
    ]
}
html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html"],
}
singlehtml_sidebars = {"index": ["project.html", "localtoc.html"]}
html_logo = "_static/logo.png"
html_title = f"fastapi-mvc-example Documentation ({__version__})"
html_show_sourcelink = False
html_static_path = ["_static"]