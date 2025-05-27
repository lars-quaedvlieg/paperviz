# `code_evolution`

> Visualizes the evolution of code versions with their optimality scores

---

## 📥 Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| functions | List[str] | ✅ | The list of functions to visualize. |
| title | str | ❌ | The title of the code evolution. |
| function_scores | List[float] | ❌ | The list of optimality scores for each function. |
| function_rounds | List[int] | ❌ | The list of rounds for each function. |
| shorten_function_code | bool | ❌ | Whether to shorten the function code. Default is False. |
| time_beween_functions | float | ❌ | The time between functions. Default is 4. |
| code_config | dict | ❌ | The configuration for the code. |
| font_style | str | ❌ | The font style for the text. Default is 'Courier New'. |
| round_label | str | ❌ | The label for the round. |
| score_label | str | ❌ | The label for the score. |
| title_font_size | int | ❌ | The font size for the title. Default is 28. |
| score_font_size | int | ❌ | The font size for the score. Default is 24. |
| round_font_size | int | ❌ | The font size for the round. Default is 20. |
| code_scale | float | ❌ | The scale for the code. Default is 0.25. |

---

## 📦 Example Output

````{dropdown} Click to show example code
```python
from swizz import render_manim

# Example showing different versions of a sorting algorithm evolving
example_functions_evolving = [
    """
    def bubble_sort(arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr
    """,
    """
    def quick_sort(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)
    """,
    """
    def optimized_quick_sort(arr):
        def partition(low, high):
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1

        def quick_sort_helper(low, high):
            if low < high:
                pi = partition(low, high)
                quick_sort_helper(low, pi - 1)
                quick_sort_helper(pi + 1, high)
            return arr

        return quick_sort_helper(0, len(arr) - 1)
    """,
]

# Scores representing the efficiency of each algorithm
# Higher scores (closer to 1) are shown in green, lower scores in red
example_function_scores = [
    0.3,  # Bubble sort: O(n²)
    0.7,  # Basic quicksort: O(n log n)
    0.9,  # Optimized quicksort: O(n log n) with better constants
]

# Rounds/iterations of the optimization process
example_function_rounds = [
    "O(n²)",  # Initial implementation
    "O(n log n)",  # First optimization
    "O(n log n)",  # Final optimization
]

# Configuration for the Manim renderer
# All attributes can be found at https://docs.manim.community/en/stable/reference/manim._config.utils.ManimConfig.html
manim_render_config = {
    "quality": "high_quality",
    "format": "mp4",
    "save_pngs": True,
}

# Render the code evolution animation
render_manim(
    "code_evolution",
    render_config=manim_render_config,
    title="Sorting Algorithm Evolution",
    functions=example_functions_evolving,
    function_scores=example_function_scores,
    function_rounds=example_function_rounds,
    # Optional arguments with explanations:
    shorten_function_code=False,  # Set to True to truncate long code snippets
    time_beween_functions=3,      # Time in seconds between transitions
    code_config={                 # Customize code appearance
        "tab_width": 4,
        "language": "python",
        "add_line_numbers": True,
        "formatter_style": "monokai",
        "background": "window",
    },
    font_style="Courier New",     # Font for text elements
    round_label="Complexity",      # Custom label for rounds
    score_label="Efficiency",     # Custom label for scores
    title_font_size=28,          # Larger title for better visibility
    score_font_size=24,          # Size for score text
    round_font_size=20,          # Size for round text
    code_scale=0.6,              # Scale factor for code blocks
)
```
````

<video src="../../_static/images/manim/code_evolution.mp4" alt="code_evolution" controls style="max-width: 100%; width: auto; height: auto; max-height: 450px;">
