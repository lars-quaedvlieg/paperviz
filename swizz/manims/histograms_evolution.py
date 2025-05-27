from manim import *
from swizz.manims._registry import register_manim
import numpy as np

@register_manim(
    name="histograms_evolution",
    description="Visualizes the evolution of histograms",
    args=[
        {"name": "scores_df", "type": "pd.DataFrame", "required": True, "description": "The dataframe containing the scores."},
        {"name": "method_column", "type": "str", "required": True, "description": "The column containing the method names."},
        {"name": "iteration_column", "type": "str", "required": True, "description": "The column containing the iteration numbers."},
        {"name": "score_column", "type": "str", "required": True, "description": "The column containing the scores."},
        {"name": "x_min", "type": "float", "required": True, "description": "The minimum value of the x-axis."},
        {"name": "x_max", "type": "float", "required": True, "description": "The maximum value of the x-axis."},
        {"name": "x_step", "type": "float", "required": True, "description": "The step size of the x-axis."},
        {"name": "num_bins", "type": "int", "required": True, "description": "The number of bins for the histogram."},
        {"name": "font_style", "type": "str", "required": False, "description": "The font style for the text. Default is 'Courier New'."},
        {"name": "max_y", "type": "float", "required": False, "description": "The maximum value of the y-axis. Default is None."},
        {"name": "x_length", "type": "float", "required": False, "description": "The length of the x-axis within the render. Default is 10."},
        {"name": "y_length", "type": "float", "required": False, "description": "The length of the y-axis within the render. Default is 5."},
        {"name": "time_between_iterations", "type": "float", "required": False, "description": "The time between iterations. Default is 0.5."},
        {"name": "color_dict", "type": "dict", "required": False, "description": "The dictionary containing the hex codes for the colors for the methods. Default is None."},
        {"name": "wait_time_at_end", "type": "float", "required": False, "description": "The time to wait at the end. Default is 5."},
    ],
    example_output="histograms_evolution.mp4",
    example_thumbnail="histograms_evolution.png",
    example_code="histograms_evolution.py",
)
class HistogramEvolution(Scene):
    def __init__(self, scores_df, method_column, iteration_column, score_column, x_min, x_max, x_step, num_bins, font_style="Courier New", max_y=None, x_length=10, y_length=5, time_between_iterations=0.5, wait_time_at_end=5, color_dict=None):
        super().__init__()
        self.scores_df = scores_df
        self.method_column = method_column
        self.iteration_column = iteration_column
        self.score_column = score_column
        self.x_min = x_min
        self.x_max = x_max
        self.max_y = max_y
        self.x_step = x_step
        self.num_bins = num_bins
        self.font_style = font_style
        self.x_length = x_length
        self.y_length = y_length
        self.time_between_iterations = time_between_iterations
        self.color_dict = color_dict
        self.wait_time_at_end = wait_time_at_end

    def construct(self):
        iteration_label = self.iteration_column
        time_grouped_df = sorted(self.scores_df.groupby(self.iteration_column))

        bins = np.linspace(0.0, self.x_max, self.num_bins)

        num_methods = len(self.scores_df[self.method_column].unique())
        method_names = sorted(self.scores_df[self.method_column].unique())
        if self.color_dict is not None:
            colors = [self.color_dict[method] for method in method_names]
        else:
            colors = [interpolate_color(BLUE, ORANGE, i / (num_methods - 1)) for i in range(num_methods)]

        # Precompute max height from all score datasets
        all_hist_values = []
        for _, time_group in time_grouped_df:
            for _, method_group in sorted(time_group.groupby(self.method_column)):
                all_hist_values.append(np.histogram(method_group[self.score_column].values, bins=bins)[0])
        global_max_height = max([h.max() for h in all_hist_values])

        if self.max_y is None:
            global_y_max = int(1.2 * global_max_height)
        else:
            global_y_max = self.max_y

        scene_height_per_count = self.y_length / global_y_max

        # Set up axes
        axes = Axes(
            x_range=[self.x_min, self.x_max, self.x_step],
            y_range=[0, global_y_max, int(round(global_y_max / 5))],
            tips=False,
            axis_config={"include_numbers": True},
            x_length=self.x_length, y_length=self.y_length,
        ).to_edge(UP * 1.5)

        # Create axis titles
        to_write = [Create(axes)]

        x_label = Text(self.score_column, font_size=28, font=self.font_style)
        # Position them relative to axes
        x_label.next_to(axes.x_axis, DOWN, buff=0.4)
        to_write.append(Write(x_label))

        y_label = Text("Count", font_size=28, font=self.font_style)
        # Position them relative to axes
        y_label.next_to(axes.y_axis, buff=0.4).rotate(PI / 2).move_to(
            axes.c2p(0, global_y_max / 2) + LEFT * 1.5)
        to_write.append(Write(y_label))

        self.play(*to_write)

        time_iter = iter(time_grouped_df)

        # Text to show round number and total count
        first_round, first_round_data = next(time_iter)
        round_text = Text(f"{iteration_label}: {first_round}", font_size=24, font=self.font_style).next_to(x_label, DOWN)

        # Initial histogram
        all_bars = VGroup()
        for hist_idx, (_, histogram_score_data_per_round) in enumerate(sorted(first_round_data.groupby(self.method_column))):
            hist_values, _ = np.histogram(histogram_score_data_per_round[self.score_column].values, bins=bins)
            bar_width = (bins[1] - bins[0]) * (
                    self.x_length / (self.x_max - self.x_min))  # Some spacing TODO: Figure out how to tweak this analytically
            bars = VGroup()
            for i, height in enumerate(hist_values):
                bar = Rectangle(
                    width=bar_width,
                    height=height * scene_height_per_count,  # scale height
                    fill_color=colors[hist_idx],
                    fill_opacity=0.7,
                    stroke_width=0
                )
                bar.next_to(
                    axes.c2p((bins[i] + bins[i + 1]) / 2, 0),
                    direction=UP,
                    buff=0
                )
                bars.add(bar)
            all_bars.add(bars)

        # Create legend in the top right corner
        legend_items = VGroup()
        for i, color in enumerate(colors):
            color_box = Square(side_length=0.3, fill_color=color, fill_opacity=1, stroke_width=0)
            label = Text(f"{method_names[i]}", font_size=20, font=self.font_style)
            legend_item = VGroup(color_box, label).arrange(RIGHT, buff=0.3)
            legend_items.add(legend_item)

        # Arrange all legend items in a vertical stack and place in the top-right
        legend = legend_items.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.to_corner(UR, buff=0.5)

        self.play(Write(round_text), FadeIn(all_bars), Write(legend))

        for round_num, scores in time_iter:
            next_all_bars = VGroup()
            for hist_idx, (_, histogram_score_data_per_round) in enumerate(sorted(scores.groupby(self.method_column))):
                next_hist_values, _ = np.histogram(histogram_score_data_per_round[self.score_column].values, bins=bins)

                # Recompute bars with updated axis scaling
                next_bars = VGroup()
                for i, height in enumerate(next_hist_values):
                    bar = Rectangle(
                        width=bar_width,
                        height=height * scene_height_per_count,  # dynamic scaling for height
                        fill_color=colors[hist_idx],
                        fill_opacity=0.7,
                        stroke_width=0
                    )
                    bar.next_to(
                        axes.c2p((bins[i] + bins[i + 1]) / 2, 0),
                        direction=UP,
                        buff=0
                    )
                    next_bars.add(bar)
                next_all_bars.add(next_bars)

            new_round_text = Text(f"{iteration_label}: {round_num}", font_size=24, font=self.font_style).next_to(x_label, DOWN)

            self.play(
                Transform(all_bars, next_all_bars),
                Transform(round_text, new_round_text),
                run_time=self.time_between_iterations
            )

        self.wait(self.wait_time_at_end)