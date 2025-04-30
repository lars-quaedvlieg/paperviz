# scripts/test_loading.py

from swizz.logging.logging import load_runs
import pandas as pd

def main():
    # point this at the folder you’ve been writing into
    root = "swizz_runs"

    # 1) load everything
    df_all = load_runs(root)
    print("=== ALL LOGS ===")
    print(df_all.head(), "\n")
    print(f"Total records: {len(df_all)}")
    print("Trackers present:", df_all["tracker"].unique())
    print("Runs present:    ", df_all["run_name"].unique(), "\n")

    # 2) filter just batch‐level tracker logs
    df_batch = load_runs(root, criteria={"tracker": "batch"})
    print("=== BATCH TRACKER LOGS ===")
    print(df_batch.sort_values(["epoch", "batch"]).head(), "\n")

    # 3) filter just wrapper logs (the ones with run_name set)
    df_wrapper = load_runs(root, criteria={"tracker": None})
    print("=== WRAPPER LOGS ===")
    print(df_wrapper.head())

if __name__ == "__main__":
    main()
