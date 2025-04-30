import numpy as np
import matplotlib.pyplot as plt
from swizz import plot

# Generate fake scores
np.random.seed(42)
scores = np.random.normal(200, 400, size=500)

fig, ax = plot("percentile_curve_plot",
    scores=scores,
    normalize_scores=True,
    normalize_percentiles=True,
    horizontal_markers=[
        (0.9, "Prize Threshold"),
    ],
    vertical_markers=[
        (0.6, "Backbone\nPerformance"),
    ],
    highlight_top_n=70,
    highlight_label="Top 70",
    highlight_label_color="darkgreen",
    highlight_label_font_size=16,
    highlight_color="#c8e6c9",
    vertical_label_offset=0.03,
    xlabel="Percentile of contestants below score",
    ylabel="Normalized score",
    title="Synthetic Contest Performance",
    font_family="Times New Roman",
    font_axis=14,
    figsize=(8, 5),
)
plt.show()