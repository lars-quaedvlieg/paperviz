from swizz.plots._registry import register_plot
import matplotlib.pyplot as plt
import numpy as np

@register_plot(
    name="dual_histogram_with_errorbars",
    description="Plot a main model histogram and multiple baseline histograms with mean frequencies and standard error bars.",
    args=[
        {"name": "data_main", "type": "List[np.ndarray]", "required": True, "description": "List of arrays with scores for the main dataset across seeds."},
        {"name": "data_baseline_list", "type": "List[List[np.ndarray]]", "required": True, "description": "List of baselines, each a list of arrays across seeds."},
        {"name": "baseline_labels", "type": "List[str]", "required": False, "description": "List of labels for each baseline. Default: Baseline 1, Baseline 2, etc."},
        {"name": "baseline_colors", "type": "List[str]", "required": False, "description": "List of colors for each baseline. Default: auto colors."},
        {"name": "num_bins", "type": "int", "required": False, "description": "Number of histogram bins. Default: 50."},
        {"name": "main_color", "type": "str", "required": False, "description": "Color for the main dataset. Default: '#4C72B0'."},
        {"name": "xlabel", "type": "str", "required": False, "description": "Label for the x-axis. Default: 'Score'."},
        {"name": "ylabel", "type": "str", "required": False, "description": "Label for the y-axis. Default: 'Average Frequency'."},
        {"name": "title", "type": "str", "required": False, "description": "Title for the plot. Default: None."},
        {"name": "font_family", "type": "str", "required": False, "description": "Font family for text. Default: 'Times New Roman'."},
        {"name": "font_axis", "type": "int", "required": False, "description": "Font size for axis labels. Default: 14."},
        {"name": "figsize", "type": "tuple", "required": False, "description": "Figure size in inches. Default: (8, 5)."},
        {"name": "save", "type": "str", "required": False, "description": "Base filename to save PNG and PDF if provided."},
    ],
    example_image="dual_histogram_with_errorbars.png",
    example_code="dual_histogram_with_errorbars.py",
)
def plot(
    data_main,
    data_baseline_list,
    baseline_labels=None,
    baseline_colors=None,
    num_bins=50,
    main_color="#4C72B0",
    xlabel="Score",
    ylabel="Average Frequency",
    title=None,
    font_family="Times New Roman",
    font_axis=14,
    figsize=(8, 5),
    save=None,
    ax=None,
):
    """
    Plot main model histogram and multiple baselines with error bars.
    """

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    # Flatten and get global min/max
    all_scores = np.concatenate([np.concatenate(data_main)] + [np.concatenate(b) for b in data_baseline_list])
    min_score, max_score = np.min(all_scores), np.max(all_scores)

    bins = np.linspace(min_score, max_score, num_bins + 1)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    # Main model
    histograms_main = np.array([np.histogram(seed_scores, bins=bins)[0] for seed_scores in data_main])
    mean_freq_main = np.mean(histograms_main, axis=0)
    stderr_freq_main = np.std(histograms_main, axis=0) / np.sqrt(len(data_main))

    # Plot baselines
    if baseline_labels is None:
        baseline_labels = [f"Baseline {i+1}" for i in range(len(data_baseline_list))]

    if baseline_colors is None:
        baseline_colors = ["#C44E52", "#55A868", "#8172B2"]  # Expandable palette

    for i, (baseline_data, label, color) in enumerate(zip(data_baseline_list, baseline_labels, baseline_colors)):
        histograms_baseline = np.array([np.histogram(seed_scores, bins=bins)[0] for seed_scores in baseline_data])
        mean_freq_baseline = np.mean(histograms_baseline, axis=0)
        stderr_freq_baseline = np.std(histograms_baseline, axis=0) / np.sqrt(len(baseline_data))

        ax.step(bin_centers, mean_freq_baseline, where='mid',
                color=color, linestyle='dashed', linewidth=2, label=label)
        ax.errorbar(bin_centers, mean_freq_baseline, yerr=stderr_freq_baseline, fmt='s',
                    color=color, capsize=3, markersize=4, markerfacecolor='white')

    # Plot main model bar
    bar_width = bins[1] - bins[0]
    ax.bar(bin_centers, mean_freq_main, width=bar_width,
           color=main_color, alpha=0.6, edgecolor='black', label="Main Model")
    ax.errorbar(bin_centers, mean_freq_main, yerr=stderr_freq_main, fmt='o',
                color=main_color, capsize=3, markersize=4, markerfacecolor='white')

    ax.set_xlabel(xlabel, fontsize=font_axis, fontfamily=font_family)
    ax.set_ylabel(ylabel, fontsize=font_axis, fontfamily=font_family)
    if title:
        ax.set_title(title, fontsize=font_axis+2, fontfamily=font_family)

    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend()
    plt.tight_layout()

    if save:
        plt.savefig(f"{save}.png", dpi=300, bbox_inches="tight")
        plt.savefig(f"{save}.pdf", dpi=300, bbox_inches="tight")

    return fig, ax