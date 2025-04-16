import numpy as np


def format_cell(value, precision=2, with_pm=True, stderr=False):
    if isinstance(value, (float, int)):
        return str(value), value  # return (formatted_str, numeric_mean)

    elif isinstance(value, (list, tuple, np.ndarray)):
        arr = np.array(value)
        mean = arr.mean()
        error = arr.std(ddof=1) / np.sqrt(len(arr)) if stderr else arr.std(ddof=1)
        if with_pm:
            formatted = f"${mean:.{precision}f} \\pm {error:.{precision}f}$"
        else:
            formatted = f"{mean:.{precision}f}"
        return formatted, mean

    else:
        raise ValueError(f"Unsupported value type: {value}")
