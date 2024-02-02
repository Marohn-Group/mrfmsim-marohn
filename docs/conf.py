# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("../../mrfmsim_marohn"))
sys.path.insert(0, os.path.abspath("../../mrfmsim_marohn/experiment"))
sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "mrfmSim-marohn"
copyright = "2023 - 2024, Peter Sun, John A. Marohn"
author = "Peter Sun, John A. Marohn, Corinne Isaac, and others"
release = "0.2.0"


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "nbsphinx",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_static_path = []

# -- custom directive for rst -----------------------------------------------------

from docutils.parsers.rst import Directive
from docutils import nodes
import importlib


class CollectionDirective(Directive):
    """Discover all experiments in a collection and output their string representation."""

    has_content = True
    required_arguments = 1
    optional_arguments = 0

    def run(self):

        name_list = self.arguments[0].split(".")
        module = importlib.import_module(".".join(name_list[:-1]))
        module = getattr(module, name_list[-1])
        node_out = []
        for expt in module.experiments:
            child_node = nodes.literal_block(text=str(module[expt]))
            # create a indentation
            list_node = nodes.bullet_list(
                "", nodes.line(text=f"{name_list[-1]}['{expt}']"), child_node
            )

            node_out.append(list_node)

        return node_out


class ExperimentDirective(Directive):
    """Output experiment string representation."""

    has_content = True
    required_arguments = 1
    optional_arguments = 0

    def run(self):

        name_list = self.arguments[0].split(".")
        module = importlib.import_module(".".join(name_list[:-1]))
        module = getattr(module, name_list[-1])

        # create a indentation
        child_node = nodes.literal_block(text=str(module))
        list_node = nodes.bullet_list("", child_node)

        return [list_node]


def setup(app):
    app.add_directive("collection", CollectionDirective)
    app.add_directive("experiment", ExperimentDirective)
