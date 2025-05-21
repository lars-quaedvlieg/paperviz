import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from swizz.plots._registry import register_plot
from swizz.utils.plot import apply_legend

@register_plot(
    name="multiple_std_lines_df",
    description=(
        "Line plot with shaded confidence intervals and configurable label, color, "
        "and linestyle mappings, using a pandas DataFrame in long format."
    ),
    args=[
        {"name": "data_df", "type": "pd.DataFrame", "required": True,
         "description": (
             "Long-form DataFrame containing one row per point with columns for the run label, "
             "x values, y values, and standard error."
         )},
        {"name": "label_key", "type": "str", "required": True,
         "description": "Column name in data_df that identifies each run/series."},
        {"name": "x_key", "type": "str", "required": False,
         "description": "Column name for x-axis values. Default: 'round_num'."},
        {"name": "y_key", "type": "str", "required": False,
         "description": "Column name for y-axis values. Default: 'unique_scores'."},
        {"name": "yerr_key", "type": "str", "required": False,
         "description": "Column name for standard error. Default: 'std_error'."},
        {"name": "figsize", "type": "tuple", "required": False,
         "description": "Figure size. Default: (8, 5)."},
        {"name": "legend_loc", "type": "str", "required": False,
         "description": "Legend location. Default: 'upper left'."},
        {"name": "label_map", "type": "Dict[str, str]", "required": False,
         "description": "Mapping of raw labels to display names."},
        {"name": "color_map", "type": "Dict[str, str]", "required": False,
         "description": "Mapping of raw labels to line colors."},
        {"name": "style_map", "type": "Dict[str, str]", "required": False,
         "description": "Mapping of raw labels to line styles."},
        {"name": "xlim", "type": "Tuple[float, float]", "required": False,
         "description": "X-axis limits."},
        {"name": "ylim", "type": "Tuple[float, float]", "required": False,
         "description": "Y-axis limits."},
        {"name": "xlabel", "type": "str", "required": False,
         "description": "X-axis label."},
        {"name": "ylabel", "type": "str", "required": False,
         "description": "Y-axis label."},
        {"name": "x_formatter", "type": "Callable", "required": False,
         "description": "Formatter for x-axis ticks."},
        {"name": "y_formatter", "type": "Callable", "required": False,
         "description": "Formatter for y-axis ticks."},
        {"name": "save", "type": "str", "required": False,
         "description": "Base filename to save PNG and PDF."},
    ],
    example_code="multiple_std_lines_df_example.py",
)
def plot(
    data_df: pd.DataFrame,
    label_key: str,
    x_key: str = "round_num",
    y_key: str = "unique_scores",
    yerr_key: str = "std_error",
    figsize: tuple = (8, 5),
    legend_loc: str = "upper left",
    label_map: dict = None,
    color_map: dict = None,
    style_map: dict = None,
    xlim: tuple = None,
    ylim: tuple = None,
    xlabel: str = None,
    ylabel: str = None,
    x_formatter=None,
    y_formatter=None,
    save: str = None,
    ax=None,
):
    # Prepare figure and axis
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    # Group and plot each series
    for label, group in data_df.groupby(label_key):
        display_name = label_map.get(label, label) if label_map else label
        color = color_map.get(label) if color_map else None
        linestyle = style_map.get(label, "solid") if style_map else "solid"

        x = group[x_key].values
        y = group[y_key].values
        yerr = group[yerr_key].values

        line, = ax.plot(x, y, label=display_name, color=color, linestyle=linestyle)
        fill_color = color if color is not None else line.get_color()
        ax.fill_between(x, y - yerr, y + yerr, color=fill_color, alpha=0.2)

    # Legend and formatting
    if legend_loc:
        ax.legend(loc=legend_loc)
    if x_formatter:
        ax.xaxis.set_major_formatter(mtick.FuncFormatter(x_formatter))
    if y_formatter:
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(y_formatter))

    # Axis labels and limits
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)

    # Save if requested
    if save:
        fig.savefig(f"{save}.png", dpi=300, bbox_inches="tight")
        fig.savefig(f"{save}.pdf", dpi=300, bbox_inches="tight")

    return fig, ax