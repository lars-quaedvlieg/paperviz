import pandas as pd
import matplotlib.pyplot as plt
from swizz import plot

# 1) Define a toy confusion matrix as a DataFrame
data = [
    [50,  2,  3],
    [ 5, 45, 10],
    [ 2,  8, 40],
]
labels = ["Class A", "Class B", "Class C"]
cm_df = pd.DataFrame(data, index=labels, columns=labels)

# 2) Plot raw counts
fig1, ax1 = plot(
    "confusion_matrix",
    cm=cm_df,
    labels=labels,  # optional, can be omitted since already in the DataFrame
    figsize=(6, 5),
    cmap="Oranges",
    normalize=False,
    fmt="d",
    cbar=True,
    save="confusion_matrix_raw"
)
plt.show()
