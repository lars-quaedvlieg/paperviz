from swizz.plots._registry import register_plot
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from swizz.utils.plot import apply_legend


@register_plot(
    name="multiple_std_lines",
    description="Line plot with shaded confidence intervals and configurable label, color, and linestyle mappings.",
    args=[
        {"name": "data_dict", "type": "Dict[str, Dict[str, np.ndarray]]", "required": True,
         "description": "Each key is a run, and maps to a dict with arrays for x, y, and stderr."},
        {"name": "x_key", "type": "str", "required": False,
         "description": "Key in inner dict to use for x-axis. Default: 'round_num'."},
        {"name": "y_key", "type": "str", "required": False,
         "description": "Key in inner dict to use for y-axis. Default: 'unique_scores'."},
        {"name": "yerr_key", "type": "str", "required": False,
         "description": "Key in inner dict for standard error values. Default: 'std_error'."},
        {"name": "figsize", "type": "tuple", "required": False,
         "description": "The size of your figure. Default: (8, 5)."},
        {"name": "legend_loc", "type": "str", "required": False,
         "description": "The location of the legend. Default: 'upper left'."},
        {"name": "label_map", "type": "Dict[str, str]", "required": False,
         "description": "Mapping of internal label to display name."},
        {"name": "color_map", "type": "Dict[str, str]", "required": False,
         "description": "Mapping of label → color hex string."},
        {"name": "style_map", "type": "Dict[str, str]", "required": False,
         "description": "Mapping of label → line style."},
        {"name": "xlim", "type": "Tuple[float, float]", "required": False, "description": "X-axis limits."},
        {"name": "ylim", "type": "Tuple[float, float]", "required": False, "description": "Y-axis limits."},
        {"name": "xlabel", "type": "str", "required": False, "description": "X-axis label."},
        {"name": "ylabel", "type": "str", "required": False, "description": "Y-axis label."},
        {"name": "x_formatter", "type": "Callable", "required": False,
         "description": "Formatter function for x-ticks."},
        {"name": "y_formatter", "type": "Callable", "required": False,
         "description": "Formatter function for y-ticks."},
        {"name": "save", "type": "str", "required": False, "description": "Base filename to save PNG and PDF."},
        # {"name": "include_latex", "type": "bool", "required": False, "description": "Generate LaTeX \\includegraphics snippet for figure."}
    ],
    example_image="multiple_std_lines.png",
    example_code="multiple_std_lines.py",
)
def plot(
        data_dict,
        x_key="round_num",
        y_key="unique_scores",
        yerr_key="std_error",
        figsize=(8, 5),
        legend_loc="upper left",
        label_map=None,
        color_map=None,
        style_map=None,
        xlim=None,
        ylim=None,
        xlabel=None,
        ylabel=None,
        x_formatter=None,
        y_formatter=None,
        save=None,
        ax=None,
):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure  # Use the one passed by layout

    for label, data in data_dict.items():
        display_name = label_map.get(label, label) if label_map else label
        color = color_map.get(label, None) if color_map else None
        linestyle = style_map.get(label, "solid") if style_map else "solid"

        x = data[x_key]
        y = data[y_key]
        yerr = data[yerr_key]

        line, = ax.plot(x, y, label=display_name, color=color, linestyle=linestyle)
        fill_color = color if color is not None else line.get_color()
        ax.fill_between(x, y - yerr, y + yerr, color=fill_color, alpha=0.2)

    if legend_loc:
        ax.legend(loc=legend_loc)

    # Formatters
    if x_formatter:
        ax.xaxis.set_major_formatter(mtick.FuncFormatter(x_formatter))
    if y_formatter:
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(y_formatter))

    # Axes, labels, limits
    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
    if xlim: ax.set_xlim(xlim)
    if ylim: ax.set_ylim(ylim)

    if save:
        plt.savefig(f"{save}.png", dpi=300, bbox_inches="tight")
        plt.savefig(f"{save}.pdf", dpi=300, bbox_inches="tight")

    return fig, ax
