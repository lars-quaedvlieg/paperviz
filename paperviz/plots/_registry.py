plot_registry = {}


def register_plot(name, description=None, args=None, example_image=None, example_code=None):
    def wrapper(func):
        plot_registry[name] = {
            "func": func,
            "description": description or "",
            "args": args or [],
            "example_image": example_image or "",
            "example_code": example_code or "",
        }
        return func

    return wrapper
