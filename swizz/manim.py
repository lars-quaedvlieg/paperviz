from swizz.manims._registry import manim_registry
from manim import tempconfig
import os

def render_manim(name, render_config=None, *args, **kwargs):
    """Render a registered Manim scene by name and config."""
    
    if name not in manim_registry:
        raise ValueError(f"Manim scene '{name}' not found.")
    
    scene_class = manim_registry[name]["scene"]
    scene_to_render = scene_class(*args, **kwargs)

    # Merge default config with render_config
    default_render_config = {
        "quality": "high_quality",
        "format": "mp4",
    }
    render_config = {**default_render_config, **render_config}

    # This can be any setting in ManimConfig 
    with tempconfig(render_config):
        scene_to_render.render()

def available_manim_scenes():
    """Return a list of all available Manim scenes."""
    return list(manim_registry.keys())