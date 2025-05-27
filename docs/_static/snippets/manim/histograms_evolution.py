from swizz import render_manim
import numpy as np
import pandas as pd

# Create the dataframe
methods = ['Method A', 'Method B', 'Method C']
iterations = range(30)
scores = []

for method in methods:
    for iteration in iterations:
        # Generate some random scores that evolve over iterations
        # Each method has a different mean and variance
        if method == 'Method A':
            mean = 50 + iteration * 1  # Gradually increasing mean
            std = 10 + iteration * 3
        elif method == 'Method B':
            mean = 40 + iteration * 2  # Steeper increase
            std = 15 + iteration * 0.5
        else:  # Method C
            mean = 45 + iteration * 3  # Moderate increase
            std = 12
            
        # Generate 100 scores for each method-iteration combination
        scores.extend([(method, iteration, score) for score in np.random.normal(mean, std, 300)])

scores_df = pd.DataFrame(scores, columns=['method', 'iteration', 'score'])

# Configuration for the Manim renderer
# All attributes can be found at https://docs.manim.community/en/stable/reference/manim._config.utils.ManimConfig.html
manim_render_config = {
    "quality": "high_quality",
    "format": "mp4",
    "save_pngs": True,
}

render_manim(
    "histograms_evolution",
    render_config=manim_render_config,
    scores_df=scores_df,
    method_column="method",
    iteration_column="iteration",
    score_column="score",
    x_min=0,
    x_max=100,
    x_step=10,
    num_bins=60,
    x_length=10,
    y_length=5,
    time_between_iterations=0.5,
    color_dict={
        "Method A": "#1f77b4",
        "Method B": "#ff7f0e",
        "Method C": "#2ca02c",
    },
)