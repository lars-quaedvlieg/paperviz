import numpy as np
from matplotlib import pyplot as plt
from swizz import plot

data = {
    "No APM limit": {"Test Elo": 1392},
    "200% APM limit": {"Test Elo": 1411},
    "100% APM limit": {"Test Elo": 1540},
    "50% APM limit": {"Test Elo": 1536},
    "25% APM limit": {"Test Elo": 1419},
    "10% APM limit": {"Test Elo": 1145},
    "0% APM limit": {"Test Elo": 0},
}
fig, ax = plot("general_horizontal_bar_plot",
    data,
    xlabel="Test Elo",
    ylabel="APM limits",
    color_map={"Test Elo": "#FF7F0E"},
    bar_height=0.45,
    style_map={"Test Elo": ""},
    save="general_barh_plot",
)
plt.show()
