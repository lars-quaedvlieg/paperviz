# `simple_df_to_latex`

> Render a simple LaTeX table from a flat DataFrame.
> - First column (e.g., 'Model') is treated as the row label
> - Other columns contain either scalars or list-like values (e.g. [0.82, 0.84, 0.85])
> - Automatically formats values as mean ± std or stderr
> - Optionally highlights best values per column (min or max)

---

## 🧾 Required LaTeX packages / commands

- `\usepackage{booktabs}`


---

## 📥 Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| df | pd.DataFrame | ✅ | DataFrame where the first column is a string label (e.g., 'Model') and other columns are scalars or list-like numeric values. |
| highlight | Dict[str, str] | ❌ | Map of column → 'min' or 'max' to bold the best values. |
| stderr | bool | ❌ | Use standard error (instead of std) for ± formatting. |
| caption | str | ❌ | Optional caption to display below the table. |
| label | str | ❌ | Optional LaTeX label for referencing. |

---

## 📦 Example Output

````{dropdown} Click to show example code
```python
# Example code for |simple_df_to_latex| not found.
```
````

<img src="../../_static/images/tables/simple_df_to_latex.png" alt="simple_df_to_latex" style="max-width: 100%; width: auto; height: auto; max-height: 450px;">
