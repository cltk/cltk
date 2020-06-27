# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

from datetime import datetime
import pkg_resources
import os
import sys

# this path required for local build, to find ``pyproject.toml``
sys.path.insert(0, os.path.abspath(".."))
# this required for RTD build to find source
sys.path.insert(0, os.path.abspath("../src/cltkv1"))


# -- Project information -----------------------------------------------------

project = "The Classical Language Toolkit"
today = datetime.today()
curr_year = today.year
copyright = f'2019-{curr_year}, "Kyle P. Johnson <kyle@kyle-p-johnson.com>"'
author = '"Kyle P. Johnson <kyle@kyle-p-johnson.com>"'
# The full version, including alpha/beta/rc tags
curr_version = pkg_resources.get_distribution("cltkv1")
release = curr_version.version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
#
# TODO: Decide which of these are necessary, if others needed
#
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",  # Must come *after* sphinx.ext.napoleon.
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.extlinks",
    "sphinx.ext.ifconfig",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
]


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML op_output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]
