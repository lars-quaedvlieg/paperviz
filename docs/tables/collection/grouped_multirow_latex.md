# `grouped_multirow_latex`

> Render a grouped LaTeX table with two-level row headers (e.g., Domain and Task) and flat method columns (e.g., MLP, Modality, Component).
> - Input must be a flat DataFrame with (row1, row2, column, value) format.
> - Each value should be a float or a list of floats, from which mean ± std or stderr is computed.
> - Bolds the best (min or max) per row.

---

## 🧾 Required LaTeX packages / commands

- `\usepackage{booktabs}`
- `\usepackage{multirow}`
- `\newcommand{\highlightcolor}[1]{\colorbox[HTML]{bae6fb}{\textbf{#1}}}`


---

## 📥 Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| df | pd.DataFrame | ✅ | DataFrame with columns for row1, row2, column, and values (as lists or floats). |
| row1 | str | ✅ | Column name for the outer row grouping (e.g., Domain). |
| row2 | str | ✅ | Column name for the row label (e.g., Task). |
| col | str | ✅ | Column name representing the method axis (e.g., Method). |
| value_column | str | ✅ | Column name containing scalar or list-of-floats to summarize. |
| highlight | str | ❌ | 'min' or 'max' to bold best value per row. |
| stderr | bool | ❌ | Use standard error instead of std when formatting. |
| caption | str | ❌ | LaTeX caption to display below the table. |
| label | str | ❌ | Optional LaTeX label for referencing. |

---

## 📦 Example Output

````{dropdown} Click to show example code
```python
import numpy as np
import pandas as pd
from paperviz import table

np.random.seed(0)

domains = ["HalfCheetah", "Hopper", "Walker2d", "Ant"]
tasks = ["IL (↑) [1]", "Off-RL (↑) [1]", "Sensor failure (↑) [11]", "Dynamics change (↑) [4]"]
methods = ["MLP", "Modality", "Component"]

rows = []
for domain in domains:
    for task in tasks:
        for method in methods:
            values = np.round(np.random.normal(loc=1.0, scale=0.05, size=5), 3).tolist()
            rows.append({
                "Domain": domain,
                "Task": task,
                "Method": method,
                "score": values
            })

df = pd.DataFrame(rows)

latex = table(
    "grouped_multirow_latex",
    df=df,
    row1="Domain",
    row2="Task",
    col="Method",
    value_column="score",
    highlight="max",
    stderr=False,
    caption="Expert-normalized returns across domains and methods.",
    label="tab:tokenization_comparison"
)

print(latex)

```
````

<img src="../../_static/images/tables/grouped_multirow_latex.png" alt="grouped_multirow_latex" style="max-width: 100%; width: auto; height: auto; max-height: 450px;">
