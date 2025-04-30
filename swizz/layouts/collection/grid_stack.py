from swizz.layouts._registry import register_layout
from swizz.layouts.blocks import Row, Col

@register_layout(
    name="grid_stack",
    description="Create an n x m grid of plots with only outer row/column showing axis labels."
)
def grid_stack(n_rows, n_cols, plot_fn, spacing=0.05):
    """
    Create an n x m grid layout.

    Args:
        n_rows: Number of rows
        n_cols: Number of columns
        plot_fn: A function that takes (row_idx, col_idx) and returns a PlotBlock
        row_heights: Optional list of relative row heights (len=n_rows)
        col_widths: Optional list of relative col widths (len=n_cols)
        spacing: Spacing between plots

    Returns:
        A Col containing the full layout.
    """
    rows = []
    for i in range(n_rows):
        row_children = []
        for j in range(n_cols):
            block = plot_fn(i, j)
            row_children.append(block)

        row = Row(
            row_children,
            spacing=spacing
        )
        rows.append(row)

    full_layout = Col(
        rows,
        spacing=spacing
    )
    return full_layout
