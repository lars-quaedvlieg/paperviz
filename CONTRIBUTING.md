# 🤝 Contributing to paperviz

Thanks for your interest in contributing to **paperviz**! This project aims to make **beautiful, publication-quality figures and LaTeX outputs** as effortless as possible for researchers.

Whether you're fixing a bug, adding a table format, improving docs, or building new layouts — you're very welcome here.

---

## 🧱 Repository Structure

| Folder                  | Purpose                                                           |
|--------------------------|-------------------------------------------------------------------|
| `paperviz/table/`        | Table generators                                                  |
| `paperviz/plot/`         | [COMING SOON] Plotting utilities (Seaborn + Matplotlib wrappers)  |
| `paperviz/layout/`       | [COMING SOON] Layout builders for subfigures, grids, side-by-side |
| `paperviz/utils/`        | [COMING SOON] Formatters, math helpers, config exports            |
| `docs/`                  | Jupyter Book examples and usage guides                            |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone git@github.com:lars-quaedvlieg/paperviz.git
cd paperviz
```

### 2. Set up the environment

We recommend using `venv` or `conda`.

```bash
pip install -e .
```

---

## ✅ What You Can Work On

- 📊 Add new table formats (`paperviz/table/`)
- 🖼️ Add plot utilities with unified style (`paperviz/plot/`)
- 🧩 Create layout presets (`paperviz/layout/`)
- 🐛 Fix issues or formatting bugs

### Adding a New Table

If you're adding a new table function:

1. Create a file in `paperviz/table/yourfile.py`
2. Register it with the `@register_table` decorator
3. Fill out all the information inside the decorator arguments. For a good example of this, see below.
4. Create an example script for this table, focusing on the input format, and put it inside of `docs/_static/snippets/tables`.
5. Paste the example output into LaTeX and render the table. Put a picture of this table inside `docs/_static/images/tables`.

The codebase will then automatically detect when a new table has been registered, meaning it can be used in the `paperviz.table` method.

The snippet and output image are automatically compiled into the documentation website, so you do not have to edit the docs! This adding new tables super simple!

Example of the `@register_table` decorator:
```python
@register_table(
    name="simple_df_to_latex",
    description=(
            "Render a simple LaTeX table from a flat DataFrame.\n"
            "- First column (e.g., 'Model') is treated as the row label\n"
            "- Other columns contain either scalars or list-like values (e.g. [0.82, 0.84, 0.85])\n"
            "- Automatically formats values as mean ± std or stderr\n"
            "- Optionally highlights best values per column (min or max)"
    ),
    requires_latex=["\\usepackage{booktabs}"],
    args=[
        {"name": "df", "type": "pd.DataFrame", "required": True,
         "description": "DataFrame where the first column is a string label (e.g., 'Model') and other columns are scalars or list-like numeric values."},
        {"name": "highlight", "type": "Dict[str, str]", "required": False,
         "description": "Map of column → 'min' or 'max' to bold the best values."},
        {"name": "stderr", "type": "bool", "required": False,
         "description": "Use standard error (instead of std) for ± formatting."},
        {"name": "caption", "type": "str", "required": False,
         "description": "Optional caption to display below the table."},
        {"name": "label", "type": "str", "required": False, "description": "Optional LaTeX label for referencing."}
    ],
    example_image="simple_df_to_latex.png",
    example_code="simple_df_to_latex.py"
)
```

---

## 📬 Submitting a Pull Request

In order to push your changes from your local to this repository, follow these general steps:

1. Fork the repo
2. Create a new branch: `feature/new-table` or `fix/highlight-bug`
3. Make your changes
4Open a pull request and describe what you changed

---

## ❤️ Acknowledgements

Paperviz is made by researchers, for researchers. Thank you for helping improve it — every contribution counts!
