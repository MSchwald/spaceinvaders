from pathlib import Path
import sys

project_root = Path(__file__).parent.parent.parent.resolve()
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

project = 'Spaceinvaders'
copyright = '2025, Martin Schwald'
author = 'Martin Schwald'
release = '11.10.2025'

#autoapi_ignore = [str(p) + '/**' for p in project_root.iterdir() if p.is_dir() and p.name != 'docs'] + ['documentation.py','event.py','conf.py']
extensions = [
    'autoapi.extension',
    'sphinx.ext.autodoc',
    "sphinx.ext.autosummary",
    'sphinx.ext.napoleon'
]

autoapi_type = 'python'
autoapi_dirs = [str(src_path)]
autoapi_python_use_implicit_namespaces = True
autoapi_options = ['members', 'undoc-members', 'show-inheritance']
autoapi_add_toctree_entry = True
autoapi_root = 'autoapi'
autoapi_keep_files = True

autosummary_generate = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
autodoc_mock_imports = ["pygame"]

latex_engine = 'pdflatex'
latex_elements = {
    'classoptions': 'openany, oneside, nonumchapters',
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'sphinxsetup': 'hmargin=2cm, vmargin=2.5cm',
    'fontpkg': r'\usepackage{helvet}\renewcommand{\familydefault}{\sfdefault}',
    'preamble': r'''
\usepackage{titlesec}
\titleformat{\chapter}[hang]{\huge\bfseries}{\thechapter\ }{0pt}{\huge\bfseries}
\titlespacing*{\chapter}{0pt}{-20pt}{20pt}
'''
}

master_doc = 'modules'
language = 'en'

latex_documents = [
    (
        'modules',
        'spaceinvaders.tex',
        'Spaceinvaders Documentation',
        'Martin Schwald',
        'manual'
    )
]