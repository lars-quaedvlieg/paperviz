from swizz.tables._registry import register_table
from swizz.utils.table import format_cell


@register_table(
    name="grouped_multirow_latex",
    description=(
            "Render a grouped LaTeX table with two-level row headers (e.g., Domain and Task) and "
            "flat method columns (e.g., MLP, Modality, Component).\n- Input must be a flat DataFrame with "
            "(row1, row2, column, value) format.\n- Each value should be a float or a list of floats, from which "
            "mean ± std or stderr is computed.\n- Bolds the best (min or max) per row."
    ),
    requires_latex=["\\usepackage{booktabs}", "\\usepackage{multirow}",
                    r"\newcommand{\highlightcolor}[1]{\colorbox[HTML]{bae6fb}{\textbf{#1}}}"],
    args=[
        {"name": "df", "type": "pd.DataFrame", "required": True,
         "description": "DataFrame with columns for row1, row2, column, and values (as lists or floats)."},
        {"name": "row1", "type": "str", "required": True,
         "description": "Column name for the outer row grouping (e.g., Domain)."},
        {"name": "row2", "type": "str", "required": True, "description": "Column name for the row label (e.g., Task)."},
        {"name": "col", "type": "str", "required": True,
         "description": "Column name representing the method axis (e.g., Method)."},
        {"name": "value_column", "type": "str", "required": True,
         "description": "Column name containing scalar or list-of-floats to summarize."},
        {"name": "highlight", "type": "str", "required": False,
         "description": "'min' or 'max' to bold best value per row."},
        {"name": "stderr", "type": "bool", "required": False,
         "description": "Use standard error instead of std when formatting."},
        {"name": "caption", "type": "str", "required": False,
         "description": "LaTeX caption to display below the table."},
        {"name": "label", "type": "str", "required": False, "description": "Optional LaTeX label for referencing."}
    ],
    example_image="grouped_multirow_latex.png",
    example_code="grouped_multirow_latex.py"
)
def plot(df, row1, row2, col, value_column, highlight="max", stderr=False, caption=None, label=None):
    # Pivot into MultiIndex rows, columns = method
    pivot = df.pivot_table(
        index=[row1, row2],
        columns=col,
        values=value_column,
        aggfunc=lambda x: list(x)[0]  # assumes unique per (row1, row2, col)
    ).copy()

    formatted = pivot.copy()
    means = {}

    for method in pivot.columns:
        means[method] = []
        for i, val in enumerate(pivot[method]):
            formatted_val, numeric_val = format_cell(val, stderr=stderr)
            formatted.iloc[i, formatted.columns.get_loc(method)] = formatted_val
            means[method].append(numeric_val)

    # Highlighting (per row)
    if highlight in ("min", "max"):
        for i in range(len(formatted)):
            vals = [means[col][i] for col in pivot.columns]
            best_val = min(vals) if highlight == "min" else max(vals)
            for j, col in enumerate(pivot.columns):
                cell = formatted.iloc[i, j]
                if means[col][i] == best_val:
                    if cell.startswith("$") and cell.endswith("$"):
                        inner = cell.strip("$")
                        formatted.iloc[i, j] = f"$\\mathbf{{{inner}}}$"
                    else:
                        formatted.iloc[i, j] = f"$\\mathbf{{{cell}}}$"
                    formatted.iloc[i, j] = f"\highlightcolor{{{formatted.iloc[i, j]}}}"

    # Start LaTeX
    latex = "\\renewcommand{\\arraystretch}{1.15}\n\\begin{table}[t!]\n\\centering\n\\footnotesize\n"
    if caption:
        latex += f"\\caption{{{caption}}}\n"
    if label:
        latex += f"\\label{{{label}}}\n"
    latex += "\\resizebox{\\textwidth}{!}{%\n\\begin{tabular}{cl" + "c" * len(pivot.columns) + "}\n\\toprule\n"
    latex += f"{{{row1}}} & \\multicolumn{{1}}{{c}}{{{row2}}} & " + " & ".join(
        pivot.columns) + " \\\\\n\\midrule\n\\midrule\n"

    grouped = formatted.groupby(level=0)
    for domain, group_df in grouped:
        latex += f"\\multirow{{{len(group_df)}}}{{*}}{{\\textbf{{{domain}}}}} "
        for i, ((_, task), row) in enumerate(group_df.iterrows()):
            if i > 0:
                latex += " & "
            else:
                latex += "& "
            latex += f"{task} & " + " & ".join(row.values) + " \\\\\n"
        latex += "\\midrule\n"

    latex += "\\bottomrule\n\\end{tabular}%\n}\n\\end{table}\n\\renewcommand{\\arraystretch}{1}"
    return latex
