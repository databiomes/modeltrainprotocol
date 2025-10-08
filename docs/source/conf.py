# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import tomllib

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('../../'))

# Read version from pyproject.toml
def get_version() -> str:
    pyproject_path = os.path.join(os.path.dirname(__file__), '..', '..', 'pyproject.toml')
    with open(pyproject_path, 'rb') as f:
        pyproject_data = tomllib.load(f)
    return pyproject_data['project']['version']

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Model Training Protocol'
copyright = '2025, Databiomes Inc.'
author = 'Databiomes Inc.'

# Get version from pyproject.toml
version = f"v{get_version()}"
release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.githubpages',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']

# PyData Sphinx Theme options
html_theme_options = {
    "navbar_align": "left",
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/databiomes/mikoshi",
            "icon": "fab fa-github-square",
        },
    ],
    "show_toc_level": 1,
    "navbar_end": ["navbar-icon-links", "theme-switcher"],
}

# HTML context for edit page button
html_context = {
    "github_user": "databiomes",
    "github_repo": "mikoshi",
    "github_version": "main",
    "doc_path": "docs/source",
}

# -- Extension configuration -------------------------------------------------

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}
