from swizz.plots._registry import register_plot
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors as mcolors

@register_plot(
    name="general_bar_plot",
    description="General bar plot comparing two metrics (e.g., Reward and Goal) for each category with consistent colors.",
    args=[
        {"name": "data_dict", "type": "Dict[str, Dict[str, np.ndarray]]", "required": True,
         "description": "Each key is a category (e.g., 'No F Tz', 'F Tz') and maps to a dict with arrays for metrics."},
        {"name": "figsize", "type": "tuple", "required": False, "description": "Size of the figure. Default: (10, 6)."},
        {"name": "xlabel", "type": "str", "required": False, "description": "Label for the x-axis."},
        {"name": "ylabel", "type": "str", "required": False, "description": "Label for the y-axis."},
        {"name": "title", "type": "str", "required": False, "description": "Title for the plot."},
        {"name": "legend_loc", "type": "str", "required": False, "description": "Location for the legend. Default: 'upper left'."},
        {"name": "bar_width", "type": "float", "required": False, "description": "Width of the bars. Default: 0.25."},
        {"name": "color_map", "type": "Dict[str, str]", "required": False, "description": "Mapping of metrics to colors."},
        {"name": "style_map", "type": "Dict[str, str]", "required": False, "description": "Mapping of metrics to hatch styles."},
        {"name": "save", "type": "str", "required": False, "description": "Base filename to save PNG and PDF."},
    ],
    example_image="general_bar_plot.png",
    example_code="general_bar_plot.py",
)
def plot(
        data_dict,
        figsize=(12, 7),
        xlabel=None,
        ylabel="Value",
        title=None,
        legend_loc="upper right",
        bar_width=0.25,
        color_map=None,
        style_map=None,
        save=None,
        ax=None,
):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure  # Use the one passed by layout

    categories = list(data_dict.keys())
    indices = np.arange(len(categories))

    metrics = list(data_dict[next(iter(data_dict))].keys())

    if not color_map:
        # make all colors = None
        color_map = {metric: None for metric in metrics}

    if not style_map:
        style_map = {metric: '/' for metric in metrics}
        
    bar_positions_list=[]
    bar_containers = []
    for i, metric in enumerate(metrics):
        metric_values = [data[metric] for data in data_dict.values()]

        metric_color = color_map[metric]
        hatch = style_map.get(metric, '/')

        bar_positions = indices + (i - len(metrics) / 2) * bar_width
        bar_positions_list.append(bar_positions)
        bar_container = ax.bar(bar_positions, metric_values, bar_width,
                               label=metric, color=metric_color, linewidth=1, hatch=hatch)
        bar_containers.append(bar_container)

        for rect in bar_container:
            metric_dark=mcolors.to_rgba(rect.get_facecolor(), alpha=1.0)
            metric_dark=mcolors.to_hex([min(1, c * 0.6) for c in metric_dark[:3]])
            rect.set_edgecolor(metric_dark)
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2, height + 0.1, f'{height:.1f}', ha='center', va='bottom',
                    color=metric_dark, fontweight='bold', fontsize=12)

            ax.plot([rect.get_x() + rect.get_width() / 2, rect.get_x() + rect.get_width() / 2],
                    [height, height + 0.1], color=metric_dark, lw=1.5)

    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)

    bar_positions_list = np.array(bar_positions_list)
    center_indices = np.mean(bar_positions_list, axis=0)
    ax.set_xticks(center_indices)
    ax.set_xticklabels(categories)

    if legend_loc is not None:
        ax.legend(loc=legend_loc, ncol=len(metrics))
    ax.set_title(title)

    plt.tight_layout()

    if save:
        plt.savefig(f"{save}.png", dpi=300, bbox_inches="tight")
        plt.savefig(f"{save}.pdf", dpi=300, bbox_inches="tight")

    return fig, ax
