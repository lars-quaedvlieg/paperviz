from swizz.plots._registry import register_plot
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

@register_plot(
    name="heatmap",
    description="Plot a heatmap of any pandas DataFrame with optional axis labels, annotations, and custom color-scaling.",
    args=[
        {"name": "data", "type": "pd.DataFrame", "required": True,
         "description": "Pandas DataFrame containing the matrix to visualize; index and columns are used as y- and x-labels by default."},
        {"name": "x_labels", "type": "List[str]", "required": False,
         "description": "Labels for columns (overrides DataFrame columns)."},
        {"name": "y_labels", "type": "List[str]", "required": False,
         "description": "Labels for rows (overrides DataFrame index)."},
        {"name": "x_category", "type": "str", "required": False,
            "description": "Category for x-axis labels (overrides DataFrame columns)."},
        {"name": "y_category", "type": "str", "required": False,
        "description": "Category for y-axis labels (overrides DataFrame index)."},
        {"name": "figsize", "type": "tuple", "required": False,
         "description": "Figure size (width, height), e.g., (8, 6)."},
        {"name": "cmap", "type": "str", "required": False,
         "description": "Name of matplotlib colormap, e.g., 'viridis'."},
        {"name": "vmin", "type": "float", "required": False,
         "description": "Minimum data value for color scaling."},
        {"name": "vmax", "type": "float", "required": False,
         "description": "Maximum data value for color scaling."},
        {"name": "annot", "type": "bool", "required": False,
         "description": "If True, overlay numeric annotations on each cell."},
        {"name": "fmt", "type": "str", "required": False,
         "description": "Format string for annotations, e.g. '.2f' or 'd'."},
        {"name": "cbar", "type": "bool", "required": False,
         "description": "Whether to display the colorbar."},
        {"name": "title", "type": "str", "required": False,
         "description": "Title of the heatmap."},
        {"name": "save", "type": "str", "required": False,
         "description": "Base filename to save PNG and PDF (without extension)."},
        {"name": "cbar_title", "type": "str", "required": False,
         "description": "Title for the colorbar."},
        {"name": "ax", "type": "matplotlib.axes.Axes", "required": False,
         "description": "Matplotlib Axes object to plot on. If None, a new figure is created."},
    ],
    example_code="heatmap.py",
    example_image="heatmap.png",
)
def plot(
    data: pd.DataFrame,
    x_labels=None,
    y_labels=None,
    x_category=None,
    y_category=None,
    figsize=(8, 6),
    cmap='viridis',
    vmin=None,
    vmax=None,
    annot=False,
    fmt='.2f',
    cbar=True,
    title=None,
    save=None,
    ax=None,
    cbar_title="Intensity",
):
    # Prepare figure/axis
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    # Ensure DataFrame
    if not isinstance(data, pd.DataFrame):
        raise ValueError("`data` must be a pandas DataFrame")

    # Extract values and labels
    arr = data.values
    cols = x_labels if x_labels is not None else list(data.columns)
    rows = y_labels if y_labels is not None else list(data.index)

    # Display image
    im = ax.imshow(arr, interpolation='nearest',
                   cmap=cmap, vmin=vmin, vmax=vmax)
    if cbar:
        cbar_obj = fig.colorbar(im, ax=ax)
        if cbar_title:
            # Place the title vertically on the left side
            cbar_ax = cbar_obj.ax
            cbar_ax.yaxis.set_label_position('right')
            cbar_ax.yaxis.set_ticks_position('right')
            cbar_obj.set_label(
                cbar_title,
                rotation=90,
                labelpad=12,
                fontsize=12
            )

    # Annotate cells if requested
    if annot:
        thresh = (vmax if vmax is not None else arr.max()) / 2.0
        n_rows, n_cols = arr.shape
        for i in range(n_rows):
            for j in range(n_cols):
                val = arr[i, j]
                color = 'white' if val > thresh else 'black'
                ax.text(j, i, format(val, fmt),
                        ha='center', va='center',
                        color=color, fontweight='bold')

    # Set tick labels
    ax.set_xticks(np.arange(len(cols)))
    ax.set_xticklabels(cols)
    plt.setp(ax.get_xticklabels(), rotation=0, ha="right")
    ax.set_yticks(np.arange(len(rows)))
    ax.set_yticklabels(rows)
    ax.set_xlabel(x_category if x_category else "")
    ax.set_ylabel(y_category if y_category else "")

    if title:
        ax.set_title(title)
    plt.tight_layout()

    # Save to files if requested
    if save:
        import os
        # Determine file paths
        # If save has an extension, use it directly; otherwise append .png and .pdf
        save_dir = os.path.dirname(save)
        if save_dir and not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
        base, ext = os.path.splitext(save)
        if ext.lower() in ['.png', '.pdf']:
            # single file provided
            fig.savefig(save, dpi=300, bbox_inches='tight')
        else:
            fig.savefig(f"{save}.png", dpi=300, bbox_inches='tight')
            fig.savefig(f"{save}.pdf", dpi=300, bbox_inches='tight')


    return fig, ax
