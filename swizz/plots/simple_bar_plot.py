from swizz.plots._registry import register_plot
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import colors as mcolors

@register_plot(
    name="general_bar_plot",
    description="General bar plot comparing multiple metrics for each category with consistent colors and hatching.",
    args=[
        {"name": "df", "type": "pd.DataFrame", "required": True,
         "description": "DataFrame containing the category column and one or more metric columns."},
        {"name": "category_column", "type": "str", "required": True,
         "description": "Column name for the x-axis categories (e.g., 'Group', 'Condition')."},
        {"name": "figsize", "type": "tuple", "required": False, "description": "Figure size. Default: (12, 7)."},
        {"name": "xlabel", "type": "str", "required": False, "description": "Label for x-axis."},
        {"name": "ylabel", "type": "str", "required": False, "description": "Label for y-axis."},
        {"name": "title", "type": "str", "required": False, "description": "Title of the plot."},
        {"name": "legend_loc", "type": "str", "required": False, "description": "Legend location. Default: 'upper right'."},
        {"name": "bar_width", "type": "float", "required": False, "description": "Width of bars. Default: 0.25."},
        {"name": "color_map", "type": "Dict[str, str]", "required": False, "description": "Map from metric name to color."},
        {"name": "style_map", "type": "Dict[str, str]", "required": False, "description": "Map from metric name to hatch style."},
        {"name": "save", "type": "str", "required": False, "description": "Base filename to save PNG and PDF."},
    ],
    example_image="general_bar_plot.png",
    example_code="general_bar_plot.py",
)
def plot(
    df,
    category_column,
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
        fig = ax.figure

    # Ensure DataFrame and extract data
    if not isinstance(df, pd.DataFrame):
        raise TypeError("`df` must be a pandas DataFrame.")

    if category_column not in df.columns:
        raise ValueError(f"`category_column` '{category_column}' not found in DataFrame.")

    categories = df[category_column].tolist()
    metric_columns = [col for col in df.columns if col != category_column]
    indices = np.arange(len(categories))

    if not color_map:
        color_map = {metric: None for metric in metric_columns}

    if not style_map:
        style_map = {metric: '/' for metric in metric_columns}

    bar_positions_list = []
    bar_containers = []

    for i, metric in enumerate(metric_columns):
        metric_values = df[metric].values
        metric_color = color_map.get(metric, None)
        hatch = style_map.get(metric, '/')

        bar_positions = indices + (i - len(metric_columns) / 2) * bar_width
        bar_positions_list.append(bar_positions)

        bar_container = ax.bar(bar_positions, metric_values, bar_width,
                               label=metric, color=metric_color, linewidth=1, hatch=hatch)
        bar_containers.append(bar_container)

        for rect in bar_container:
            metric_dark = mcolors.to_rgba(rect.get_facecolor(), alpha=1.0)
            metric_dark = mcolors.to_hex([min(1, c * 0.6) for c in metric_dark[:3]])
            rect.set_edgecolor(metric_dark)
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2, height + 0.1, f'{height:.1f}',
                    ha='center', va='bottom', color=metric_dark, fontweight='bold', fontsize=12)

            ax.plot([rect.get_x() + rect.get_width() / 2, rect.get_x() + rect.get_width() / 2],
                    [height, height + 0.1], color=metric_dark, lw=1.5)

    # Axis labels and ticks
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel if xlabel else category_column)

    bar_positions_list = np.array(bar_positions_list)
    center_indices = np.mean(bar_positions_list, axis=0)
    ax.set_xticks(center_indices)
    ax.set_xticklabels(categories)

    if legend_loc:
        ax.legend(loc=legend_loc, ncol=len(metric_columns))

    ax.set_title(title)
    plt.tight_layout()

    if save:
        print(f"Saving plot to {save}.png and {save}.pdf")
        plt.savefig(f"{save}.png", dpi=300, bbox_inches="tight")
        plt.savefig(f"{save}.pdf", dpi=300, bbox_inches="tight")

    return fig, ax
