import pandas as pd
import matplotlib.pyplot as plt
from swizz import plot

# 1) Prepare the data as a DataFrame
df = pd.DataFrame({
    "Category": ["64", "128", "256", "512", "1024", "2048", "0.95", "0.99", "0.995"],
    "rate": [0.7835051, 0.8800000, 0.9368421,
             0.8913044, 0.8800000, 0.8736842,
             0.8297873, 0.8800000, 0.7234042]
})

# 2) Map each category string into a group key
category_group_map = {
    "64":  "Hidden size",
    "128": "Hidden size",
    "256": "Hidden size",
    "512":  "Batch size",
    "1024": "Batch size",
    "2048": "Batch size",
    "0.95":  "Discount factor",
    "0.99":  "Discount factor",
    "0.995": "Discount factor",
}

# 3) Assign one color per group
group_color_map = {
    "Discount factor": "#41047F",
    "Batch size":      "#7464AE",
    "Hidden size":     "#A3A1CB",
}

# 4) Plot using the new function
fig, ax = plot(
    "general_horizontal_bar_plot",
    df=df,
    category_column="Category",
    category_group_map=category_group_map,
    group_color_map=group_color_map,
    xlabel="Lone-wolf capture rate",
    ylabel="",
    title="",
    bar_height=0.4,
    style_map={"rate": ""},
    put_legend=True,
    save="general_barh_plot",
    legend_loc="upper left",
)

plt.show()
