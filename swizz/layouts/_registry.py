layout_registry = {}

def register_layout(name=None, description=""):
    def wrapper(fn):
        layout_registry[name or fn.__name__] = {
            "func": fn,
            "description": description
        }
        return fn
    return wrapper