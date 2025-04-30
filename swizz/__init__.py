from swizz.plots.base import set_style
from swizz.plot import plot, available_plots
from swizz.table import table, available_tables
from swizz.layout import layout, available_layouts

# Set the default style to latex
set_style("latex")

__version__ = "0.1.1"
__author__ = "Lars Quaedvlieg"
__email__ = "larsquaedvlieg@outlook.com"

__all__ = ["set_style", "table", "plot", "layout", "available_layouts", "available_tables", "available_plots",
           "__version__", "__author__", "__email__"]