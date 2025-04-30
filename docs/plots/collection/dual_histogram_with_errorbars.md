# `dual_histogram_with_errorbars`

> Plot a main model histogram and multiple baseline histograms with mean frequencies and standard error bars.

---

## 📥 Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| data_main | List[np.ndarray] | ✅ | List of arrays with scores for the main dataset across seeds. |
| data_baseline_list | List[List[np.ndarray]] | ✅ | List of baselines, each a list of arrays across seeds. |
| baseline_labels | List[str] | ❌ | List of labels for each baseline. Default: Baseline 1, Baseline 2, etc. |
| baseline_colors | List[str] | ❌ | List of colors for each baseline. Default: auto colors. |
| num_bins | int | ❌ | Number of histogram bins. Default: 50. |
| main_color | str | ❌ | Color for the main dataset. Default: '#4C72B0'. |
| xlabel | str | ❌ | Label for the x-axis. Default: 'Score'. |
| ylabel | str | ❌ | Label for the y-axis. Default: 'Average Frequency'. |
| title | str | ❌ | Title for the plot. Default: None. |
| font_family | str | ❌ | Font family for text. Default: 'Times New Roman'. |
| font_axis | int | ❌ | Font size for axis labels. Default: 14. |
| figsize | tuple | ❌ | Figure size in inches. Default: (8, 5). |
| save | str | ❌ | Base filename to save PNG and PDF if provided. |

---

## 📦 Example Output

````{dropdown} Click to show example code
```python
import numpy as np
import matplotlib.pyplot as plt
from swizz import plot

# ---- 1. Generate Example Data ----

np.random.seed(42)

# Main model scores (5 seeds)
data_main = [
    np.random.normal(loc=100, scale=15, size=200),
    np.random.normal(loc=102, scale=15, size=200),
    np.random.normal(loc=98, scale=14, size=200),
    np.random.normal(loc=101, scale=13, size=200),
    np.random.normal(loc=99, scale=16, size=200),
]

# Baseline 1 (5 seeds, worse model)
data_baseline1 = [
    np.random.normal(loc=90, scale=18, size=200),
    np.random.normal(loc=92, scale=17, size=200),
    np.random.normal(loc=88, scale=19, size=200),
    np.random.normal(loc=89, scale=16, size=200),
    np.random.normal(loc=91, scale=18, size=200),
]

# Baseline 2 (5 seeds, slightly different from baseline 1)
data_baseline2 = [
    np.random.normal(loc=130, scale=16, size=200),
    np.random.normal(loc=126, scale=15, size=200),
    np.random.normal(loc=128, scale=16, size=200),
    np.random.normal(loc=132, scale=14, size=200),
    np.random.normal(loc=134, scale=15, size=200),
]

# ---- 2. Plot Dual Histogram with 2 baselines ----

fig, ax = plot("dual_histogram_with_errorbars",
    data_main=data_main,
    data_baseline_list=[data_baseline1, data_baseline2],
    baseline_labels=["Baseline 1", "Baseline 2"],
    baseline_colors=["#C44E52", "#55A868"],  # Red and Green
    num_bins=30,
    xlabel="Score",
    ylabel="Average Frequency",
    title="Main Model vs Two Baselines",
    main_color="#4C72B0",
    font_family="Times New Roman",
    font_axis=14,
    figsize=(8, 5),
)
plt.show()

```
````

<img src="../../_static/images/plots/dual_histogram_with_errorbars.png" alt="dual_histogram_with_errorbars" style="max-width: 100%; width: auto; height: auto; max-height: 450px;">
