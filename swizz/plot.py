from swizz.plots._registry import plot_registry


def plot(name, *args, **kwargs):
    if name not in plot_registry:
        raise ValueError(f"Plot '{name}' not found.")
    return plot_registry[name]["func"](*args, **kwargs)

def available_plots():
    return list(plot_registry.keys())
