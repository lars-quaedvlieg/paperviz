import numpy as np
import pandas as pd
from swizz import table

# Config
tasks = ["Bin Packing", "TSP", "Flat Pack"]
models = ["LLaMA FunSearch", "LLaMA Method", "Phi FunSearch", "Phi Method", "Granite FunSearch", "Granite Method"]
splits = ["Validation", "Validation-Perturbed", "Test"]
budgets = ["9.6k", "16k", "22.4k"]

# Create 4-level MultiIndex
index = pd.MultiIndex.from_product([tasks, models, splits, budgets], names=["Task", "Model", "Split", "Budget"])

# Random generator with slight bias per method
np.random.seed(42)


def simulate_scores(model):
    base = {
        "FunSearch": 4.5,
        "Method": 3.5,
    }["Method" if "Method" in model else "FunSearch"]
    return [round(np.random.normal(loc=base, scale=0.1), 3) for _ in range(3)]


# Fill DataFrame
data = {"score": [simulate_scores(model) for (_, model, _, _) in index]}
df = pd.DataFrame(data, index=index).reset_index()

latex_code = table(
    "grouped_multicol_latex",
    df=df,
    row_index="Model",  # Goes on the left
    col_index=["Split", "Budget"],  # Becomes multicolumn/multicolumn in header
    groupby="Task",  # Each task gets a separate subtable section
    value_column="score",  # List of values to be formatted
    highlight="max",  # Highlight lowest mean in each column
    stderr=False,  # Use std error instead of std dev
    caption="Results across three combinatorial optimization tasks.",
    label="tab:combinatorial_results"
)

print(latex_code)
