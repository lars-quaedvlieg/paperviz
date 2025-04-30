from swizz.plots._registry import register_plot

import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

from mpl_toolkits.axes_grid1.inset_locator import inset_axes

@register_plot(
    name="embedding_2d_plot",
    description="Plot a 2D embedding (e.g., t-SNE, PCA, UMAP) colored by categorical groups or continuous values, with optional density contours, legends, and colorbars.",
    args=[
        {"name": "df", "type": "pd.DataFrame", "required": True, "description": "DataFrame containing at least 'x', 'y', and the hue column."},
        {"name": "font_family", "type": "str", "required": False, "description": "Font family for title, legend, and colorbar. Default: 'Times New Roman'."},
        {"name": "title", "type": "str", "required": False, "description": "Title for the plot. Default: None."},
        {"name": "mode", "type": "str", "required": False, "description": "Plotting mode: 'categorical' or 'continuous'. Default: 'categorical'."},
        {"name": "hue_column", "type": "str", "required": False, "description": "Column name for coloring points. Must be provided."},
        {"name": "palette", "type": "List[str]", "required": False, "description": "List of colors for categorical groups. If None, uses seaborn 'tab20' palette."},
        {"name": "cmap_continuous", "type": "str", "required": False, "description": "Matplotlib colormap name for continuous values. Default: 'viridis'."},
        {"name": "display_legend", "type": "bool", "required": False, "description": "Whether to display the legend (categorical mode only). Default: False."},
        {"name": "legend_loc", "type": "str", "required": False, "description": "Legend location if displayed. Default: 'lower right'."},
        {"name": "display_cbar", "type": "bool", "required": False, "description": "Whether to display the colorbar (continuous mode only). Default: False."},
        {"name": "cbar_loc", "type": "str", "required": False, "description": "Colorbar inset location if displayed. Default: 'lower right'."},
        {"name": "show_density", "type": "bool", "required": False, "description": "Whether to overlay density contours (continuous mode only). Default: False."},
        {"name": "density_column", "type": "str", "required": False, "description": "Column to use for density grouping. Default: 'island' if exists."},
        {"name": "density_alpha", "type": "float", "required": False, "description": "Transparency for density contours. Default: 0.5."},
        {"name": "figsize", "type": "tuple", "required": False, "description": "Figure size in inches. Default: (8, 8)."},
        {"name": "s", "type": "int", "required": False, "description": "Marker size for scatter points. Default: 40."},
        {"name": "alpha", "type": "float", "required": False, "description": "Transparency for scatter points. Default: 0.9."},
        {"name": "edgecolor", "type": "str", "required": False, "description": "Edge color for scatter points. Default: 'white'."},
        {"name": "linewidth", "type": "float", "required": False, "description": "Edge line width for scatter points. Default: 0.3."},
        {"name": "save", "type": "str", "required": False, "description": "Base filename to save PNG and PDF versions if provided."},
    ],
    example_image="embedding_2d_plot.png",
    example_code="embedding_2d_plot.py",
)
def plot(
    df,
    font_family="Times New Roman",
    title=None,
    mode="categorical",  # "categorical" or "continuous"
    hue_column=None,
    palette=None,
    cmap_continuous="viridis",
    display_legend=False,
    legend_loc="lower right",
    display_cbar=False,
    cbar_loc="lower right",
    show_density=False,
    density_column=None,
    density_alpha=0.5,
    figsize=(8, 8),
    s=40,
    alpha=0.9,
    edgecolor='white',
    linewidth=0.3,
    ax=None,
    save=None,
):
    """
    General 2D Embedding Plot (for t-SNE, PCA, UMAP, etc.)
    """

    mpl.rcParams.update({"axes.spines.top": True, "axes.spines.right": True})

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    if mode == "categorical":
        assert hue_column is not None, "hue_column must be provided for categorical mode."
        df = df.sort_values(by=hue_column).reset_index(drop=True)

        if palette is None:
            num_classes = df[hue_column].nunique()
            palette = sns.color_palette("tab20", n_colors=num_classes)

        sns.scatterplot(
            ax=ax,
            data=df,
            x='x',
            y='y',
            hue=df[hue_column].astype(str),
            s=s,
            alpha=alpha,
            edgecolor=edgecolor,
            linewidth=linewidth,
            legend=display_legend,
            palette=palette,
        )

        if display_legend:
            legend = ax.legend(
                loc=legend_loc,
                fontsize=12,
                frameon=True,
                handlelength=1.1,
                title=hue_column,
                labelspacing=0.4,
                borderpad=0.8,
            )
            for handle in legend.legend_handles:
                handle.set_markersize(8)
            for text in legend.get_texts():
                text.set_fontfamily(font_family)
                text.set_fontsize(10)
            legend.get_title().set_fontsize(12)
            legend.get_title().set_fontfamily(font_family)
            legend.get_frame().set_alpha(0.9)

    elif mode == "continuous":
        assert hue_column is not None, "hue_column must be provided for continuous mode."

        sns.scatterplot(
            ax=ax,
            data=df,
            x='x',
            y='y',
            hue=hue_column,
            palette=sns.color_palette(cmap_continuous, as_cmap=True),
            legend=False,
            s=s,
            alpha=alpha,
            edgecolor=edgecolor,
            linewidth=linewidth,
        )

        if show_density:
            df = df.sort_values(by=density_column).reset_index(drop=True)

            # Default fallback
            if palette is None:
                num_classes = df[density_column].nunique()
                palette = sns.color_palette("tab20", n_colors=num_classes)

            for idx, (island, group) in enumerate(df.groupby(density_column)):
                sns.kdeplot(
                    ax=ax,
                    x=group['x'],
                    y=group['y'],
                    levels=1,
                    color=palette[idx % len(palette)],
                    linewidths=1.5,
                    alpha=density_alpha,
                    zorder=0
                )

        if display_cbar:
            norm = plt.Normalize(df[hue_column].min(), df[hue_column].max())
            sm = plt.cm.ScalarMappable(cmap=cmap_continuous, norm=norm)
            sm.set_array([])

            axins = inset_axes(ax, width="3%", height="25%", loc=cbar_loc,
                               bbox_to_anchor=(-0.02, 0.02, 1, 1),
                               bbox_transform=ax.transAxes,
                               borderpad=0)

            cbar = plt.colorbar(sm, cax=axins)
            cbar.ax.tick_params(labelsize=12)
            cbar.ax.yaxis.label.set_family(font_family)
            for label in cbar.ax.get_yticklabels():
                label.set_family(font_family)
            cbar.ax.yaxis.set_label_position('left')
            cbar.ax.yaxis.set_ticks_position('left')

            cbar.ax.set_ylabel("")
            cbar.ax.text(
                -2.5, 0.5, hue_column,
                rotation=90,
                fontsize=14,
                fontfamily=font_family,
                va='center',
                ha='center',
                transform=cbar.ax.transAxes
            )

    else:
        raise ValueError(f"Unknown mode: {mode}")

    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_aspect('equal')

    if title:
        ax.set_title(title, fontsize=16, fontfamily=font_family)

    plt.tight_layout()

    if save:
        plt.savefig(f"{save}.png", dpi=300, bbox_inches="tight")
        plt.savefig(f"{save}.pdf", dpi=300, bbox_inches="tight")

    return fig, ax