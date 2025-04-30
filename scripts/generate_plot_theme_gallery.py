import os

from swizz.plots.base import theme_registry

GALLERY_PATH = "docs/plot_themes/index.md"
DETAILS_DIR = "collection/"  # where individual md files live

CARD_TEMPLATE = """\
<div style="flex: 1 1 300px; max-width: 300px; border: 1px solid #ddd; padding: 1rem; border-radius: 0.5rem;">
  <div style="height: 180px; display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 0.5rem;">
    <a href="{details_path}">
      <img src="{img_path}" alt="{name}" style="max-height: 100%; max-width: 100%;">
    </a>
  </div>
  <h4 style="margin: 0.5rem 0;">{name}</h4>
  <p style="font-size: 0.9rem;">{short_description}</p>
</div>
"""

TEMPLATE = """\
# 🎨 Themes Overview

Swizz comes with built-in visual themes for plots, inspired by common publication styles, or dark-mode aesthetics.

Each theme controls global plot styling:
- Font and font size
- Gridlines
- Color palette
- Line thickness
- Layout spacing and more

---

## ⚙️ How to use a theme

Use `set_style` to apply a theme globally to all plots:

```python
from swizz.plot.base import set_style

# Apply a theme
set_style("latex")  # This is actually the default theme

# Optionally override specific parameters
set_style("dark_latex", font_size=20, linewidth=3)
```

You can override any valid `matplotlib.rcParams` using keyword arguments.

👉 Full list of overridable params:  
[matplotlib.rcParams reference](https://matplotlib.org/stable/api/matplotlib_configuration_api.html#matplotlib.rcParams)

---

## 🖼 Theme Previews

Browse available themes below. All plots use the same data for visual consistency.

<div style="display: flex; flex-wrap: wrap; gap: 2rem; justify-content: flex-start;">
{gallery_entries}
</div>
"""


def generate_gallery():
    entries = []

    for name, info in theme_registry.items():
        img_path = f"../_static/images/plot_themes/{info.get('example_image', f'{name}.png')}"
        description = info.get("description", "").strip().split("\n")[0]  # 1-liner
        details_path = "" # f"collection/{name}.html"

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
