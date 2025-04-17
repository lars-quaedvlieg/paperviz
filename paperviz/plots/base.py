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
        "font.family": "Arial",
        "axes.titlesize": 14,
        "axes.labelsize": 14,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
        "legend.fontsize": 14,
        "legend.frameon": True,
        "legend.framealpha": 0.9,
        "legend.edgecolor": "black",
        "legend.handlelength": 1.5,
        "axes.grid": False,
        "grid.linestyle": "-",
        "grid.alpha": 0.4,
        "lines.linewidth": 1.5,
        "figure.dpi": 300,
        "style": "seaborn-v0_8-white",  # special key (we'll pop it)
        "color_palette": "deep",  # special key (same)
    }


@register_theme("latex", example_image="latex.png")
def latex_theme():
    return {
        # === Fonts ===
        "font.family": "Times New Roman",  # Classic serif font for paper aesthetics
        "font.size": 18,  # Base font size (can be overridden below)

        # === Axes ===
        "axes.labelsize": 18,  # Axis label font size
        "axes.titlesize": 18,  # Title font size
        "axes.labelpad": 6.0,  # Padding between axis and label
        "axes.labelcolor": "black",  # Label font color
        "axes.linewidth": 1.0,  # Thickness of axis borders
        "axes.grid": True,  # Enable grid by default
        "axes.grid.axis": "both",  # Grid lines for both axes
        "axes.spines.top": False,  # Hide top spine
        "axes.spines.right": False,  # Hide right spine

        # === Grid ===
        "grid.linestyle": "--",  # Dashed grid lines
        # "grid.linewidth": 0.5,  # Thin grid lines
        "grid.alpha": 0.3,  # Slight transparency
        "grid.color": "gray",  # Neutral grid color

        # === Ticks ===
        "xtick.labelsize": 16, # x-axis label size
        "ytick.labelsize": 16, # y-axis label size

        # === Figure ===
        "figure.dpi": 300,  # High-res export
        "figure.figsize": (8, 5),  # Default figure size
        "figure.facecolor": "white",  # Background for saved figures
        "figure.autolayout": True,  # Avoid overlap

        # === Lines ===
        "lines.linewidth": 2.5,  # Thicker lines for visibility
        "lines.markersize": 6,  # Reasonable default marker size

        # === Legend ===
        "legend.frameon": True,
        "legend.framealpha": 0.9,
        "legend.edgecolor": "grey",
        "legend.fontsize": 16,
        "legend.handlelength": 1.5,
        "legend.loc": "best",

        # === Style + Palette (handled outside rcParams) ===
        "style": "seaborn-v0_8-whitegrid",  # Classic whitegrid with slight polish
        "color_palette": "colorblind",  # Nice default for publication safety
    }


@register_theme("dark_latex", example_image="dark_latex.png")
def dark_latex_theme():
    return {
        "font.family": "Times New Roman",
        "axes.titlesize": 18,
        "axes.labelsize": 18,
        "xtick.labelsize": 18,
        "ytick.labelsize": 18,
        "legend.fontsize": 18,
        "legend.frameon": True,
        "legend.framealpha": 0.9,
        "legend.edgecolor": "grey",
        "legend.handlelength": 1.5,
        "axes.grid": True,
        "grid.linestyle": "--",
        "grid.alpha": 0.3,
        "lines.linewidth": 2.5,
        "figure.dpi": 300,
        "style": "dark_background",
        "color_palette": "dark",
    }


def set_style(theme="latex", **overrides):
    if theme not in theme_registry:
        raise ValueError(f"Theme '{theme}' not found. Available themes: {list(theme_registry.keys())}")

    # Reset to default
    mpl.rcParams.update(mpl.rcParamsDefault)
    plt.style.use('default')
    sns.set_palette("tab10")

    # Configs
    config = theme_registry[theme]["func"]()
    config.update(overrides)

    # Special cases (non-rcParams)
    style = config.pop("style", None)
    palette = config.pop("color_palette", None)

    if style:
        plt.style.use(style)
    if palette:
        sns.set_palette(palette)

    # Apply all rcParams
    mpl.rcParams.update(config)
