table_registry = {}


def register_table(name, description=None, requires_latex=None, args=None):
    def wrapper(func):
        table_registry[name] = {
            "func": func,
            "description": description or "",
            "requires_latex": requires_latex or [],
            "args": args or [],
        }
        return func

    return wrapper
