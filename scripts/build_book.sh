rm -rf docs/tables
rm docs/_toc.yml
PYTHONPATH=. python scripts/generate_table_docs.py
PYTHONPATH=. python scripts/generate_plots_docs.py
PYTHONPATH=. python scripts/generate_table_gallery.py
PYTHONPATH=. python scripts/generate_plots_gallery.py
PYTHONPATH=. python scripts/generate_plot_theme_gallery.py
PYTHONPATH=. python scripts/generate_toc.py
jupyter-book build docs