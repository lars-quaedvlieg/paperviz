import matplotlib.pyplot as plt

from paperviz.layout.blocks import PlotBlock, LegendBlock


def render_layout(layout, figsize=(10, 6), margin=0.05):
    fig = plt.figure(figsize=figsize)

    # Pass 1: layout everything and track blocks
    all_blocks = []

    def get_all_blocks(node):
        all_blocks.append(node)
        if hasattr(node, "children"):
            children = node.children
            for c in children:
                get_all_blocks(c)

    get_all_blocks(layout)

    # Render once to get the legend information
    layout.layout(fig, [
        margin, margin,
        1.0 - 2 * margin,
        1.0 - 2 * margin
    ])

    # Pass 2: fill in any LegendBlocks
    plot_axes = [
        block.last_ax for block in all_blocks
        if isinstance(block, PlotBlock) and not block.exclude_from_legend and block.last_ax is not None
    ]
    legend_blocks = [
        block for block in all_blocks if isinstance(block, LegendBlock) and block.handles is None
    ]

    if len(legend_blocks) > 0:
        for legend in legend_blocks:
            handles, labels = [], []
            for ax in plot_axes:
                hs, ls = ax.get_legend_handles_labels()
                for h, l in zip(hs, ls):
                    if l not in labels and l in legend.labels:
                        handles.append(h)
                        labels.append(l)
            if len(handles) > 0:
                legend.set_handles(handles, labels)

        # Render again to plot the legends
        # TODO: Find a more efficient way to do this
        layout.layout(fig, [
            margin, margin,
            1.0 - 2 * margin,
            1.0 - 2 * margin
        ])

    return fig
