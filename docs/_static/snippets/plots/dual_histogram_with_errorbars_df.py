import numpy as np
import matplotlib.pyplot as plt
from swizz import plot
import pandas as pd

np.random.seed(42)
records = []
# Main model (5 seeds)
for seed in range(5):
    scores = np.random.normal(loc=100 + seed*0, scale=15, size=200)
    for s in scores:
        records.append({"label": "Main Model", "seed": seed, "score": s})
# Baseline 1 (5 seeds)
for seed in range(5):
    scores = np.random.normal(loc=90 + seed*0, scale=18, size=200)
    for s in scores:
        records.append({"label": "Baseline 1", "seed": seed, "score": s})
# Baseline 2 (5 seeds)
for seed in range(5):
    scores = np.random.normal(loc=130 + seed*0, scale=16, size=200)
    for s in scores:
        records.append({"label": "Baseline 2", "seed": seed, "score": s})
data_df = pd.DataFrame(records)

# ---- 2. Plot Dual Histogram with Error Bars ----
fig, ax = plot(
    "dual_histogram_with_errorbars_df",
    data_df,
    label_key="label",
    seed_key="seed",
    score_key="score",
    main_label="Main Model",
    baseline_labels=["Baseline 1", "Baseline 2"],
    baseline_colors=["#C44E52", "#55A868"],
    num_bins=30,
    xlabel="Score",
    ylabel="Average Frequency",
    title="Main Model vs Two Baselines",
    main_color="#4C72B0",
    figsize=(8, 5),
)
plt.show()
