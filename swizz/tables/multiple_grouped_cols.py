from swizz.tables._registry import register_table
import pandas as pd


@register_table(
    name="multiple_grouped_cols",
    description=(
        "Render a grouped LaTeX table with multi-level column headers.\n"
        "- Data is passed in flat format and pivoted internally\n"
        "- Row identifiers (e.g. Corpus, Size) are passed via `row_labels`\n"
        "- Column grouping and subcolumns (e.g. 'English Benchmarks → GSM8K') inferred from `col_groups` and `col_subgroups`\n"
        "- Optionally bold the last row (e.g. final model)\n"
        "- Values are auto-formatted as percentages unless already formatted"
    ),
    requires_latex=[
        "\\usepackage{booktabs}",
        "\\usepackage{multirow}",
        "\\usepackage{adjustbox}"
        "\\usepackage{makecell}"
    ],
    args=[
        {"name": "df", "type": "pd.DataFrame", "required": True,
         "description": "Flat-format DataFrame with rows like [Corpus, Size, Group, Subtask, Score]."},
        {"name": "row_labels", "type": "List[str]", "required": True,
         "description": "Which columns to use for row identification (e.g. ['Math Corpus', 'Size'])."},
        {"name": "col_groups", "type": "str", "required": True,
         "description": "Column name used for the top-level column group (e.g. 'Group')."},
        {"name": "col_subgroups", "type": "str", "required": True,
         "description": "Column name used for the sub-columns within each group (e.g. 'Task')."},
        {"name": "value_column", "type": "str", "required": True,
         "description": "Name of the column containing values to display (e.g. 'Score')."},
        {"name": "highlight_last_row", "type": "bool", "required": False,
         "description": "Whether to bold the last row in the table."},
        {"name": "caption", "type": "str", "required": False,
         "description": "Optional caption to display below the table."},
        {"name": "label", "type": "str", "required": False,
         "description": "Optional LaTeX label for referencing in text."}
    ],
    example_image="multiple_grouped_cols.png",
    example_code="multiple_grouped_cols.py"
)
def plot(
    df: pd.DataFrame,
    row_labels,
    col_group,
    col_subgroup,
    value_column,
    highlight_last_row=True,
    caption=None,
    label=None
):
    df = df.copy()

    # Pivot the flat dataframe
    df_pivot = df.pivot_table(
        index=row_labels,
        columns=[col_group, col_subgroup],
        values=value_column,
        aggfunc="first"
    )

    # Format numeric values as percentages if not already formatted
    def format_val(x):
        if isinstance(x, (float, int)) and not isinstance(x, bool):
            return f"{x:.1f}\\%"
        return x

    df_pivot = df_pivot.applymap(format_val)

    if highlight_last_row:
        df_pivot.iloc[-1] = df_pivot.iloc[-1].map(lambda v: f"\\textbf{{{v}}}")

    top_headers = df_pivot.columns.get_level_values(0)
    sub_headers = df_pivot.columns.get_level_values(1)

    latex = "\\setlength{\\tabcolsep}{3pt}\\renewcommand{\\arraystretch}{1.15}\n\\begin{table*}[h]\n\\centering\n\\adjustbox{max width=\\textwidth}{%\n"
    latex += f"\\begin{{tabular}}{{{'l' * len(row_labels)}{'c' * len(df_pivot.columns)}}}\n"
    latex += "\\toprule\n"

    # Top-level header row
    top_line = " & " * len(row_labels)
    for group in top_headers.unique():
        count = sum(top_headers == group)
        top_line += f"\\multicolumn{{{count}}}{{c}}{{{group}}} & "
    latex += top_line.rstrip("& ") + " \\\\\n"

    # Midrules between column groups
    cursor = len(row_labels) + 1
    for group in top_headers.unique():
        count = sum(top_headers == group)
        latex += f"\\cmidrule(lr){{{cursor}-{cursor + count - 1}}}\n"
        cursor += count

    # Sub-header row
    latex += " & ".join([fr"\makecell{{{label}}}" for label in row_labels + list(sub_headers)]) + " \\\\\n\\midrule\n"

    # Data rows
    for idx, row in df_pivot.iterrows():
        idx = (idx,) if not isinstance(idx, tuple) else idx
        row_str = " & ".join(idx + tuple(str(v) for v in row.values))
        latex += row_str + " \\\\\n"

    latex += "\\bottomrule\n\\end{tabular}%\n}\n"
    if caption:
        latex += f"\\caption{{{caption}}}\n"
    if label:
        latex += f"\\label{{{label}}}\n"
    latex += "\\end{table*}\n\\renewcommand{\\arraystretch}{1}\n\\setlength{\\tabcolsep}{6pt}"

    return latex
