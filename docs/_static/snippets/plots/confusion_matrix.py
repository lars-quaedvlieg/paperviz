import numpy as np
import matplotlib.pyplot as plt
from swizz import plot

# 1) Define a toy confusion matrix
#    Rows = true classes, Columns = predicted classes
cm = np.array([
    [50,  2,  3],
    [ 5, 45, 10],
    [ 2,  8, 40],
])

# 2) Class labels
labels = ["Class A", "Class B", "Class C"]

# 3) Plot raw counts
fig1, ax1 = plot(
    "confusion_matrix",
    cm=cm,
    labels=labels,
    figsize=(6, 5),
    cmap="Oranges",
    normalize=False,
    fmt="d",
    cbar=True,
    save="confusion_matrix_raw"
)
plt.show()
