from swizz.plots._registry import plot_registry


# class PlotBlock:
#     def __init__(self, fn, kwargs=None, fixed_width=None, fixed_height=None):
#         self.fn = fn
#         self.kwargs = kwargs or {}
#         self.fixed_width = fixed_width
#         self.fixed_height = fixed_height
#
#     def render(self, fig, pos):
#         ax = fig.add_axes(pos)
#         plot_fn = plot_registry[self.fn]["func"] if isinstance(self.fn, str) else self.fn
#         return plot_fn(ax=ax, **self.kwargs)


class PlotBlock:
    def __init__(self, fn, kwargs=None, fixed_width=None, fixed_height=None):
        self.fn = fn
        self.kwargs = kwargs or {}
        self.last_ax = None  # <-- track for legends
        self.exclude_from_legend = self.kwargs.pop("exclude_from_legend", False)
        self.fixed_width = fixed_width
        self.fixed_height = fixed_height

    def render(self, fig, pos):
        ax = fig.add_axes(pos)
        plot_fn = plot_registry[self.fn]["func"] if isinstance(self.fn, str) else self.fn
        plot_fn(ax=ax, **self.kwargs)
        self.last_ax = ax
        return ax


class Label:
    def __init__(self, text, align="center", fontsize=14, fontfamily=None, fixed_width=None, fixed_height=None):
        self.text = text
        self.align = align
        self.fontsize = fontsize
        self.fontfamily = fontfamily
        self.fixed_width = fixed_width
        self.fixed_height = fixed_height

    def render(self, fig, pos):
        x, y, w, h = pos

        # Compute anchor point
        if self.align == "left":
            anchor = (x, y + h / 2)
            ha = "left"
        elif self.align == "right":
            anchor = (x + w, y + h / 2)
            ha = "right"
        else:  # center
            anchor = (x + w / 2, y + h / 2)
            ha = "center"

        fig.text(
            anchor[0],
            anchor[1],
            self.text,
            fontsize=self.fontsize,
            fontfamily=self.fontfamily,
            ha=ha,
            va="center"
        )

        return []


class LegendBlock:
    def __init__(
            self,
            labels,
            handles=None,
            title=None,
            ncol=1,
            loc="center",
            fixed_width=None,
            fixed_height=None,
    ):
        self.handles = handles
        self.labels = labels
        self.title = title
        self.ncol = ncol
        self.loc = loc
        self.fixed_width = fixed_width
        self.fixed_height = fixed_height

    def set_handles(self, handles, labels):
        self.handles = handles
        self.labels = labels

    def render(self, fig, pos):
        ax = fig.add_axes(pos)
        ax.axis("off")

        if self.handles is None or not self.handles:
            return ax  # Skip rendering legend for now

        legend = ax.legend(
            handles=self.handles,
            labels=self.labels,
            loc=self.loc,
            ncol=self.ncol,
        )

        legend.set_title(self.title)

        return [ax]


class EmptyBlock:
    def __init__(self, fixed_width=None, fixed_height=None):
        self.fixed_width = fixed_width
        self.fixed_height = fixed_height

    def render(self, fig, pos):
        # Do nothing and return no axes
        return []


class Row:
    def __init__(self, children, spacing=0.05, fixed_height=None):
        self.children = children
        self.spacing = spacing
        self.fixed_height = fixed_height

    def layout(self, fig, pos):
        x, y, w, h = pos
        total_fixed = sum(c.fixed_width or 0 for c in self.children)
        dynamic_children = [c for c in self.children if not c.fixed_width]
        dynamic_width = (w - total_fixed - self.spacing * (len(self.children) - 1)) / max(len(dynamic_children), 1)

        xpos = x
        axes = []
        for i, child in enumerate(self.children):
            width = child.fixed_width if child.fixed_width else dynamic_width
            child_pos = [xpos, y, width, h]
            if hasattr(child, "layout"):
                axes.extend(child.layout(fig, child_pos))
            else:
                axes.append(child.render(fig, child_pos))
            xpos += width + self.spacing
        return axes


class Col:
    def __init__(self, children, spacing=0.05, fixed_width=None):
        self.children = children
        self.spacing = spacing
        self.fixed_width = fixed_width

    def layout(self, fig, pos):
        x, y, w, h = pos
        total_fixed = sum(c.fixed_height or 0 for c in self.children)
        dynamic_children = [c for c in self.children if not c.fixed_height]
        dynamic_height = (h - total_fixed - self.spacing * (len(self.children) - 1)) / max(len(dynamic_children), 1)

        ypos = y + h  # start from top
        axes = []
        for i, child in enumerate(self.children):
            height = child.fixed_height if child.fixed_height else dynamic_height
            ypos -= height
            child_pos = [x, ypos, w, height]
            if hasattr(child, "layout"):
                axes.extend(child.layout(fig, child_pos))
            else:
                axes.append(child.render(fig, child_pos))
            ypos -= self.spacing
        return axes
