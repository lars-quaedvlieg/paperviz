from pathlib import Path
import tarfile, pickle
from datetime import datetime
from typing import Any, Dict, Optional
import torch
import wandb
import pandas as pd
# -----------------------------------------------------------------------------
# LogTracker: decide when to log
# -----------------------------------------------------------------------------
class LogTracker:
    MAX_LEVEL    = 100
    BATCH        = -1
    EPOCH        = -2
    MINIBATCH    = -3

    def __init__(
        self,
        name: str,
        counter_key: str,
        trigger_level: int,
        logging_level: int,
        final_idx: int,
        depends_on: Optional["LogTracker"] = None,
        add_first: bool = False,
        add_last: bool = False,
    ):
        self.name           = name
        self.counter_key    = counter_key
        self.trigger_level  = trigger_level
        self.logging_level  = logging_level
        self.final_idx      = final_idx
        self.depends_on     = depends_on
        self.add_first      = add_first
        self.add_last       = add_last

        self.accumulated_progress = 0.0
        self.log_this_round       = False
        self.is_first             = False
        self.is_last              = False

        # prepare a folder just for this tracker
        self.log_dir = Path("paperviz_runs") / self.name
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def register_progress(self, idx: int, progress: float = None):
        """
        Call this at the end of each step.
        - idx: current batch/epoch index
        - progress: fraction (0..1) of how far through you are (for %‐based levels)
        """
        self.log_this_round = False
        self.is_first = (idx == 0)
        self.is_last  = (idx == self.final_idx - 1)
        if progress is not None:
            self.accumulated_progress += progress

        # 1) if we've disabled logging altogether
        if self.logging_level > LogTracker.MAX_LEVEL:
            return

        # 2) if we depend on another tracker that didn't fire, skip
        if self.depends_on is not None and not self.depends_on.log_this_round:
            return

        # 3) always fire if our trigger_level >= global logging_level
        if self.trigger_level >= self.logging_level:
            self.log_this_round = True
            return

        # 4) percentage‐based (only for top‐level)
        if self.depends_on is None:
            if self.accumulated_progress * 100 >= self.logging_level:
                self.accumulated_progress = 0.0
                self.log_this_round = True
                return

        # 5) force first/last
        if self.add_first and self.is_first:
            self.log_this_round = True
            return
        if self.add_last and self.is_last:
            self.log_this_round = True

    def log_to_file(self, logs: Dict[str, Any]):
        # convert single‐element tensors to native types
        simple = {
            k: (v.item() if isinstance(v, torch.Tensor) and v.numel() == 1 else v)
            for k, v in logs.items()
        }
        torch.save(simple, self.log_dir / f"{simple[self.counter_key]}.tar")


# -----------------------------------------------------------------------------
# thin wrapper that writes out to wandb + local tarball
# -----------------------------------------------------------------------------
def log(
    data: Dict[str, Any],
    out: list = ["wandb", "local"],
    run_name: Optional[str] = None,
):
    """
    Call this once per tracker that fires.
    - data: must include tracker.counter_key (e.g. {'epoch': 2, 'loss': 0.123})
    - out: choose any of ["wandb","local"]
    - run_name: grouping of multiple trackers into one run
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = run_name or timestamp
    base_dir = Path("paperviz_runs") / run_name
    base_dir.mkdir(parents=True, exist_ok=True)

    # --- W&B ---
    if "wandb" in out:
        # drop any keys ending in '_' to avoid internal trackers
        wb_payload = {k: v for k, v in data.items() if not k.endswith("_")}
        wandb.log(wb_payload)

    # --- LOCAL ---
    if "local" in out:
        # drop any keys ending in 'wandb' to keep local clean
        local_payload = {k: v for k, v in data.items() if not k.endswith("wandb")}
        # write a small pickle and tar it
        pkl = base_dir / f"{timestamp}.pkl"
        with open(pkl, "wb") as f:
            pickle.dump(local_payload, f)
        tar_path = base_dir / f"{timestamp}.tar.gz"
        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(pkl, arcname=pkl.name)
        pkl.unlink()
def load_runs(
    path: str,
    criteria: Optional[Dict[str, Any]] = None,
) -> pd.DataFrame:
    """
    Load all paperviz logs from `path`.

    Scans recursively for:
      - wrapper logs:   paperviz_runs/<run_name>/*.tar.gz   (contains a .pkl)
      - tracker logs:   paperviz_runs/<tracker_name>/*.tar   (torch.save)

    Returns a DataFrame with columns:
      - all your logged keys
      - run_name  (wrapper logs) or None
      - tracker   (tracker logs) or None

    If `criteria` is given, only keeps rows where each key==value.
    """
    root = Path(path)
    records: list[Dict[str, Any]] = []

    # --- wrapper logs (.tar.gz → .pkl) ---
    for gz in root.rglob("*.tar.gz"):
        run_name = gz.parent.name
        try:
            with tarfile.open(gz, "r:gz") as tf:
                member = next(m for m in tf.getmembers() if m.name.endswith(".pkl"))
                with tf.extractfile(member) as f:
                    data = pickle.load(f)
        except Exception:
            continue
        rec = dict(data)
        rec["run_name"] = run_name
        rec["tracker"] = None
        records.append(rec)

    # --- tracker logs (.tar → torch.load) ---
    for t in root.rglob("*.tar"):
        # skip the .tar.gz files we already handled
        if t.name.endswith(".tar.gz"):
            continue
        tracker = t.parent.name
        try:
            data = torch.load(t)
        except Exception:
            continue
        rec = dict(data)
        rec["tracker"] = tracker
        rec["run_name"] = None
        records.append(rec)

    # build DataFrame
    df = pd.DataFrame(records)

    # apply exact‐match filtering if requested
    if criteria:
        for key, val in criteria.items():
            df = df[df.get(key) == val]

    return df

def filter_out_underscore(d):
    """Filters out the keys ending with _"""
    return {k: v for k, v in d.items() if not k.endswith("_")}


def filter_out_wandb(d):
    """Filters out the keys ending with wandb"""
    return {k: v for k, v in d.items() if not k.endswith("wandb")}