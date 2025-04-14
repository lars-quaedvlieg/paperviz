from ._registry import register_table
from ._utils import format_cell


@register_table(
    name="results_multilevel_latex",
    description="Multi-level LaTeX table with grouped blocks, hierarchical columns, and bolded best values.",
    requires_latex=["\\usepackage{graphicx}", "\\usepackage{booktabs}", "\\usepackage{xcolor}", r"\newcommand{\highlightcolor}[1]{\colorbox[HTML]{bae6fb}{\textbf{#1}}}"],
    args=[
        {"name": "df", "type": "pd.DataFrame", "required": True, "description": "Long-format data with values + metadata."},
        {"name": "row_index", "type": "str", "required": True, "description": "Column to use as row index (e.g., 'Model')."},
        {"name": "col_index", "type": "List[str]", "required": True, "description": "Two columns to form hierarchical columns (e.g., ['Split', 'Budget'])."},
        {"name": "groupby", "type": "str", "required": True, "description": "Column to group subtables (e.g., 'Task')."},
        {"name": "value_column", "type": "str", "required": True, "description": "Column with list/float values to format."},
        {"name": "highlight", "type": "str", "required": False, "description": "'min' or 'max' to bold best values in each column."},
        {"name": "stderr", "type": "bool", "required": False, "description": "Use standard error instead of std."},
        {"name": "caption", "type": "str", "required": False, "description": "LaTeX caption."},
        {"name": "label", "type": "str", "required": False, "description": "LaTeX label."}
    ]
)
def plot(
    df,
    row_index,
    col_index,
    groupby,
    value_column,
    highlight="min",
    stderr=False,
    caption=None,
    label=None
):
    assert len(col_index) == 2, "col_index must have exactly two elements."

    # Pivot once
    pivot = df.pivot_table(
        index=[groupby, row_index],
        columns=col_index,
        values=value_column,
        aggfunc=lambda x: list(x)[0]  # Assumes each (row, col) has a single value
    )

    pivot = pivot.sort_index(axis=1, level=0)
    pivot = pivot.sort_index()  # Sort by group and model

    formatted = pivot.copy()
    means = {}

    # Format all cells and collect means for highlight
    for col in pivot.columns:
        col_idx = pivot.columns.get_loc(col)
        means[col] = []
        for i, val in enumerate(pivot[col]):
            formatted_val, numeric_val = format_cell(val, stderr=stderr)
            formatted.iloc[i, col_idx] = formatted_val
            means[col].append(numeric_val)

    # Highlighting per task (group)
    if highlight in ("min", "max"):
        for group_name, group_df in formatted.groupby(level=0):
            row_indices = group_df.index  # MultiIndex tuples
            for col in pivot.columns:
                col_idx = formatted.columns.get_loc(col)
                col_vals = [means[col][formatted.index.get_loc(idx)] for idx in row_indices]
                best = min(col_vals) if highlight == "min" else max(col_vals)
                for idx, val in zip(row_indices, group_df[col]):
                    i = formatted.index.get_loc(idx)
                    if means[col][i] == best:
                        if val.startswith("$") and val.endswith("$"):
                            inner = val.strip("$")
                            formatted.iloc[i, col_idx] = f"$\\mathbf{{{inner}}}$"
                        else:
                            formatted.iloc[i, col_idx] = f"\\textbf{{{val}}}"
                        formatted.iloc[i, col_idx] = f"\highlightcolor{{{formatted.iloc[i, col_idx]}}}"

    # Start building LaTeX
    latex = "\\begin{table*}[!ht]\n\\begin{center}\n\\resizebox{\\textwidth}{!}{\n"
    latex += "  \\begin{small}\n  \\begin{sc}\n"

    num_cols = 1 + len(pivot.columns)
    latex += f"  \\begin{{tabular}}{{{'l' + 'c' * (num_cols - 1)}}}\n"
    latex += "  \\toprule\n"

    # First-level headers (e.g. Validation, Test)
    level1 = list(dict.fromkeys([col[0] for col in pivot.columns]))
    level2_per_level1 = {
        l1: [col[1] for col in pivot.columns if col[0] == l1] for l1 in level1
    }

    latex += "  " + " & ".join([""] + [f"\\multicolumn{{{len(level2_per_level1[l1])}}}{{c}}{{{l1}}}" for l1 in level1]) + " \\\\\n"

    # cmidrules
    offset = 1
    for l1 in level1:
        span = len(level2_per_level1[l1])
        latex += f"  \\cmidrule(lr){{{offset+1}-{offset+span}}} "
        offset += span
    latex += "\n"

    # Second-level headers (e.g. 9.6k, 16k, 22.4k)
    latex += "  " + " & ".join([""] + [sub for _, sub in pivot.columns]) + " \\\\\n"
    latex += "  \\midrule\n"

    # Now write rows per group (e.g. Task)
    grouped = formatted.groupby(level=0)
    for group_name, group_df in grouped:
        latex += f"  \\multicolumn{{{num_cols}}}{{c}}{{\\hspace{{3.5cm}}\\textbf{{{group_name}}}}} \\\\\n"
        latex += "  \\midrule\n  \\midrule\n"
        for (_, model), row in group_df.iterrows():
            latex += "  " + " & ".join([model] + list(row.values)) + " \\\\\n"
        latex += "  \\midrule\n"

    latex += "  \\bottomrule\n"
    latex += "  \\end{tabular}\n  \\end{sc}\n  \\end{small}\n}\n\\end{center}\n"

    if caption:
        latex += f"\\caption{{{caption}}}\n"
    if label:
        latex += f"\\label{{{label}}}\n"
    latex += "\\end{table*}"

    return latex