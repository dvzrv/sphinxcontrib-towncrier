# pylint: disable=invalid-name
# Ref: https://www.sphinx-doc.org/en/master/usage/configuration.html
"""Configuration for the Sphinx documentation generator."""

import sys
from functools import partial
from pathlib import Path
from typing import Mapping

from sphinx.application import Sphinx

from setuptools_scm import get_version


# -- Path setup --------------------------------------------------------------

PROJECT_ROOT_DIR = Path(__file__).parents[1].resolve()
PROJECT_SRC_DIR = PROJECT_ROOT_DIR / 'src'
get_scm_version = partial(get_version, root=PROJECT_ROOT_DIR)

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.


sys.path.insert(0, str(PROJECT_SRC_DIR))


# -- Project information -----------------------------------------------------

github_url = 'https://github.com'
github_repo_org = 'sphinx-contrib'
github_repo_name = 'sphinxcontrib-towncrier'
github_repo_slug = f'{github_repo_org}/{github_repo_name}'
github_repo_url = f'{github_url}/{github_repo_slug}'
github_sponsors_url = f'{github_url}/sponsors'

project = github_repo_name
author = 'Sviatoslav Sydorenko'
copyright = f'2021, {author}'  # pylint: disable=redefined-builtin

# The short X.Y version
version = '.'.join(
    get_scm_version(
        local_scheme='no-local-version',
    ).split('.')[:3],
)

# The full version, including alpha/beta/rc tags
release = get_scm_version()

rst_epilog = f"""
.. |project| replace:: {project}
"""


# -- General configuration ---------------------------------------------------

extensions = [
    # Built-in extensions:
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel',  # autocreate section targets for refs
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',

    # Third-party extensions:
    'myst_parser',  # extended markdown; https://pypi.org/project/myst-parser/
    'sphinxcontrib.apidoc',

    # Tree-local extensions:
    'sphinxcontrib.towncrier.ext',  # provides `.. towncrier-draft-entries::`
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_build', 'Thumbs.db', '.DS_Store',  # <- Defaults
    'changelog-fragments/**',  # Towncrier-managed change notes
]


# -- Options for HTML output -------------------------------------------------

html_theme = 'furo'

html_show_sphinx = True


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'rtd': ('https://docs.rtfd.io/en/stable', None),
    'setuptools': ('https://setuptools.rtfd.io/en/latest', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master', None),
}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Options for sphinxcontrib.apidoc extension ------------------------------

apidoc_excluded_paths = []
apidoc_extra_args = [
    '--implicit-namespaces',
    '--private',  # include “_private” modules
]
apidoc_module_dir = str(PROJECT_SRC_DIR / 'sphinxcontrib')
apidoc_module_first = False
apidoc_output_dir = 'pkg'
apidoc_separate_modules = True
apidoc_toc_file = None

# -- Options for extlinks extension ------------------------------------------

extlinks = {
    'issue': (f'{github_repo_url}/issues/%s', '#%s'),  # noqa: WPS323
    'pr': (f'{github_repo_url}/pull/%s', 'PR #%s'),  # noqa: WPS323
    'commit': (f'{github_repo_url}/commit/%s', '%s'),  # noqa: WPS323
    'gh': (f'{github_url}/%s', 'GitHub: %s'),  # noqa: WPS323
    'user': (f'{github_sponsors_url}/%s', '@%s'),  # noqa: WPS323
}

# -- Options for linkcheck builder -------------------------------------------

linkcheck_ignore = [
    r'http://localhost:\d+/',  # local URLs
]
linkcheck_workers = 25

# Ref:
# * https://github.com/djungelorm/sphinx-tabs/issues/26#issuecomment-422160463
sphinx_tabs_valid_builders = ['linkcheck']  # prevent linkcheck warning

# -- Options for autosectionlabel extension ----------------------------------

# Ref:
# * https://www.sphinx-doc.org/en/master/usage/extensions/autosectionlabel.html
autosectionlabel_maxdepth = 2  # mitigate Towncrier nested subtitles collision

# -- Options for towncrier_draft extension -----------------------------------

# mode is one of 'draft', 'sphinx-version' or 'sphinx-release'
towncrier_draft_autoversion_mode = 'draft'
towncrier_draft_include_empty = True
towncrier_draft_working_directory = PROJECT_ROOT_DIR
# Not yet supported:
towncrier_draft_config_path = 'pyproject.toml'  # relative to cwd

# -- Strict mode -------------------------------------------------------------

# Ref: python-attrs/attrs#571
default_role = 'any'

nitpicky = True
_py_class_role = 'py:class'
nitpick_ignore = [
    # NOTE: Docutils does not have any intersphinx-compatible site
    (_py_class_role, 'docutils.nodes.Node'),
    (_py_class_role, 'docutils.nodes.document'),
    (_py_class_role, 'docutils.statemachine.State'),
    (_py_class_role, 'docutils.nodes.Node'),
]


def setup(app: Sphinx) -> Mapping[str, str]:
    """Set up extra Sphinx extension integrations."""
    # NOTE: Sphinx doesn't seem to expose its :event: role at the moment.
    # NOTE: This hack redeclares the event type locally.
    # Ref: https://github.com/sphinx-doc/sphinx/issues/8987
    app.add_object_type('event', 'event')

    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
        'version': 'builtin',
    }
