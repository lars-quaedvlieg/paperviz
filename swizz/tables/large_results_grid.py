from swizz.tables._registry import register_table
from swizz.utils.table import format_cell

@register_table(
    name="grouped_multicol_latex",
    description=(
        "Render a grouped LaTeX table with hierarchical column headers.\n"
        "- The DataFrame must contain:\n"
        "  - A row label column (e.g., 'Model')\n"
        "  - Two columns for column grouping (e.g., 'Split', 'Budget')\n"
        "  - A grouping column for row-wise subtables (e.g., 'Task')\n"
        "  - A value column, which can be:\n"
        "      – a float (e.g., 0.92)\n"
        "      – or a list of floats (e.g., [0.91, 0.93, 0.92])\n"
        "- Automatically computes mean ± std or stderr\n"
        "- Highlights best values (min or max) per column *within each group*\n"
    ),
    requires_latex=[r"\usepackage{booktabs}", r"\usepackage{scalefnt}", r"\newcommand{\highlightcolor}[1]{\colorbox[HTML]{bae6fb}{\textbf{#1}}}"],
    args=[
        {"name": "df", "type": "pd.DataFrame", "required": True, "description": "DataFrame with row and column metadata + values. Must include all column names passed below."},
        {"name": "row_index", "type": "str", "required": True, "description": "Name of the column to use for the leftmost index (e.g., 'Model')."},
        {"name": "col_index", "type": "List[str]", "required": True, "description": "Two column names to create multi-level column headers (e.g., ['Split', 'Budget'])."},
        {"name": "groupby", "type": "str", "required": True, "description": "Column used to group subtables (e.g., 'Task')."},
        {"name": "value_column", "type": "str", "required": True, "description": "Column containing scalar or list-like values to format."},
        {"name": "highlight", "type": "str", "required": False, "description": "'min' or 'max' to bold best values per column within each group."},
        {"name": "stderr", "type": "bool", "required": False, "description": "Use standard error instead of std deviation."},
        {"name": "caption", "type": "str", "required": False, "description": "Optional LaTeX caption added below the table."},
        {"name": "label", "type": "str", "required": False, "description": "Optional LaTeX label for referencing."}
    ],
    example_image="grouped_multicol_latex.png",
    example_code="grouped_multicol_latex.py"
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