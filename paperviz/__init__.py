from paperviz.plots.base import set_style
from paperviz.plot import plot, available_plots
from paperviz.table import table, available_tables

# from .layout import layout

# Set the default style to latex
set_style("latex")

__all__ = ["set_style", "table", "plot", "available_tables", "available_plots"]
