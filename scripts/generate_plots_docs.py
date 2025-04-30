import os

from swizz.plots._registry import plot_registry

DOCS_DIR = "docs/plots/collection"
IMG_DIR = "res/images/plots"
CODE_DIR = "res/snippets/plots"

TEMPLATE = """\
# `{name}`

> {description}

---

## 📥 Arguments

{args_section}

---

## 📦 Example Output

````{{dropdown}} Click to show example code
```python
{code_contents}
```
````

<img src="{image_path}" alt="{name}" style="max-width: 100%; width: auto; height: auto; max-height: 450px;">
"""


def to_arg_table(args):
    if not args:
        return "_No arguments._"
    lines = ["| Name | Type | Required | Description |", "|------|------|----------|-------------|"]
    for arg in args:
        lines.append(
            f"| {arg['name']} | {arg['type']} | {'✅' if arg['required'] else '❌'} | {arg['description']} |"
        )
    return "\n".join(lines)


def generate_docs():
    os.makedirs(DOCS_DIR, exist_ok=True)

    for name, info in plot_registry.items():
        description = info.get("description", "").replace("\n", "\n> ")
        args_section = to_arg_table(info.get("args", []))

        img_path = f"../../_static/images/plots/{info.get('example_image', f'{name}.png')}"
        code_path = f'docs/_static/snippets/plots/{info.get("example_code", f"{name}.py")}'

        # Load code
        code_contents = ""
        if os.path.exists(code_path):
            with open(code_path, "r") as f:
                code_contents = f.read()
        else:
            code_contents = f"# Example code for `{name}` not found."

        # Create markdown
        out_path = os.path.join(DOCS_DIR, f"{name}.md")
        with open(out_path, "w") as f:
            f.write(TEMPLATE.format(
                name=name,
                description=description,
                args_section=args_section,
                image_path=img_path,
                code_contents=code_contents.replace("`", "|")
            ))

        print(f"✅ Generated docs for: {name}")


if __name__ == "__main__":
    generate_docs()
