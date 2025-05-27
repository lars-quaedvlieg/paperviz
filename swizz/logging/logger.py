from pathlib import Path
import tarfile
import pickle
from datetime import datetime
from typing import Any, Dict, List, Optional
import pandas as pd
import torch
import wandb


class LogTracker:
    """
    Tracks whether to emit a log based on the presence of specified keys.

    Parameters
    ----------
    name
        Unique name for this tracker (also the subfolder under swizz_runs/).
    counter_key
        The key in your logs dict whose value is used as filename for local files.
    final_idx
        Index of the last step (so we know when we're on the “last” batch/epoch).
    keys_to_log
        List of keys: if any appear in the logs dict, we’ll log this round.
    depends_on
        Another LogTracker; if it didn’t fire, this one won’t fire either.
    add_first
        Always log at idx=0 regardless of keys.
    add_last
        Always log at idx=final_idx-1 regardless of keys.
    """
    def __init__(
        self,
        name: str,
        counter_key: str,
        final_idx: int,
        keys_to_log: Optional[List[str]] = None,
        depends_on: Optional["LogTracker"] = None,
        add_first: bool = False,
        add_last: bool = False,
    ):
        self.name = name
        self.counter_key = counter_key
        self.final_idx = final_idx
        self.keys_to_log = keys_to_log or []
        self.depends_on = depends_on
        self.add_first = add_first
        self.add_last = add_last

        self.log_this_round = False
        self.is_first = False
        self.is_last = False

        # prepare a folder just for this tracker
        self.log_dir = Path("swizz_runs") / self.name
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def register(self, idx: int, logs: Dict[str, Any]) -> bool:
        """
        Decide whether to log on this round.

        Parameters
        ----------
        idx
            Current batch/epoch index.
        logs
            Dictionary of values you intend to record (e.g. {'epoch': 3, 'loss': 0.12}).

        Returns
        -------
        bool
            True if we should log (so you can call .log_to_file(logs)).
        """
        self.is_first = (idx == 0)
        self.is_last = (idx == self.final_idx - 1)
        self.log_this_round = False

        # If we're chained to another tracker that didn’t fire, skip
        if self.depends_on and not self.depends_on.log_this_round:
            return False

        # Fire if any of the watched keys are present
        if any(key in logs for key in self.keys_to_log):
            self.log_this_round = True

        # Force first/last if requested
        if self.add_first and self.is_first:
            self.log_this_round = True
        if self.add_last and self.is_last:
            self.log_this_round = True

        return self.log_this_round

    def log_to_file(self, logs: Dict[str, Any]) -> None:
        """
        Save a local torch.tar snapshot of whatever you passed in logs.

        Uses `counter_key` to name the file, so ensure that key is in your dict.
        """
        # convert single‐element tensors to native types
        simple = {
            k: (v.item() if isinstance(v, torch.Tensor) and v.numel() == 1 else v)
            for k, v in logs.items()
        }
        filename = f"{simple[self.counter_key]}.tar"
        torch.save(simple, self.log_dir / filename)


def log(
    data: Dict[str, Any],
    out: List[str] = ["wandb", "local"],
    run_name: Optional[str] = None,
) -> None:
    """
    Log to W&B and/or locally (wrapper for LogTracker.log_to_file).

    Parameters
    ----------
    data
        Must include a timestamp/key field (e.g. {'epoch':2,'loss':0.123}).
    out
        Any of ["wandb","local"].
    run_name
        If given, groups this under swizz_runs/<run_name>/; else
        uses timestamp as run_name.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = run_name or timestamp
    base_dir = Path("swizz_runs") / run_name
    base_dir.mkdir(parents=True, exist_ok=True)

    # --- W&B ---
    if "wandb" in out:
        wb_payload = {k: v for k, v in data.items() if not k.endswith("_")}
        wandb.log(wb_payload)

    # --- LOCAL (.tar.gz) ---
    if "local" in out:
        # drop any keys ending in 'wandb'
        local_payload = {k: v for k, v in data.items() if not k.endswith("wandb")}
        pkl_path = base_dir / f"{timestamp}.pkl"
        with open(pkl_path, "wb") as f:
            pickle.dump(local_payload, f)
        tar_path = base_dir / f"{timestamp}.tar.gz"
        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(pkl_path, arcname=pkl_path.name)
        pkl_path.unlink()


def load_runs(
    path: str,
    criteria: Optional[Dict[str, Any]] = None,
) -> pd.DataFrame:
    """
    Recursively load both wrapper (.tar.gz) and tracker (.tar) logs under `path`.
    Returns a DataFrame with one row per log and columns for every key.

    If `criteria` is given, only keeps rows where each key==value.
    """
    root = Path(path)
    records = []

    # wrapper logs: .tar.gz → .pkl
    for gz in root.rglob("*.tar.gz"):
        run_name = gz.parent.name
        try:
            with tarfile.open(gz, "r:gz") as tf:
                member = next(m for m in tf.getmembers() if m.name.endswith(".pkl"))
                with tf.extractfile(member) as f:
                    data = pickle.load(f)
        except Exception:
            continue
        rec = dict(data, run_name=run_name, tracker=None)
        records.append(rec)

    # tracker logs: .tar → torch.load
    for t in root.rglob("*.tar"):
        if t.name.endswith(".tar.gz"):
            continue
        tracker_name = t.parent.name
        try:
            data = torch.load(t)
        except Exception:
            continue
        rec = dict(data, run_name=None, tracker=tracker_name)
        records.append(rec)

    df = pd.DataFrame(records)
    if criteria:
        for key, val in criteria.items():
            df = df[df.get(key) == val]
    return df
