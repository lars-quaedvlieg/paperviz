from swizz.plots._registry import register_plot
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors as mcolors
from matplotlib.patches import Patch
@register_plot(
    name="general_horizontal_bar_plot",
    description=(
        "General horizontal bar plot comparing two (or more) metrics "
        "for each category with consistent colors and hatches."
    ),
    args=[
        {"name": "data_dict", "type": "Dict[str, Dict[str, float]]", "required": True,
         "description": (
             "Mapping of category names to a dict of metric→value. Categories are arbitrary strings."
         )},
        {"name": "figsize", "type": "tuple", "required": False,
         "description": "Figure size. Default: (12, 7)."},
        {"name": "xlabel", "type": "str", "required": False,
         "description": "Label for the x-axis."},
        {"name": "ylabel", "type": "str", "required": False,
         "description": "Label for the y-axis."},
        {"name": "title", "type": "str", "required": False,
         "description": "Title for the plot."},
        {"name": "legend_loc", "type": "str", "required": False,
         "description": "Legend location. Default: 'upper right'."},
        {"name": "bar_height", "type": "float", "required": False,
         "description": "Height of the bars. Default: 0.25."},
        {"name": "color_map", "type": "Dict[str, str]", "required": False,
         "description": (
             "Mapping of metrics to colors (used if no group-based coloring)."
         )},
        {"name": "category_group_map", "type": "Dict[str, str]", "required": False,
         "description": (
             "Mapping of each category name to a group key. "
             "Colors can then be assigned per group via `group_color_map`."
         )},
        {"name": "group_color_map", "type": "Dict[str, str]", "required": False,
         "description": (
             "Mapping of group keys to colors. "
             "If provided, overrides `color_map`."
         )},
        {"name": "style_map", "type": "Dict[str, str]", "required": False,
         "description": "Mapping of metrics to hatch styles."},
        {"name": "put_legend", "type": "bool", "required": False,
         "description": "Whether to show a legend. Default: True."},
        {"name": "save", "type": "str", "required": False,
         "description": "Base filename to save PNG and PDF outputs (without extension)."},
        {"name": "ax", "type": "matplotlib.axes.Axes", "required": False,
         "description": "Matplotlib Axes to plot on. If None, a new figure is created."},
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
    category_group_map=None,
    group_color_map=None,
    style_map=None,
    save=None,
    put_legend=True,
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
        # Determine colors per bar
        if category_group_map and group_color_map:
            bar_colors = []
            for cat in categories:
                grp = category_group_map.get(cat)
                bar_colors.append(group_color_map.get(grp, color_map.get(metric)))
        else:
            bar_colors = [color_map.get(metric)] * len(categories)
        bars = ax.barh(
            bar_pos,
            values,
            height=bar_height,
            label=metric,
            color=bar_colors,
            edgecolor=None,
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
                f"{w:.3f}",
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
    if put_legend:
        if category_group_map and group_color_map:
            # show groups in legend
            handles = [Patch(color=color, label=group)
                       for group, color in group_color_map.items()]
            ax.legend(handles=handles, loc=legend_loc)
        else:
            ax.legend(loc=legend_loc, ncol=len(metrics))

    plt.tight_layout()


    # Save if requested
    if save:
        import os
        # Resolve to absolute path and ensure directory exists
        save_path = os.path.abspath(save)
        save_dir = os.path.dirname(save_path)
        if save_dir and not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
        base, ext = os.path.splitext(save_path)
        # Save both formats (png/pdf)
        if ext.lower() in ['.png', '.pdf']:
            # Save given format
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            # Also save the other format
            other = '.pdf' if ext.lower() == '.png' else '.png'
            fig.savefig(base + other, dpi=300, bbox_inches='tight')
            print(f"Saved plot to {save_path} and {base + other}")
        else:
            fig.savefig(f"{save_path}.png", dpi=300, bbox_inches='tight')
            fig.savefig(f"{save_path}.pdf", dpi=300, bbox_inches='tight')



    return fig, ax
