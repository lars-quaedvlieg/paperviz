np.random.seed(0)

domains = ["HalfCheetah", "Hopper", "Walker2d", "Ant"]
tasks = ["IL (↑) [1]", "Off-RL (↑) [1]", "Sensor failure (↑) [11]", "Dynamics change (↑) [4]"]
methods = ["MLP", "Modality", "Component"]

rows = []
for domain in domains:
    for task in tasks:
        for method in methods:
            values = np.round(np.random.normal(loc=1.0, scale=0.05, size=5), 3).tolist()
            rows.append({
                "Domain": domain,
                "Task": task,
                "Method": method,
                "score": values
            })

df = pd.DataFrame(rows)

latex = table(
    "grouped_multirow_latex",
    df=df,
    row1="Domain",
    row2="Task",
    col="Method",
    value_column="score",
    highlight="max",
    stderr=False,
    caption="Expert-normalized returns across domains and methods.",
    label="tab:tokenization_comparison"
)

print(latex)
