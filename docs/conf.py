#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Inferring space from sensorimotor dependencies documentation build configuration file, created by
# sphinx-quickstart on Sat Jun  9 07:30:01 2018.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('./..'))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
#sys.path[0:0] = [os.path.abspath('_themes/foundation-sphinx-theme')]
#'foundation_sphinx_theme'
extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Inferring Space from Sensorimotor Dependencies'
copyright = '2018, Kexin Ren & Younesse Kaddar'
author = 'Kexin Ren & Younesse Kaddar'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '0.0.1'
# The full version, including alpha/beta/rc tags.
release = '0.0.1'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_materialdesign_theme'

# Html logo in drawer.
# Fit in the drawer at the width of image is 240 px.
html_logo = '_static/logo_project.png'


# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#

html_theme_options = {
    # Specify a list of menu in Header.
    # Tuples forms:
    #  ('Name', 'external url or path of pages in the document', boolean, 'icon name')
    #
    # Third argument:
    # True indicates an external link.
    # False indicates path of pages in the document.
    #
    # Fourth argument:
    # Specify the icon name.
    # For details see link.
    # https://material.io/icons/
    'header_links' : [
        ('Home', 'index', False, 'home'),
        ("ExternalLink", "http://younesse.net", True, 'launch'),
        ("GitHub", "https://github.com/youqad/Neurorobotics_Project", True, 'link')
    ],

    # Customize css colors.
    # For details see link.
    # https://getmdl.io/customize/index.html
    #
    # Values: amber, blue, brown, cyan deep_orange, deep_purple, green, grey, indigo, light_blue,
    #         light_green, lime, orange, pink, purple, red, teal, yellow(Default: indigo)
    'primary_color': 'cyan',
    # Values: Same as primary_color. (Default: pink)
    'accent_color': 'orange',

    # Customize layout.
    # For details see link.
    # https://getmdl.io/components/index.html#layout-section
    'fixed_drawer': False,
    'fixed_header': False,
    'header_waterfall': False,
    'header_scroll': True,

    # Render title in header.
    # Values: True, False (Default: False)
    'show_header_title': True,
    # Render title in drawer.
    # Values: True, False (Default: True)
    'show_drawer_title': False,
    # Render footer.
    # Values: True, False (Default: True)
    'show_footer': True
}


# html_theme_options = {
#         'motto': 'Neurobotics Cogmaster project at the Ecole Normale Supérieure / Univ. Paris Descartes',

#         # Your stylesheet relative to the _static dir.
#         # Default is 'foundation/css/basic.css'
#         'stylesheet': 'foundation/css/cards.css',

#         # Logo image in SVG format. If the browser doesn't support SVG
#         # It will try to load JPG with the same name.
#         'logo_screen': 'http://younesse.net/images/Neurorobotics/logo_project.svg',

#         # Logo for small screens. If ommited, logo_screen will be used.
#         'logo_mobile': '',

#         # Path to your favicon.ico file relative to the _static dir.
#         'favicon': '',

#         # Use this if the top-level items of the toctree don't fit in the top-bar navigation.
#         # If True, the whole toctree will be placed inside a single top-level item.
#         'top_bar_force_fit': False,

#         # The title of the aformentioned top-level item. Default is "Sections"
#         #'top_bar_content_title': 'Sections',

#         # If set, Google Analytics code will be appended to body of each page.
#         #'google_analytics_id': 'your-google-analytics-id',

#         # The "og:title", "og:type", "og:url", "og:site_name" and "og:description" Open Graph tags
#         # will be generated automatically, but you should specify the
#         # path to the image that you want to be used
#         # in the required "og:image" property relative to the _static dir.
#         #'opengraph_image': 'path/to/your/opengraph-image.jpg',

#         # Any custom additional OG tags
#         #'opengraph_tags': {
#         #        'foo': 'bar', # will be rendered as <meta property="og:foo" content="bar" />
#         #},

#         # The "description" meta tag will be created automatically, but
#         # you can specify additional meta tags here.
#         #'meta_tags': {
#         #        'foo': 'bar', # will be rendered as <meta name="foo" content="bar">
#         #},

#         # The value for "description" and "og:description" metatags.
#         # If omitted, the value of "motto" will be used.
#         'seo_description': 'Kexin Ren & Younesse Kaddar\'s neurorobotics project at ENS Ulm/Uni. Paris Decartes on inferring space from sensorimotor dependencies',

#         # Use this as the base for Open Graph URLs without trailing slash.
#         #'base_url': 'http://example.com',

#         # If true a bar with Facebook, Google+ and Twitter social buttons will be displayed
#         # underneath the header.
#         'social_buttons': True,

#         # ID of your Facebook app associated with the Facebook Like button.
#         #'facebook_app_id': '123456789',

#         # A Twitter ID used for the via mention of the Twitter button.
#         #'twitter_id': 'FoundationSphinx',

#         # Flattr button settings.
#         #'flattr_id': 'andypipkin', # Your Flattr ID
#         #'flattr_title': '', # If missing docstitle or title will be used.
#         #'flattr_description': '', # If missing seo_description or motto will be used.
#         #'flattr_tags': '', # Optional.


#         # If "author" and "copyright_year" are set they will override the "copyright" setting.

#         # Author's name.
#         'author': 'Kexin Ren & Younesse Kaddar',

#         # Author's link.
#         'author_link': 'http://younesse.net',

#         # Year to be used in the copyright statement.
#         'copyright_year': '2018',

#         # Author's Google+ id. If set a G+ authorship link will be added.
#         #'google_plus_id': '117034840853387702598',


#         # Fork me on GitHub ribbon will be displayed if "github_user", "github_repo" and "github_ribbon_image" are set:
#         # https://github.com/blog/273-github-ribbons
#         # Ribbons are hidden on small screens!

#         # Your GitHub ID.
#         'github_user': 'youqad',

#         # The repository slug.
#         'github_repo': 'Neurorobotics_Project',

#         # Path to the ribbon image relative to the "_static" directory.
#         #'github_ribbon_image': 'my-github-ribbon.png',

#         # Position of the ribbon "left" or "right".
#         'github_ribbon_position': 'right',
# }
# html_theme_path = foundation_sphinx_theme.HTML_THEME_PATH

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']


# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
        'donate.html',
    ]
}


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'Inferringspacefromsensorimotordependenciesdoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'Inferringspacefromsensorimotordependencies.tex', 'Inferring space from sensorimotor dependencies Documentation',
     'Kexin Ren \\& Younesse Kaddar', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'inferringspacefromsensorimotordependencies', 'Inferring space from sensorimotor dependencies Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'Inferringspacefromsensorimotordependencies', 'Inferring space from sensorimotor dependencies Documentation',
     author, 'Inferringspacefromsensorimotordependencies', 'One line description of project.',
     'Miscellaneous'),
]



