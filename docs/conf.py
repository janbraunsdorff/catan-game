import os
import sys
import traceback

import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath("../src"))


# -- Project ------------------------------------------------------------

project = "catan"
author = "Jan Braunsdorff"
year = "2023"
copyright = f"{year}, {author}"

try:
    from pkg_resources import get_distribution

    version = relase = get_distribution("catan").version
except:
    version = relase = "0.1.0"

# -- Genral configs -----------------------------------------------------
source_suffix = ".rst"
master_doc = "index"
pygments_style = "trac"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.ifconfig",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
]

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False

templates_path = ["."]

exclude_patterns = [
    ".pytest_cache",
    "dist/",
    "README.md",
    "_build",
    "Thumbs.db",
    ".DS_Store",
]


html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_use_smartypants = True
html_last_updated_fmt = "%b %d, %Y"
html_split_index = False
html_sidebars = {"**": ["searchbox.html", "globaltoc.html", "sourcelink.html"]}
html_short_title = "%s-%s" % (project, version)
