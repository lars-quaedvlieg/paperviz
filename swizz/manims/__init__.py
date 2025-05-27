import importlib
import os

# Dynamically import all .py files in the manims directory (excluding special files)
for filename in os.listdir(os.path.dirname(__file__)):
    if filename.endswith(".py") and not filename.startswith(("_", "__")):
        importlib.import_module(f"swizz.manims.{filename[:-3]}")