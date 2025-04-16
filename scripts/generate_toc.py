import os

from paperviz.plots._registry import plot_registry
from paperviz.tables._registry import table_registry

TOC_PATH = "docs/_toc.yml"

def generate_toc():
    toc_lines = [
        "format: jb-book",
        "root: intro",
        "",
        "chapters:",
        "  - file: tables/index",
        "    sections:"
    ]

    # Generate section entries for each table
    for name in sorted(table_registry.keys()):
        toc_lines.append(f"      - file: tables/collection/{name}")

    toc_lines.extend([
        "  - file: plot_themes/index",
        "  - file: plots/index",
        "    sections:"
    ])

    # Generate section entries for each table
    for name in sorted(plot_registry.keys()):
        toc_lines.append(f"      - file: plots/collection/{name}")

    # Write to file
    with open(TOC_PATH, "w") as f:
        f.write("\n".join(toc_lines))

    print(f"✅ TOC written to {TOC_PATH}")

if __name__ == "__main__":
    generate_toc()
