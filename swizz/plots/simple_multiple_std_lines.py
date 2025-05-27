import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.cm as cm

from swizz.plots._registry import register_plot

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
        {"name": "legend_title", "type": "str", "required": False,
         "description": "Legend title. Default: None."},
        {"name": "legend_ncol", "type": "int", "required": False,
         "description": "Number of columns in legend. Default: 1."},
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
    example_image="multiple_std_lines_df.png",
    example_code="multiple_std_lines_df.py",
)
def plot(
    data_df: pd.DataFrame,
    label_key: str,
    x_key: str = "round_num",
    y_key: str = "unique_scores",
    yerr_key: str = "std_error",
    figsize: tuple = (8, 5),
    legend_loc: str = "upper left",
    legend_title: str = None,
    legend_ncol: int = 1,
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

    try:
        data_df[label_key] = data_df[label_key].astype(int)
    except:
        try:
            data_df[label_key] = data_df[label_key].astype(float)
        except:
            pass

    if color_map is None:
        positions = np.linspace(0, 1, len(data_df[label_key].unique()))
        cmap = cm.get_cmap("viridis")
        color_map = {key: cmap(pos) for key, pos in zip(data_df[label_key].unique(), positions)}

    # Group and plot each series
    for label, group in sorted(data_df.groupby(label_key), key=lambda x: x[0]):
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
        ax.legend(loc=legend_loc, title=legend_title, ncol=legend_ncol)
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