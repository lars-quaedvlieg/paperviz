table_registry = {}


def register_table(name, description=None, requires_latex=None, args=None, example_image=None, example_code=None):
    def wrapper(func):
        table_registry[name] = {
            "func": func,
            "description": description or "",
            "requires_latex": requires_latex or [],
            "args": args or [],
            "example_image": example_image or "",
            "example_code": example_code or "",
        }
        return func

    return wrapper
