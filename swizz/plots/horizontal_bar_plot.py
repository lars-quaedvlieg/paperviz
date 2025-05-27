from swizz.plots._registry import register_plot
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import colors as mcolors
from matplotlib.patches import Patch

@register_plot(
    name="general_horizontal_bar_plot",
    description="Horizontal bar plot comparing metrics for each category, with optional group-based coloring and legends.",
    args=[
        {"name": "df", "type": "pd.DataFrame", "required": True,
         "description": "DataFrame with category_column and metric columns."},
        {"name": "category_column", "type": "str", "required": True,
         "description": "Column used for y-axis labels."},
        {"name": "category_group_key", "type": "str", "required": False,
         "description": "Column used for group labels (used for colour and legend)."},
        {"name": "group_color_map", "type": "Dict[str, str]", "required": False,
         "description": "Mapping of group label → colour."},
        {"name": "figsize", "type": "tuple", "required": False, "description": "Figure size. Default: (12, 7)."},
        {"name": "xlabel", "type": "str", "required": False, "description": "Label for x-axis."},
        {"name": "ylabel", "type": "str", "required": False, "description": "Label for y-axis."},
        {"name": "title", "type": "str", "required": False, "description": "Title of the plot."},
        {"name": "legend_loc", "type": "str", "required": False, "description": "Legend location. Default: 'upper right'."},
        {"name": "bar_height", "type": "float", "required": False, "description": "Height of the bars. Default: 0.35."},
        {"name": "color_map", "type": "Dict[str, str]", "required": False, "description": "Mapping of metrics to colours."},
        {"name": "style_map", "type": "Dict[str, str]", "required": False, "description": "Mapping of metrics to hatch styles."},
        {"name": "put_legend", "type": "bool", "required": False, "description": "Whether to display a legend. Default: True."},
        {"name": "save", "type": "str", "required": False, "description": "Filename base to save PNG and PDF."},
        {"name": "ax", "type": "matplotlib.axes.Axes", "required": False, "description": "Optional matplotlib Axes object."},
    ],
    example_image="general_barh_plot.png",
    example_code="general_barh_plot.py",
)
def plot(
    df,
    category_column,
    category_group_key=None,
    group_color_map=None,
    figsize=(12, 7),
    xlabel=None,
    ylabel=None,
    title=None,
    legend_loc="upper right",
    bar_height=0.35,
    color_map=None,
    style_map=None,
    put_legend=True,
    save=None,
    ax=None,
):
    if not isinstance(df, pd.DataFrame):
        raise TypeError("`df` must be a pandas DataFrame.")

    if category_column not in df.columns:
        raise ValueError(f"`{category_column}` not in DataFrame.")

    categories = df[category_column].tolist()
    if category_group_key:
        groups = df[category_group_key].tolist()
    else:
        groups = None
    y_positions = np.arange(len(categories))
    metric_columns = [col for col in df.columns if col != category_column and (category_group_key is None or col != category_group_key)]

    if not color_map:
        color_map = {m: None for m in metric_columns}
    if not style_map:
        style_map = {m: '/' for m in metric_columns}

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    for i, metric in enumerate(metric_columns):
        values = df[metric].values
        offsets = (i - len(metric_columns) / 2) * bar_height
        bar_pos = y_positions + offsets
        hatch = style_map.get(metric, '/')

        # Determine colour for each bar
        if groups and group_color_map:
            bar_colors = [group_color_map.get(group, None) for group in groups]
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
            hatch=hatch,
        )

        for bar in bars:
            face = mcolors.to_rgba(bar.get_facecolor(), alpha=1.0)
            edge_col = mcolors.to_hex([min(1, c * 0.6) for c in face[:3]])
            bar.set_edgecolor(edge_col)

            w = bar.get_width()
            y = bar.get_y() + bar.get_height() / 2
            ax.text(
                w + max(values) * 0.01,
                y,
                f"{w:.3f}",
                va="center",
                ha="left",
                color=edge_col,
                fontweight="bold",
                fontsize=12
            )
            ax.plot([w, w + max(values) * 0.01], [y, y], lw=1.5, color=edge_col)

    # Axes and title
    ax.set_yticks(y_positions)
    ax.set_yticklabels(categories)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    # Custom legend
    if put_legend:
        if groups and group_color_map:
            handles = [Patch(facecolor=col, label=group) for group, col in group_color_map.items()]
            ax.legend(handles=handles, loc=legend_loc)
        else:
            ax.legend(loc=legend_loc, ncol=len(metric_columns))

    plt.tight_layout()

    if save:
        import os
        save_path = os.path.abspath(save)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        base, ext = os.path.splitext(save_path)
        if ext.lower() in ['.png', '.pdf']:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            fig.savefig(base + ('.pdf' if ext.lower() == '.png' else '.png'), dpi=300, bbox_inches='tight')
        else:
            fig.savefig(f"{save_path}.png", dpi=300, bbox_inches='tight')
            fig.savefig(f"{save_path}.pdf", dpi=300, bbox_inches='tight')

    return fig, ax
