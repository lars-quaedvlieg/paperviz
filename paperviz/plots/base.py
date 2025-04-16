import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

# Theme registry
theme_registry = {}


def register_theme(name, example_image=None):
    def decorator(fn):
        theme_registry[name] = {
            "func": fn,
            "example_image": example_image or "",
        }

        return fn

    return decorator


@register_theme("nature", example_image="nature.png")
def nature_theme():
    return {
        "font": "Arial",
        "font_size": 14,
        "grid": False,
        "grid_style": "-",
        "grid_alpha": 0.4,
        "color_palette": "deep",
        "linewidth": 1.5,
        "style": "seaborn-v0_8-white",
        "dpi": 300,
    }


@register_theme("latex", example_image="latex.png")
def latex_theme():
    return {
        "font": "Times New Roman",
        "font_size": 18,
        "grid": True,
        "grid_style": "--",
        "grid_alpha": 0.7,
        "color_palette": "colorblind",
        "linewidth": 2.5,
        "style": "seaborn-v0_8-whitegrid",
        "dpi": 300,
    }


@register_theme("dark_latex", example_image="dark_latex.png")
def dark_latex_theme():
    return {
        "font": "Times New Roman",  # Clean monospace
        "font_size": 18,
        "grid": True,
        "grid_style": "--",
        "grid_alpha": 0.3,
        "color_palette": "dark",  # seaborn dark palette
        "linewidth": 2.5,
        "style": "dark_background",  # matplotlib built-in
        "dpi": 300,
    }


def set_style(theme="latex", **overrides):
    if theme not in theme_registry:
        raise ValueError(f"Theme '{theme}' not found. Available themes: {list(theme_registry.keys())}")

    config = theme_registry[theme]["func"]()
    config.update(overrides)

    # Apply general styles
    plt.style.use(config["style"])
    sns.set_palette(config["color_palette"])

    font = config["font"]
    font_size = config["font_size"]

    mpl.rcParams.update({
        "font.family": font,
        "axes.titlesize": font_size,
        "axes.labelsize": font_size,
        "xtick.labelsize": font_size,
        "ytick.labelsize": font_size,
        "legend.fontsize": font_size,
        "axes.grid": config["grid"],
        "grid.linestyle": config["grid_style"],
        "grid.alpha": config["grid_alpha"],
        "lines.linewidth": config["linewidth"],
        "figure.dpi": config["dpi"],
    })
