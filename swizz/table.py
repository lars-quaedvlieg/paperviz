from swizz.tables._registry import table_registry


def table(name, *args, **kwargs):
    if name not in table_registry:
        raise ValueError(f"Table '{name}' not found.")
    return table_registry[name]["func"](*args, **kwargs)


def table_info(name):
    if name not in table_registry:
        raise ValueError(f"Table '{name}' not found.")
    return {
        "description": table_registry[name]["description"],
        "requires_latex": table_registry[name]["requires_latex"],
        "args": table_registry[name]["args"]
    }


def print_table_info(name):
    info = table_info(name)

    print(f"🧾 Table: {name}")
    print(f"\t📄 Description:\n\t{info['description']}")

    if info["requires_latex"]:
        print(f"\n\t📦 Requires LaTeX packages / commands:")
        for pkg in info["requires_latex"]:
            print(f"\t- {pkg}")
    else:
        print("\n\t📦 Requires LaTeX packages: None")

    if info["args"]:
        print(f"\n\t🧩 Arguments:")
        for arg in info["args"]:
            required = "✅" if arg.get("required", False) else "❌"
            print(f"\t- {arg['name']} ({arg['type']}) [{required}]: {arg['description']}")
    else:
        print("\n\t🧩 Arguments: None")

    print()


def available_tables():
    return list(table_registry.keys())
