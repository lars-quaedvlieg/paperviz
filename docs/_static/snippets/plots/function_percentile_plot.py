import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from swizz import plot, set_style

# Example function
transform_full = lambda r, c, s: ((np.tanh((r + c) / s) + 1) / (1 + np.tanh(c / s))) * 2 - 1
transform = lambda r, s: transform_full(r, 0, s)

# Generate Data
failed_reward, max_reward = -1500, 0
scores = np.linspace(failed_reward, max_reward, 500)

reward_scales = [500, 750, 1000, 1500, 2000, 3000, 4000, 5000, 7500]

data = []
for scale in reward_scales:
    transformed_scores = transform(scores, scale)
    for x, y in zip(scores, transformed_scores):
        data.append({'x': x, 'y': y, 'group': f'scale={scale}'})

df = pd.DataFrame(data)

# Call the plot method
fig, ax = plot("function_percentile_plot",
    df,
    xlabel="Original Reward",
    ylabel="Transformed Reward",
    title="Transformed Rewards Across Scales",
    cmap="viridis",
    legend_title="Scale",
    min_label_val=-0.98,
    max_label_val=0.8,
    function_str=r'$r_{new} = \frac{\tanh\left(\frac{r + c}{s}\right) + 1}{1 + \tanh\left(\frac{c}{s}\right)} \cdot 2 - 1$',
)
plt.show()