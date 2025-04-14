import os
from paperviz.tables._registry import table_registry

DOCS_DIR = "docs/tables/collection"
IMG_DIR = "res/images/tables"
CODE_DIR = "res/snippets/tables"

TEMPLATE = """\
# `{name}`

> {description}

---

## 🧾 Required LaTeX packages / commands

{latex_packages}

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

    for name, info in table_registry.items():
        description = info.get("description", "").replace("\n", "\n> ")
        args_section = to_arg_table(info.get("args", []))
        latex_packages = "".join([f"- `{pkg}`\n" for pkg in info.get("requires_latex", [])]) or "- _None_"

        img_path = f"../../_images/{info.get('example_image', f'tables/{name}.png')}"
        code_path = f'docs/res/snippets/tables/{info.get("example_code", f"tables/{name}.py")}'

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
                latex_packages=latex_packages,
                args_section=args_section,
                image_path=img_path,
                code_contents=code_contents.replace("`", "|")
            ))

        print(f"✅ Generated docs for: {name}")

if __name__ == "__main__":
    generate_docs()