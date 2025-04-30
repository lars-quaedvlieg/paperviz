import numpy as np
from matplotlib import pyplot as plt
from swizz import plot

data_dict = {
    "Forward": {
        "Accuracy": 4.2, "Precision": 3.5, "Recall": 2.1,
    },
    "Reverse": {
        "Accuracy": 6.0, "Precision": 5.2, "Recall": 4.8,
    },
    "Baseline": {
        "Accuracy": 5.3, "Precision": 4.8, "Recall": 3.6,
    }
}

# Color map where 'Reward' is assigned blue and 'Goal' is assigned pink


# Style map for each metric (hatch patterns for filling)
style_map = {
    "Accuracy": '',
    "Precision": '\\',
    "Recall": 'x'  # Cross hatch pattern for Recall
}

plot("general_bar_plot",data_dict,style_map=style_map,save="bar")
plt.show()
