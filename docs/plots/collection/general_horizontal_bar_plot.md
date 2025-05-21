# `general_horizontal_bar_plot`

> General horizontal bar plot comparing two (or more) metrics for each category with consistent colors and hatches.

---

## 📥 Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| data_dict | Dict[str, Dict[str, float]] | ✅ | Mapping of category names to a dict of metric→value. Categories are arbitrary strings. |
| figsize | tuple | ❌ | Figure size. Default: (12, 7). |
| xlabel | str | ❌ | Label for the x-axis. |
| ylabel | str | ❌ | Label for the y-axis. |
| title | str | ❌ | Title for the plot. |
| legend_loc | str | ❌ | Legend location. Default: 'upper right'. |
| bar_height | float | ❌ | Height of the bars. Default: 0.25. |
| color_map | Dict[str, str] | ❌ | Mapping of metrics to colors (used if no group-based coloring). |
| category_group_map | Dict[str, str] | ❌ | Mapping of each category name to a group key. Colors can then be assigned per group via `group_color_map`. |
| group_color_map | Dict[str, str] | ❌ | Mapping of group keys to colors. If provided, overrides `color_map`. |
| style_map | Dict[str, str] | ❌ | Mapping of metrics to hatch styles. |
| put_legend | bool | ❌ | Whether to show a legend. Default: True. |
| save | str | ❌ | Base filename to save PNG and PDF outputs (without extension). |
| ax | matplotlib.axes.Axes | ❌ | Matplotlib Axes to plot on. If None, a new figure is created. |

---

## 📦 Example Output

````{dropdown} Click to show example code
```python
import numpy as np
import matplotlib.pyplot as plt
from swizz import plot

# 1) Your data
data = {
    "64":  {"rate": 0.7835051},
    "128": {"rate": 0.8800000},
    "256": {"rate": 0.9368421},
    "512":  {"rate": 0.8913044},
    "1024": {"rate": 0.8800000},
    "2048": {"rate": 0.8736842},
    "0.95":  {"rate": 0.8297873},
    "0.99":  {"rate": 0.8800000},
    "0.995": {"rate": 0.7234042},
}

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
    "Discount factor":"#41047F",
    "Batch size":     "#7464AE",
    "Hidden size":    "#A3A1CB",
}

# 4) Plot
fig, ax = plot(
    "general_horizontal_bar_plot",
    data,
    figsize=(10, 6),
    xlabel="Lone-wolf capture rate",
    ylabel="",
    title="",
    bar_height=0.4,
    color_map=None,
    category_group_map=category_group_map,
    group_color_map=group_color_map,
    style_map={"rate": ""},    
    put_legend=True,         
    save="general_barh_plot",
    legend_loc="upper left",
)

plt.show()
```
````

<img src="../../_static/images/plots/general_barh_plot.png" alt="general_horizontal_bar_plot" style="max-width: 100%; width: auto; height: auto; max-height: 450px;">
