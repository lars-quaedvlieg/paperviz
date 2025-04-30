from swizz.plots._registry import register_plot
import matplotlib.pyplot as plt
import numpy as np

@register_plot(
    name="percentile_curve_plot",
    description="Plot a curve showing scores ranked by percentile, with optional normalization, vertical/horizontal marker lines, and shaded regions for top scores.",
    args=[
        {"name": "scores", "type": "np.ndarray", "required": True, "description": "Array of raw scores to plot."},
        {"name": "normalize_scores", "type": "bool", "required": False, "description": "Whether to normalize scores between 0 and 1. Default: True."},
        {"name": "normalize_percentiles", "type": "bool", "required": False, "description": "Whether to normalize x-axis (percentile) between 0 and 1. Default: True."},
        {"name": "horizontal_markers", "type": "List[Tuple[float, str]]", "required": False, "description": "List of (y_value, label) for horizontal reference lines."},
        {"name": "vertical_markers", "type": "List[Tuple[float, str]]", "required": False, "description": "List of (x_value, label) for vertical reference lines."},
        {"name": "highlight_top_n", "type": "int", "required": False, "description": "Number of top scores to highlight with background shading. Default: None."},
        {"name": "highlight_color", "type": "str", "required": False, "description": "Background color for the highlight region. Default: light green."},
        {"name": "highlight_label", "type": "str", "required": False, "description": "Optional label to display inside the highlight area. Default: None."},
        {"name": "highlight_label_color", "type": "str", "required": False, "description": "Color for the highlight label text. Default: 'green'."},
        {"name": "highlight_label_font_size", "type": "int", "required": False, "description": "Font size for the highlight label text. Default: same as font_axis."},
        {"name": "vertical_label_offset", "type": "float", "required": False, "description": "Vertical offset above vertical marker in axis coordinates. Default: 0.02."},
        {"name": "xlabel", "type": "str", "required": False, "description": "Label for the x-axis. Default: 'Percentile'."},
        {"name": "ylabel", "type": "str", "required": False, "description": "Label for the y-axis. Default: 'Score'."},
        {"name": "title", "type": "str", "required": False, "description": "Title for the plot. Default: None."},
        {"name": "font_family", "type": "str", "required": False, "description": "Font family for text. Default: 'Times New Roman'."},
        {"name": "font_axis", "type": "int", "required": False, "description": "Font size for axis labels. Default: 14."},
        {"name": "figsize", "type": "tuple", "required": False, "description": "Figure size in inches. Default: (8, 5)."},
        {"name": "save", "type": "str", "required": False, "description": "Base filename to save PNG and PDF if provided."},
    ],
    example_image="percentile_curve_plot.png",
    example_code="percentile_curve_plot.py",
)
def plot(
    scores,
    normalize_scores=True,
    normalize_percentiles=True,
    horizontal_markers=None,
    vertical_markers=None,
    highlight_top_n=None,
    highlight_color="#c8e6c9",
    highlight_label=None,
    highlight_label_color="green",
    highlight_label_font_size=None,
    vertical_label_offset=0.02,
    xlabel="Percentile",
    ylabel="Score",
    title=None,
    font_family="Times New Roman",
    font_axis=14,
    figsize=(8, 5),
    save=None,
    ax=None,
):
    """
    Plot scores against percentile with optional normalization and highlighting.
    """

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    scores_sorted = np.sort(scores)
    percentiles = np.linspace(0, 1, len(scores_sorted))

    if not normalize_percentiles:
        percentiles = np.arange(len(scores_sorted)) / (len(scores_sorted) - 1)

    if normalize_scores:
        scores_min = np.min(scores_sorted)
        scores_max = np.max(scores_sorted)
        scores_sorted = (scores_sorted - scores_min) / (scores_max - scores_min)

    # Plot shaded region for top-N
    if highlight_top_n is not None and highlight_top_n > 0:
        n_highlight = highlight_top_n
        if n_highlight >= len(scores_sorted):
            n_highlight = len(scores_sorted)

        highlight_start = 1 - (n_highlight / len(scores_sorted))
        ax.axvspan(highlight_start, 1, color=highlight_color, alpha=0.5, zorder=0)

        # Add highlight label if provided
        if highlight_label:
            if highlight_label_font_size is None:
                highlight_label_font_size = font_axis
            ax.text((highlight_start + 1) / 2, 0.02, highlight_label,
                    fontsize=highlight_label_font_size, fontfamily=font_family,
                    color=highlight_label_color, ha='center', va='bottom')

    # Plot main line
    ax.plot(percentiles, scores_sorted, color="black", linewidth=2, label="Scores")

    # Plot horizontal markers
    if horizontal_markers:
        for y_val, label in horizontal_markers:
            ax.axhline(y=y_val, color="gray", linestyle="dashed", linewidth=1.5)
            ax.text(0.01, y_val, label, fontsize=font_axis - 2, fontfamily=font_family,
                    verticalalignment='bottom', horizontalalignment='left', color="gray")

    # Plot vertical markers
    if vertical_markers:
        for x_val, label in vertical_markers:
            idx = np.abs(percentiles - x_val).argmin()
            y_val = scores_sorted[idx]
            ax.plot([x_val, x_val], [0, y_val], color="gray", linestyle="dashed", linewidth=1.5)

            ax.text(x_val, y_val + vertical_label_offset, label,
                    fontsize=font_axis - 2, fontfamily=font_family,
                    verticalalignment='bottom', horizontalalignment='center', color="gray")

    ax.set_xlabel(xlabel, fontsize=font_axis, fontfamily=font_family)
    ax.set_ylabel(ylabel, fontsize=font_axis, fontfamily=font_family)

    if normalize_percentiles:
        ax.set_xticks(np.linspace(0, 1, 6))
        ax.set_xticklabels([f"{int(x * 100)}%" for x in np.linspace(0, 1, 6)])

    if normalize_scores:
        ax.set_yticks(np.linspace(0, 1, 6))
        ax.set_yticklabels([f"{int(x * 100)}%" for x in np.linspace(0, 1, 6)])

    if title:
        ax.set_title(title, fontsize=font_axis + 2, fontfamily=font_family)

    plt.tight_layout()

    if save:
        plt.savefig(f"{save}.png", dpi=300, bbox_inches="tight")
        plt.savefig(f"{save}.pdf", dpi=300, bbox_inches="tight")

    return fig, ax
