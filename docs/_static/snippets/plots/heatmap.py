import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from swizz import plot

# 1) Create a toy DataFrame (5 rows × 4 columns)
rows = [f"Sample {i}" for i in range(1, 6)]
cols = [f"Feature {j}" for j in range(1, 5)]
data = pd.DataFrame(
    np.random.rand(5, 4),
    index=rows,
    columns=cols
)

# 2) Plot with annotations, custom colormap, and save output
fig, ax = plot(
    "heatmap",
    data=data,
    figsize=(7, 5),
    cmap="Oranges",
    vmin=0.0,
    vmax=1.0,
    annot=False,
    fmt=".2f",
    cbar=True,
    title="Toy DataFrame Heatmap",
    save="dataframe_heatmap_example"
)

# 3) Show the figure
plt.show()
