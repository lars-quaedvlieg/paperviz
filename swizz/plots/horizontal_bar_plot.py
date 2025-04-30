from swizz.plots._registry import register_plot
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors as mcolors

@register_plot(
    name="general_horizontal_bar_plot",
    description=(
        "General horizontal bar plot comparing two (or more) metrics "
        "for each category with consistent colors and hatches."
    ),
    args=[
        {"name": "data_dict", "type": "Dict[str, Dict[str, float]]", "required": True,
         "description": "Each key is a category and maps to a dict of metric→value."},
        {"name": "figsize", "type": "tuple", "required": False,
         "description": "Size of the figure. Default: (10, 6)."},
        {"name": "xlabel", "type": "str", "required": False,
         "description": "Label for the x-axis."},
        {"name": "ylabel", "type": "str", "required": False,
         "description": "Label for the y-axis."},
        {"name": "title", "type": "str", "required": False,
         "description": "Title for the plot."},
        {"name": "legend_loc", "type": "str", "required": False,
         "description": "Location for the legend. Default: 'upper right'."},
        {"name": "bar_height", "type": "float", "required": False,
         "description": "Height of the bars. Default: 0.25."},
        {"name": "color_map", "type": "Dict[str, str]", "required": False,
         "description": "Mapping of metrics to colors."},
        {"name": "style_map", "type": "Dict[str, str]", "required": False,
         "description": "Mapping of metrics to hatch styles."},
        {"name": "save", "type": "str", "required": False,
         "description": "Base filename to save PNG and PDF."},
    ],
    example_image="general_barh_plot.png",
    example_code="general_barh_plot.py",
)
def plot(
    data_dict,
    figsize=(12, 7),
    xlabel=None,
    ylabel=None,
    title=None,
    legend_loc="upper right",
    bar_height=0.35,
    color_map=None,
    style_map=None,
    save=None,
    ax=None,
):
    # Create axes if needed
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    # Prepare data
    categories = list(data_dict.keys())
    y_positions = np.arange(len(categories))
    metrics = list(data_dict[categories[0]].keys())

    # Default color/hatch maps
    if not color_map:
        color_map = {m: None for m in metrics}
    if not style_map:
        style_map = {m: '/' for m in metrics}

    # Plot each metric as a set of horizontal bars
    all_bar_positions = []
    for i, metric in enumerate(metrics):
        values = [data_dict[cat][metric] for cat in categories]
        color = color_map.get(metric)
        hatch = style_map.get(metric, '/')

        # Offset each metric row
        offsets = (i - len(metrics)/2) * bar_height
        bar_pos = y_positions + offsets
        all_bar_positions.append(bar_pos)

        bars = ax.barh(
            bar_pos,
            values,
            height=bar_height,
            label=metric,
            color=color,
            linewidth=1,
            hatch=hatch
        )

        # Annotate each bar
        for bar in bars:
            # Darken edge for contrast
            face = mcolors.to_rgba(bar.get_facecolor(), alpha=1.0)
            edge_col = mcolors.to_hex([min(1, c*0.6) for c in face[:3]])
            bar.set_edgecolor(edge_col)

            w = bar.get_width()
            y = bar.get_y() + bar.get_height() / 2
            # Value label
            ax.text(
                w + max(values) * 0.01,  # small offset past bar
                y,
                f"{w:.0f}",
                va="center",
                ha="left",
                color=edge_col,
                fontweight="bold",
                fontsize=12
            )
            # little connector line
            ax.plot(
                [w, w + max(values) * 0.01],
                [y, y],
                lw=1.5,
                color=edge_col
            )

    # Set labels and ticks
    ax.set_yticks(y_positions)
    ax.set_yticklabels(categories)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    # Legend
    ax.legend(loc=legend_loc, ncol=len(metrics))

    plt.tight_layout()

    # Save if requested
    if save:
        fig.savefig(f"{save}.png", dpi=300, bbox_inches="tight")
        fig.savefig(f"{save}.pdf", dpi=300, bbox_inches="tight")

    return fig, ax
