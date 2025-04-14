# 📄📊 paperviz

**Paperviz** is a Python library for generating **publication-ready visualizations**, **LaTeX tables**, and **subfigure layouts** with minimal code and consistent style.

Built for AI/ML researchers, it's designed to make NeurIPS/ICLR/CVPR-style figures effortless — no more LaTeX hacks, pixel wrangling, or style mismatches. Focus on your results, not your rendering.

---

## 🚀 Features

- 📊 One-liner **plotting functions**
- 🧾 Auto-generated **LaTeX table code** from pandas DataFrames
- 🧩 Easy **layout builders** for stacked, grid, and subfigure formats
- ⚙️ Table export from **Hydra/OmegaConf** configs and experiment logs
- 🧠 Unified **style system** (fonts, sizes, spacing)
- 📚 **Jupyter Book** documentation with live examples

---

## 🧪 Examples

**Simple LaTeX table from lists:**
```python
from paperviz.table import table
import pandas as pd

df = pd.DataFrame({
    "Model": ["A", "B"],
    "acc": [[0.85, 0.88, 0.87], [0.90, 0.91, 0.89]],
    "f1": [[0.83, 0.83, 0.83], [0.92, 0.93, 0.93]],
})

latex_string = table(
    "results_latex",
    df,
    highlight={"acc": "max", "f1": "min"},
    stderr=True,
    caption="CIFAR-10 results",
    label="tab:cifar10"
)
```
![Simple Table](docs/_static/images/table/simple_df_to_latex.png)

**Grouped 4-level index table:**
```python
from paperviz.table import table

complex_df = ...

latex_string = table(
    "results_multilevel_latex",
    df=complex_df,
    row_index="Model",
    col_index=["Split", "Budget"],
    groupby="Task",
    value_column="score",
    highlight="min",
    stderr=True,
    caption="Combinatorial optimization results",
    label="tab:combo_results"
)
```
![Complex Table](docs/_static/images/table/grouped_multicol_latex.png)

---

## 📦 Installation

```bash
pip install paperviz
```

(Coming soon to PyPI)

---

## 📚 Documentation

We're building a full [Jupyter Book site](https://your-link-here.com) with:
- 📊 Plotting gallery
- 📐 Layout + subfigure examples
- 🧾 Table demos with config
- 📎 LaTeX integration guides

---

## 📁 Project Structure

| Module       | Description |
|--------------|-------------|
| `paperviz.table`  | Table generators |
| `paperviz.plot`   | Plotting utilities built on Seaborn & Matplotlib |
| `paperviz.layout` | Layout builders for stacked / side-by-side images |
| `paperviz.utils`  | Formatters, LaTeX helpers, config exporters |

---

## 🛠️ Roadmap

- [ ] Add plot types (confusion, UMAP, attention, histograms)
- [ ] Themes: `"neurips"`, `"nature"`, `"cvpr"`, ...
- [ ] LaTeX PDF + PNG export
- [ ] W&B / MLflow integration
- [ ] Citation cards / figure references

---

## 🤝 Contributing

Contributions are very welcome! See `CONTRIBUTING.md` (coming soon) for setup and module structure.

---
