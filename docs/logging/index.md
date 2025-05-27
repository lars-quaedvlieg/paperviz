# 🪵 Logging

We support Weights & Biases (wandb) for experiment tracking and analysis. This page documents our tools for analyzing wandb runs.

## WandbAnalyzer

The `WandbAnalyzer` is a powerful tool for analyzing and comparing multiple wandb runs. When running experiments, you often need to handle multiple runs with the same seed (e.g., from restarted jobs), compare results across different seeds, or analyze multiple experiment configurations. The WandbAnalyzer makes this process seamless by automatically handling these common scenarios.

Key benefits:
- One-liner data retrieval from wandb, no more manual run filtering and data extraction
- Seamless integration with our plotting utilities for beautiful visualizations
- Automatic handling of restarted runs and multiple seeds
- Clean, pandas-based interface for further analysis

### Basic Usage

```python
from swizz.logging.wandb_analyzer import WandbAnalyzer, RunGroup

# Initialize the analyzer
analyzer = WandbAnalyzer("your-username/your-project", verbose=True)

# Define run groups (either by prefix or run IDs)
run_groups = [
    RunGroup(name="experiment1", prefix="your-prefix-1"),
    RunGroup(name="experiment2", prefix="your-prefix-2"),
]

# Or using run IDs
run_groups = [
    RunGroup(name="experiment1", run_ids=["run1", "run2"]),
    RunGroup(name="experiment2", run_ids=["run3", "run4"]),
]

# Get analyzed metrics
results_df = analyzer.compute_grouped_metrics(
    run_groups,
    x_key="round_num",
    y_key="your_metric"
)
```

### Analysis Methods

The analyzer provides two main ways to work with your data. The first is getting the raw stitched data, which gives you complete control over how you process and analyze the results. This is particularly useful when you need to perform custom analysis or when you want to inspect the data before computing statistics:

```python
# Get raw stitched data for custom analysis
stitched_data = analyzer.get_stitched_runs(
    run_groups,
    x_key="round_num",
    y_key="your_metric"
)
```

The second, and more commonly used method, is computing grouped metrics across seeds. This is where the analyzer really shines - it automatically handles all the complexity of combining runs from the same seed and computing statistics across different seeds. The result is a clean pandas DataFrame that's ready for visualization or further analysis:

```python
# Get pre-computed metrics
results_df = analyzer.compute_grouped_metrics(
    run_groups,
    x_key="round_num",
    y_key="your_metric"
)
```

The resulting DataFrame contains columns for the group name, x-axis values, mean and standard deviation of your metric, and the number of seeds used in the computation.

### Visualization Example

The grouped metrics can be easily visualized using our plotting utilities. This is where the analyzer's integration with our plotting system really pays off - you can go from raw wandb data to publication-quality plots in just a few lines:

```python
import swizz
import matplotlib.pyplot as plt

# Get analyzed metrics
results_df = analyzer.compute_grouped_metrics(run_groups, x_key="round_num", y_key="your_metric")

# Create a plot
fig, ax = swizz.plot(
    "multiple_std_lines_df",
    figsize=(8, 5),
    data_df=results_df,
    label_key="group_name",
    x_key="round_num",
    y_key="your_metric_mean",
    yerr_key="your_metric_std",
    xlabel="X Axis Label",
    ylabel="Y Axis Label",
    legend_title="Legend Title",
)

plt.show()
```

### Verbose Logging

The analyzer includes an optional verbose logging mode that provides detailed information about the analysis process. When enabled, it shows you the number of runs found for each group, how they're distributed across seeds, and any potential issues like missing data or NaN values. This is particularly helpful when debugging or when you want to understand exactly how your data is being processed.

### Handling Edge Cases

The analyzer is designed to handle common edge cases gracefully. If you have a single run, it's automatically assigned to seed 0 since seed-based analysis isn't relevant. Similarly, if some runs don't have a seed specified, they're grouped together under seed 0. The analyzer also handles NaN values and overlapping data points automatically, ensuring you get clean, reliable results without manual intervention.