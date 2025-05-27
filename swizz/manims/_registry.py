manim_registry = {}

def register_manim(name, description=None, args=None, example_output=None, example_thumbnail=None, example_code=None):
    def wrapper(scene_class):
        manim_registry[name] = {
            "scene": scene_class,
            "description": description or "",
            "args": args or [],
            "example_output": example_output or "",
            "example_thumbnail": example_thumbnail or "",
            "example_code": example_code or "",
        }
        return scene_class
    return wrapper 