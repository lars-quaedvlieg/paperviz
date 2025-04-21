# `general_horizontal_bar_plot`

> General horizontal bar plot comparing two (or more) metrics for each category with consistent colors and hatches.

---

## 📥 Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| data_dict | Dict[str, Dict[str, float]] | ✅ | Each key is a category and maps to a dict of metric→value. |
| figsize | tuple | ❌ | Size of the figure. Default: (10, 6). |
| xlabel | str | ❌ | Label for the x-axis. |
| ylabel | str | ❌ | Label for the y-axis. |
| title | str | ❌ | Title for the plot. |
| legend_loc | str | ❌ | Location for the legend. Default: 'upper right'. |
| bar_height | float | ❌ | Height of the bars. Default: 0.25. |
| color_map | Dict[str, str] | ❌ | Mapping of metrics to colors. |
| style_map | Dict[str, str] | ❌ | Mapping of metrics to hatch styles. |
| save | str | ❌ | Base filename to save PNG and PDF. |

---

## 📦 Example Output

````{dropdown} Click to show example code
```python
import numpy as np
from matplotlib import pyplot as plt
from paperviz import plot

data = {
    "No APM limit": {"Test Elo": 1392},
    "200% APM limit": {"Test Elo": 1411},
    "100% APM limit": {"Test Elo": 1540},
    "50% APM limit": {"Test Elo": 1536},
    "25% APM limit": {"Test Elo": 1419},
    "10% APM limit": {"Test Elo": 1145},
    "0% APM limit": {"Test Elo": 0},
}
fig, ax = plot("general_horizontal_bar_plot",
    data,
    xlabel="Test Elo",
    ylabel="APM limits",
    color_map={"Test Elo": "#FF7F0E"},
    bar_height=0.45,
    style_map={"Test Elo": ""},
    save="general_barh_plot",
)
plt.show()

```
````

<img src="../../_static/images/plots/general_barh_plot.png" alt="general_horizontal_bar_plot" style="max-width: 100%; width: auto; height: auto; max-height: 450px;">
