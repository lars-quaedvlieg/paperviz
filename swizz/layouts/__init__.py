import matplotlib.pyplot as plt
from swizz.layouts.blocks import PlotBlock, LegendBlock
import importlib
import os

# Dynamically import all .py files in the tables directory (excluding special files)
for filename in os.listdir(os.path.join(os.path.dirname(__file__), "collection")):
    if filename.endswith(".py") and not filename.startswith(("_", "__")):
        importlib.import_module(f"swizz.layouts.collection.{filename[:-3]}")


def render_layout(layout, figsize=(10, 6), margins=0.05):
    """
    Args:
        layout: Layout object (Row, Col, etc)
        figsize: tuple, figure size in inches
        margins: float or (left, bottom, right, top) tuple; margin as fraction of figure
    """
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=figsize)

    # Handle margins
    if isinstance(margins, (float, int)):
        left = bottom = right = top = margins
    else:
        left, bottom, right, top = margins

    # First pass: collect blocks
    all_blocks = []

    def get_all_blocks(node):
        all_blocks.append(node)
        if hasattr(node, "children"):
            for child in node.children:
                get_all_blocks(child)

    get_all_blocks(layout)

    # Layout once to capture plots
    layout.layout(fig, [
        left,
        bottom,
        1.0 - left - right,
        1.0 - top - bottom
    ])

    # Find plots and legends
    plot_axes = [
        block.last_ax for block in all_blocks
        if isinstance(block, PlotBlock) and not block.exclude_from_legend and block.last_ax is not None
    ]
    legend_blocks = [
        block for block in all_blocks if isinstance(block, LegendBlock) and block.handles is None
    ]

    # If any LegendBlocks: fill them
    if legend_blocks:
        for legend in legend_blocks:
            handles, labels = [], []
            for ax in plot_axes:
                hs, ls = ax.get_legend_handles_labels()
                for h, l in zip(hs, ls):
                    if l not in labels and l in legend.labels:
                        handles.append(h)
                        labels.append(l)
            if handles:
                legend.set_handles(handles, labels)

        # Second layout pass
        layout.layout(fig, [
            left,
            bottom,
            1.0 - left - right,
            1.0 - top - bottom
        ])

    return fig
