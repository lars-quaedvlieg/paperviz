import pandas as pd
from swizz import table

df = pd.DataFrame({
    "Model": ["A", "B"],
    "acc": [[0.85, 0.88, 0.87], [0.90, 0.91, 0.89]],
    "f1": [0.83, [0.92, 0.93]]
})

latex = table(
    "df_to_latex",
    df,
    highlight={"acc": "max", "f1": "max"},
    stderr=False,
    caption="Results on CIFAR-10",
    label="tab:cifar10_results"
)

print(latex)
