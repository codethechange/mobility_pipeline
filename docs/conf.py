# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../mobility_pipeline'))


# -- Project information -----------------------------------------------------

project = 'UNICEF Mobility Pipeline'
copyright = '2019 Members of the 2018-2019 Stanford Code the Change UNICEF Team'
author = 'Stanford Code the Change (http://codethechange.stanford.edu)'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the “master” document that contains the root toctree directive
master_doc = 'index'

# Mappings to external documentation with intersphinx
# The numpy and matplotlib URLs came from Brian Skinn's gist here:
# https://gist.github.com/bskinn/0e164963428d4b51017cebdb6cda5209 for
intersphinx_mapping = {'shapely': ('https://shapely.readthedocs.io/en/latest/',
                                   None),
                       'numpy': ('https://docs.scipy.org/doc/numpy/', None),
                       'matplotlib': ('https://matplotlib.org', None),
                       'pandas': (
                           'https://pandas.pydata.org/pandas-docs/stable/',
                           None)
                       }


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
