import os

from swizz.plots._registry import plot_registry
from swizz.tables._registry import table_registry
from swizz.manims._registry import manim_registry

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
        "  - file: plots/index",
        "    sections:"
    ])

    # Generate section entries for each table
    for name in sorted(plot_registry.keys()):
        toc_lines.append(f"      - file: plots/collection/{name}")

    toc_lines.extend([
        "  - file: layout/index",
        "    sections:",
        "      - file: layout/built-in-layouts"
    ])

    toc_lines.extend([
        "  - file: plot_themes/index",
        "  - file: manim/index",
        "    sections:",
    ])

    # Generate section entries for each table
    for name in sorted(manim_registry.keys()):
        toc_lines.append(f"      - file: manim/collection/{name}")

    toc_lines.extend([
        "  - file: logging/index",
    ])

    # Write to file
    with open(TOC_PATH, "w") as f:
        f.write("\n".join(toc_lines))

    print(f"✅ TOC written to {TOC_PATH}")


if __name__ == "__main__":
    generate_toc()
