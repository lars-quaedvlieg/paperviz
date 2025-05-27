from manim import *
from swizz.manims._registry import register_manim
from swizz.utils.manims import shorten_function_code as shorten_function_code_util

@register_manim(
    name="code_evolution",
    description="Visualizes the evolution of code versions with their optimality scores",
    args=[
        {"name": "functions", "type": "List[str]", "required": True, "description": "The list of functions to visualize."},
        {"name": "title", "type": "str", "required": False, "description": "The title of the code evolution."},
        {"name": "function_scores", "type": "List[float]", "required": False, "description": "The list of optimality scores for each function."},
        {"name": "function_rounds", "type": "List[int]", "required": False, "description": "The list of rounds for each function."},
        {"name": "shorten_function_code", "type": "bool", "required": False, "description": "Whether to shorten the function code. Default is False."},
        {"name": "time_beween_functions", "type": "float", "required": False, "description": "The time between functions. Default is 4."},
        {"name": "code_config", "type": "dict", "required": False, "description": "The configuration for the code."},
        {"name": "font_style", "type": "str", "required": False, "description": "The font style for the text. Default is 'Courier New'."},
        {"name": "round_label", "type": "str", "required": False, "description": "The label for the round."},
        {"name": "score_label", "type": "str", "required": False, "description": "The label for the score."},
        {"name": "title_font_size", "type": "int", "required": False, "description": "The font size for the title. Default is 28."},
        {"name": "score_font_size", "type": "int", "required": False, "description": "The font size for the score. Default is 24."},
        {"name": "round_font_size", "type": "int", "required": False, "description": "The font size for the round. Default is 20."},
        {"name": "code_scale", "type": "float", "required": False, "description": "The scale for the code. Default is 0.25."},
    ],
    example_output="code_evolution.mp4",
    example_thumbnail="code_evolution.png",
    example_code="code_evolution.py",
)
class CodeEvolution(Scene):
        def __init__(self, functions, title=None, function_scores=None, function_rounds=None, shorten_function_code=False, 
                    time_beween_functions=4, code_config=None, font_style="Courier New", round_label="Round", score_label="Score", title_font_size=28,
                    score_font_size=24, round_font_size=20, code_scale=0.25):
            super().__init__()  # Initialize the parent Scene class
            self.title = title
            self.functions = functions
            self.function_scores = function_scores
            self.function_rounds = function_rounds
            self.shorten_function_code = shorten_function_code
            self.time_beween_functions = time_beween_functions
            self.code_config = code_config
            if self.code_config is None:
                self.code_config = {
                    "tab_width": 4,
                    "language": "python",
                    "add_line_numbers": False,
                    "formatter_style": "monokai",
                    "background": "window",
                    "background_config": {"stroke_color": BLACK}
                }
            self.font_style = font_style
            self.round_label = round_label
            self.score_label = score_label
            self.title_font_size = title_font_size
            self.score_font_size = score_font_size  
            self.round_font_size = round_font_size
            self.code_scale = code_scale
        def construct(self):
            # Title
            if self.title is not None:
                title = Text(
                    self.title,
                    font_size=self.title_font_size,
                    color=WHITE
                ).to_edge(UP)
                self.play(Write(title))
                self.wait(0.5)
            self.wait(0.5)

            if self.shorten_function_code:
                code_versions = map(shorten_function_code_util, self.functions, [45] * len(self.functions), [0] * len(self.functions))
            else:
                code_versions = self.functions

            # First code block
            prev_code = Code(code_string=code_versions[0], **self.code_config).scale(self.code_scale)

            if self.function_scores is not None:
                max_score, min_score = self.function_scores[0], self.function_scores[-1]
                norm_score = (self.function_scores[0] - min_score) / (max_score - min_score)
                prev_score_text = Text(
                    f"{self.score_label}: {self.function_scores[0]:.3f}",
                    font_size=self.score_font_size,
                    font=self.font_style,
                    color=interpolate_color(GREEN, RED, norm_score),
                ).next_to(prev_code, DOWN)

            if self.function_rounds is not None:
                prev_round_text = Text(
                    f"{self.round_label}: {self.function_rounds[0]}",
                    font_size=self.round_font_size,
                    font=self.font_style,
                    color=WHITE,
                ).next_to(prev_score_text, DOWN)

            # Appear
            to_write = [FadeIn(prev_code)]
            if self.function_scores is not None:
                to_write.append(Write(prev_score_text))
            if self.function_rounds is not None:
                to_write.append(Write(prev_round_text))
            self.play(*to_write)
            self.wait(self.time_beween_functions)

            # Animation loop through versions
            for next_version, score, round_num in zip(code_versions[1:], self.function_scores[1:], self.function_rounds[1:]):
                next_code = Code(code_string=next_version, **self.code_config).scale(self.code_scale)

                if self.function_scores is not None:
                    norm_score = (score - min_score) / (max_score - min_score)
                    color = interpolate_color(GREEN, RED, norm_score)
                    next_score_text = Text(
                        f"{self.score_label}: {score:.3f}",
                        font_size=self.score_font_size,
                        color=color,
                        font=self.font_style
                    ).next_to(next_code, DOWN)

                if self.function_rounds is not None:
                    next_round_text = Text(
                        f"{self.round_label}: {round_num}",
                        font_size=self.round_font_size,
                        font=self.font_style,
                        color=WHITE,
                    ).next_to(next_score_text, DOWN)

                to_transform = [Transform(prev_code, next_code)]
                if self.function_scores is not None:
                    to_transform.append(Transform(prev_score_text, next_score_text))
                if self.function_rounds is not None:
                    to_transform.append(Transform(prev_round_text, next_round_text))

                self.play(*to_transform)
                self.wait(self.time_beween_functions)