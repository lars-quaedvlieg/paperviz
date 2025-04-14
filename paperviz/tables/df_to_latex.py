from ._registry import register_table
from ._utils import format_cell


@register_table(
    name="df_to_latex",
    description="Auto-computes mean ± std or stderr, bolds best values (min or max).",
    requires_latex=["\\usepackage{booktabs}", "\\usepackage{graphicx}"],
    args=[
        {"name": "df", "type": "pd.DataFrame", "required": True, "description": "DataFrame of numeric or list-like values."},
        {"name": "highlight", "type": "Dict[str, str]", "required": False, "description": "Map of column → 'min' or 'max'."},
        {"name": "stderr", "type": "bool", "required": False, "description": "Use standard error instead of std."},
        {"name": "caption", "type": "str", "required": False, "description": "LaTeX caption."},
        {"name": "label", "type": "str", "required": False, "description": "LaTeX label."}
    ]
)
def plot(df, highlight=None, stderr=False, caption=None, label=None):
    import pandas as pd

    df = df.copy()
    col_means = {}  # store means for bolding later

    # Format all numeric columns
    for col in df.columns:
        if col == "Model":
            continue
        col_means[col] = []
        new_vals = []
        for val in df[col]:
            formatted, mean = format_cell(val, stderr=stderr)
            new_vals.append(formatted)
            col_means[col].append(mean)
        df[col] = new_vals

    # Bold best values in highlight columns
    if highlight:
        for col, mode in highlight.items():
            means = col_means[col]
            if mode == "min":
                best_val = min(means)
            elif mode == "max":
                best_val = max(means)
            else:
                continue

            for i, val in enumerate(df[col]):
                if means[i] == best_val:
                    if val.startswith("$") and val.endswith("$"):
                        inner = val.strip("$")
                        df.at[i, col] = f"$\\mathbf{{{inner}}}$"
                    else:
                        df.at[i, col] = f"\\textbf{{{val}}}"

    # Assemble LaTeX table
    latex = "\\begin{table}[h]\n\\centering\n\\begin{tabular}{" + "l" * len(df.columns) + "}\n"
    latex += "\\toprule\n"
    latex += " & ".join(df.columns) + " \\\\\n\\midrule\n"
    for _, row in df.iterrows():
        latex += " & ".join(str(v) for v in row.values) + " \\\\\n"
    latex += "\\bottomrule\n\\end{tabular}\n"
    if caption:
        latex += f"\\caption{{{caption}}}\n"
    if label:
        latex += f"\\label{{{label}}}\n"
    latex += "\\end{table}"
    return latex