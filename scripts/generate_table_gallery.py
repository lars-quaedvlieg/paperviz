import os
from paperviz.tables._registry import table_registry

GALLERY_PATH = "docs/tables/index.md"
DETAILS_DIR = "collection/"  # where individual md files live

CARD_TEMPLATE = """\
<div style="flex: 1 1 300px; max-width: 300px; border: 1px solid #ddd; padding: 1rem; border-radius: 0.5rem;">
  <div style="height: 180px; display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 0.5rem;">
    <a href="{details_path}">
      <img src="{img_path}" alt="{name}" style="max-height: 100%; max-width: 100%;">
    </a>
  </div>
  <h4 style="margin: 0.5rem 0;"><a href="{details_path}">{name}</a></h4>
  <p style="font-size: 0.9rem;">{short_description}</p>
</div>
"""

TEMPLATE = """\
# 📊 Table Formats

Browse available LaTeX table styles. Click a preview to see full usage, arguments, and output.

<div style="display: flex; flex-wrap: wrap; gap: 2rem; justify-content: flex-start;">
{gallery_entries}
</div>
"""


def generate_gallery():
    entries = []

    for name, info in table_registry.items():
        img_path = f"../_images/{info.get('example_image', f'tables/{name}.png')}"
        description = info.get("description", "").strip().split("\n")[0]  # 1-liner
        details_path = f"collection/{name}.html"

        entry = CARD_TEMPLATE.format(
            name=name,
            img_path=img_path,
            short_description=description,
            details_path=details_path,
        )
        entries.append(entry)

    with open(GALLERY_PATH, "w") as f:
        f.write(TEMPLATE.format(gallery_entries="\n".join(entries)))

    print(f"✅ Gallery (grid view) written to {GALLERY_PATH}")


if __name__ == '__main__':
    generate_gallery()
