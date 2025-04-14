# 🤝 Contributing to paperviz

Thanks for your interest in contributing to **paperviz**! This project aims to make **beautiful, publication-quality figures and LaTeX outputs** as effortless as possible for researchers.

Whether you're fixing a bug, adding a table format, improving docs, or building new layouts — you're very welcome here.

---

## 🧱 Repo Structure

| Folder                  | Purpose |
|--------------------------|---------|
| `paperviz/table/`        | Table generators (e.g. `results_latex`, `results_multilevel_latex`) |
| `paperviz/plot/`         | Plotting utilities (Seaborn + Matplotlib wrappers) |
| `paperviz/layout/`       | Layout builders for subfigures, grids, side-by-side |
| `paperviz/utils/`        | Formatters, math helpers, config exports |
| `docs/`                  | Jupyter Book examples and usage guides |
| `tests/`                 | Unit tests for tables, renderers, and plots |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/paperviz.git
cd paperviz
```

### 2. Set up the environment

We recommend using `venv` or `conda`.

```bash
pip install -e .[dev]
```

This will install paperviz in editable mode along with:
- `pytest`
- `black`
- `flake8`
- `jupyter-book` (for docs)

---

## ✅ What You Can Work On

- 📊 Add new table formats (`paperviz/table/`)
- 🖼️ Add plot utilities with unified style (`paperviz/plot/`)
- 🧩 Create layout presets (`paperviz/layout/`)
- 🧾 Write LaTeX string generators for common patterns
- 🧪 Improve or add tests
- 📚 Expand the Jupyter Book gallery (`docs/`)
- 🐛 Fix issues or formatting bugs

---

## 🧪 Running Tests

```bash
pytest
```

---

## 🧼 Style Guide

- Format with **Black**:  
  ```bash
  black paperviz/
  ```
- Use **type hints** where useful
- Keep functions small, composable, and documented with a one-line docstring
- Use f-strings over `format()`
- Prefer `pd.DataFrame` inputs/outputs where applicable

---

## 🧠 Tips for Adding a Table

If you're adding a new table function:

1. Add it to `paperviz/table/yourfile.py`
2. Register it with the `@register_table` decorator
3. Define argument metadata (`args=[...]`) for discoverability
4. Write a quick usage example in the `docs/`
5. Add a basic test under `tests/table/`

---

## 📬 Submitting a Pull Request

- Fork the repo
- Create a new branch: `feature/new-table` or `fix/highlight-bug`
- Open a pull request and describe what you changed
- Tag `@lars` if urgent 😎

---

## ❤️ Acknowledgements

Paperviz is made by researchers, for researchers. Thank you for helping improve it — every contribution counts 🙏
