from swizz.layouts._registry import layout_registry


def layout(name, *args, **kwargs):
    if name not in layout_registry:
        raise ValueError(f"Table '{name}' not found.")
    return layout_registry[name]["func"](*args, **kwargs)


def available_layouts():
    return list(layout_registry.keys())
