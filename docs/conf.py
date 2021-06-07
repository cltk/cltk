# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
from datetime import datetime
from typing import Dict, List, Union

import pkg_resources

# errors on rtd build
from cltk.nlp import iso_to_pipeline

# this path required for local build, to find ``pyproject.toml``
sys.path.insert(0, os.path.abspath(".."))
# this required for RTD build to find source
sys.path.insert(0, os.path.abspath("../src"))
sys.path.insert(0, os.path.abspath("../src/cltk"))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = "The Classical Language Toolkit"
dt_today: datetime = datetime.today()
curr_year: int = dt_today.year
copyright = f" 2014-{curr_year} Kyle P. Johnson"
# author = "Kyle P. Johnson et al."
# the following errors on rtd server
# cltk_project = cltk.get_pyproject()  # Dict[str,Union[str, List[str], Dict[str,str]]]
# author_list: List[str] = cltk_project["authors"]
# author = ", ".join(author_list)
# The full version, including alpha/beta/rc tags
curr_version: pkg_resources.EggInfoDistribution = pkg_resources.get_distribution("cltk")
release: str = curr_version.version


langs_available_pipelines: List[str] = [
    val.language.name for _, val in iso_to_pipeline.items()
]
langs_available_pipelines_len = len(langs_available_pipelines)
langs_available_pipelines_alpha = sorted(langs_available_pipelines)
langs_available_pipelines_str = "- " + "\n- ".join(langs_available_pipelines_alpha)


# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-rst_epilog
rst_epilog = f"""
.. |PipelinesListLen| replace:: {langs_available_pipelines_len}
"""


# -- General configuration ---------------------------------------------------

html_show_copyright = True  # default is True
# html_show_sphinx = False

# https://alabaster.readthedocs.io/en/latest/customization.html#header-footer-options
html_theme_options = {
    # 'logo': 'logo.png',
    "logo_name": False,
    "show_powered_by": False,
    # "show_relbars": True,
}

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
#
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",  # Must come *after* sphinx.ext.napoleon. https://pypi.org/project/sphinx-autodoc-typehints/
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.graphviz",  # https://www.sphinx-doc.org/en/master/usage/extensions/graphviz.html#module-sphinx.ext.graphviz
    # "sphinx.ext.doctest",
    # "sphinx.ext.duration",  # use when builds seem slow
]

# sphinx.ext.autodoc
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
autodoc_member_order = (
    "bysource"  # to sort according to order in code, not alaphabetical
)

# sphinx.ext.todo
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html
todo_include_todos = True

# sphinx.ext.napoleon
# Napolean for Google-style docstrings
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#type-annotations
'''
def func(arg1: int, arg2: str) -> bool:
    """Summary line.

    Extended description of function.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    """
    return True
'''
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#docstring-sections
napoleon_include_private_with_doc = True


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "modules.rst"]


# -- Options for HTML op_output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# https://alabaster.readthedocs.io/en/latest/customization.html
html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]  # Note: This doesn't help find the favicon
html_favicon = "_static/favicon-32x32.png"  # Note: Full path required here
# https://alabaster.readthedocs.io/en/latest/installation.html
