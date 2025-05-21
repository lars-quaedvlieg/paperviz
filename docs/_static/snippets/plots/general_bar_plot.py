import pandas as pd
from swizz import plot
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "Condition": ["No FTz", "FTz"],
    "Reward": [1.0, 1.2],
    "Goal": [0.7, 0.9],
})

fig, ax = plot("general_bar_plot",
    df=df,
    category_column="Condition",
    ylabel="Avg Value",
    title="Comparison of Reward and Goal",
    color_map={"Reward": "tab:blue", "Goal": "tab:orange"},
    style_map={"Reward": "/", "Goal": "\\"},
    bar_width=0.3,
    save="general_bar_plot"
)
plt.show()
