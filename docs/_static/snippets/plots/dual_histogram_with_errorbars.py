import numpy as np
import matplotlib.pyplot as plt
from paperviz import plot

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
