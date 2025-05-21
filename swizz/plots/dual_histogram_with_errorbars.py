import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from swizz.plots._registry import register_plot

@register_plot(
    name="dual_histogram_with_errorbars_df",
    description=(
        "Plot main model and baseline histograms with mean frequencies and standard error bars, "
        "using a pandas DataFrame in long format."
    ),
    args=[
        {"name": "data_df", "type": "pd.DataFrame", "required": True,
         "description": (
             "Long-form DataFrame containing one row per sample with columns for the dataset label, "
             "seed, and score."
         )},
        {"name": "label_key", "type": "str", "required": True,
         "description": "Column name in data_df that identifies the dataset (main or baseline)."},
        {"name": "seed_key", "type": "str", "required": True,
         "description": "Column name identifying the random seed for each sample."},
        {"name": "score_key", "type": "str", "required": True,
         "description": "Column name containing the score values."},
        {"name": "main_label", "type": "str", "required": False,
         "description": "Value in label_key that denotes the main model. If not provided, first label is used."},
        {"name": "baseline_labels", "type": "List[str]", "required": False,
         "description": "List of baseline labels; default is all labels except main_label."},
        {"name": "baseline_colors", "type": "List[str]", "required": False,
         "description": "Colors for each baseline label. Default palette is used."},
        {"name": "main_color", "type": "str", "required": False,
         "description": "Color for the main model. Default: '#4C72B0'."},
        {"name": "num_bins", "type": "int", "required": False,
         "description": "Number of histogram bins. Default: 50."},
        {"name": "xlabel", "type": "str", "required": False,
         "description": "Label for the x-axis. Default: 'Score'."},
        {"name": "ylabel", "type": "str", "required": False,
         "description": "Label for the y-axis. Default: 'Average Frequency'."},
        {"name": "title", "type": "str", "required": False,
         "description": "Plot title. Default: None."},
        {"name": "figsize", "type": "tuple", "required": False,
         "description": "Figure size. Default: (8, 5)."},
        {"name": "save", "type": "str", "required": False,
         "description": "Base path to save PNG and PDF if provided."},
    ],
    example_code="dual_histogram_with_errorbars_df_example.py",
    example_image="dual_histogram_with_errorbars.png",
)
def plot(
    data_df: pd.DataFrame,
    label_key: str,
    seed_key: str,
    score_key: str,
    main_label: str = None,
    baseline_labels: list = None,
    baseline_colors: list = None,
    main_color: str = "#4C72B0",
    num_bins: int = 50,
    xlabel: str = "Score",
    ylabel: str = "Average Frequency",
    title: str = None,
    figsize: tuple = (8, 5),
    save: str = None,
    ax=None,
):
    # Setup figure
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    # Determine labels
    labels = data_df[label_key].unique().tolist()
    if main_label is None:
        main_label = labels[0]
    if baseline_labels is None:
        baseline_labels = [lbl for lbl in labels if lbl != main_label]

    # Global bin edges
    all_scores = data_df[score_key].values
    min_score, max_score = all_scores.min(), all_scores.max()
    bins = np.linspace(min_score, max_score, num_bins + 1)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    # Function to compute mean and stderr per label
    def compute_stats(sub_df):
        # sub_df grouped by seed
        hist_matrix = np.stack(
            sub_df.groupby(seed_key)[score_key]
                  .apply(lambda arr: np.histogram(arr, bins=bins)[0])
                  .values
        )  # shape (n_seeds, n_bins)
        mean_freq = hist_matrix.mean(axis=0)
        stderr = hist_matrix.std(axis=0, ddof=0) / np.sqrt(hist_matrix.shape[0])
        return mean_freq, stderr

    # Plot baselines
    if baseline_colors is None:
        baseline_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    for lbl, color in zip(baseline_labels, baseline_colors):
        sub = data_df[data_df[label_key] == lbl]
        mean_freq, stderr = compute_stats(sub)
        ax.step(bin_centers, mean_freq, where='mid', color=color,
                linestyle='dashed', linewidth=2, label=lbl)
        ax.errorbar(bin_centers, mean_freq, yerr=stderr, fmt='s',
                    color=color, capsize=3, markersize=4, markerfacecolor='white')

    # Plot main model
    sub_main = data_df[data_df[label_key] == main_label]
    mean_main, stderr_main = compute_stats(sub_main)
    bar_width = bins[1] - bins[0]
    ax.bar(bin_centers, mean_main, width=bar_width,
           color=main_color, alpha=0.6, edgecolor='black', label=main_label)
    ax.errorbar(bin_centers, mean_main, yerr=stderr_main, fmt='o',
                color=main_color, capsize=3, markersize=4, markerfacecolor='white')

    # Labels and styling
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    plt.tight_layout()

    # Save
    if save:
        base, ext = save.rsplit('.', 1) if '.' in save else (save, None)
        if ext and ext.lower() in ['png', 'pdf']:
            fig.savefig(save, dpi=300, bbox_inches='tight')
        else:
            fig.savefig(f"{base}.png", dpi=300, bbox_inches='tight')
            fig.savefig(f"{base}.pdf", dpi=300, bbox_inches='tight')

    return fig, ax
