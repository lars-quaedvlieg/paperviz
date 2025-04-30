# `general_bar_plot`

> General bar plot comparing two metrics (e.g., Reward and Goal) for each category with consistent colors.

---

## 📥 Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| data_dict | Dict[str, Dict[str, np.ndarray]] | ✅ | Each key is a category (e.g., 'No F Tz', 'F Tz') and maps to a dict with arrays for metrics. |
| figsize | tuple | ❌ | Size of the figure. Default: (10, 6). |
| xlabel | str | ❌ | Label for the x-axis. |
| ylabel | str | ❌ | Label for the y-axis. |
| title | str | ❌ | Title for the plot. |
| legend_loc | str | ❌ | Location for the legend. Default: 'upper left'. |
| bar_width | float | ❌ | Width of the bars. Default: 0.25. |
| color_map | Dict[str, str] | ❌ | Mapping of metrics to colors. |
| style_map | Dict[str, str] | ❌ | Mapping of metrics to hatch styles. |
| save | str | ❌ | Base filename to save PNG and PDF. |

---

## 📦 Example Output

````{dropdown} Click to show example code
```python
import numpy as np
from matplotlib import pyplot as plt
from swizz import plot

data_dict = {
    "Forward": {
        "Accuracy": 4.2, "Precision": 3.5, "Recall": 2.1,
    },
    "Reverse": {
        "Accuracy": 6.0, "Precision": 5.2, "Recall": 4.8,
    },
    "Baseline": {
        "Accuracy": 5.3, "Precision": 4.8, "Recall": 3.6,
    }
}

# Color map where 'Reward' is assigned blue and 'Goal' is assigned pink


# Style map for each metric (hatch patterns for filling)
style_map = {
    "Accuracy": '',
    "Precision": '\\',
    "Recall": 'x'  # Cross hatch pattern for Recall
}

plot("general_bar_plot",data_dict,style_map=style_map,save="bar")
plt.show()

```
````

<img src="../../_static/images/plots/general_bar_plot.png" alt="general_bar_plot" style="max-width: 100%; width: auto; height: auto; max-height: 450px;">
