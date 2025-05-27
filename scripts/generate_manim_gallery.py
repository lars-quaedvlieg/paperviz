import os

from swizz.manims._registry import manim_registry

GALLERY_PATH = "docs/manim/index.md"
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
# 🎬 Manim Animations

Welcome to the Manim animations section! Here you'll find a collection of pre-built animations for visualizing code evolution, algorithms, and more. Each animation is designed to be easily customizable and ready to use in your presentations or documentation.

## 🎥 Available Animations

Browse our collection of Manim animations below. Click on any preview to see detailed usage instructions and examples.

The Manim renderer provides extensive configuration options for customizing your animations. For advanced settings, refer to the [Manim documentation](https://docs.manim.community/en/stable/reference/manim._config.utils.ManimConfig.html).
<div style="display: flex; flex-wrap: wrap; gap: 2rem; justify-content: flex-start;">
{gallery_entries}
</div>
"""


def generate_gallery():
    entries = []

    for name, info in manim_registry.items():
        img_path = f"../_static/images/manim/{info.get('example_thumbnail', f'manim/{name}.png')}"
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
