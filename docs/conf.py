# Configuration minimale pour Sphinx

project = 'Pinpin'
author = 'David Delaunay'
release = '1.1.4'

extensions = [
    'sphinx.ext.autodoc',    # Pour générer automatiquement la documentation des docstrings
    'sphinx.ext.napoleon',   # Pour le support des docstrings NumPy et Google style
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']
