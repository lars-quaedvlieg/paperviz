import logging
import wandb
import pandas as pd
import numpy as np
from tqdm import tqdm
from collections import defaultdict
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class RunGroup:
    """Represents a group of runs that should be analyzed together."""
    name: str
    run_ids: Optional[List[str]] = None
    prefix: Optional[str] = None
    
    def __post_init__(self):
        if self.run_ids is None and self.prefix is None:
            raise ValueError("Either run_ids or prefix must be provided")
        if self.run_ids is not None and self.prefix is not None:
            raise ValueError("Cannot provide both run_ids and prefix")

class WandbAnalyzer:
    def __init__(self, project_name: str, verbose: bool = False):
        """Initialize the WandbAnalyzer with a project name.
        
        Args:
            project_name: The full wandb project name (e.g., "username/project")
            verbose: Whether to enable verbose logging
        """
        self.api = wandb.Api()
        self.project_name = project_name
        self.verbose = verbose
        
    def _get_runs(self, run_group: RunGroup) -> List[wandb.apis.public.Run]:
        """Get runs either by prefix or by run IDs."""
        if run_group.prefix is not None:
            runs = list(self.api.runs(self.project_name, filters={"display_name": {"$regex": f"^{run_group.prefix}"}}))
            if self.verbose:
                logging.info(f"Found {len(runs)} runs for prefix '{run_group.prefix}'")
        else:
            runs = [self.api.run(f"{self.project_name}/{run_id}") for run_id in run_group.run_ids]
            if self.verbose:
                logging.info(f"Retrieved {len(runs)} runs by IDs for group '{run_group.name}'")
        return runs
    
    def _group_runs_by_seed(self, runs: List[wandb.apis.public.Run]) -> Dict[int, List[wandb.apis.public.Run]]:
        """Group runs by their seed value. If no seed is found, use a default seed of 0."""
        if len(runs) == 1:
            # If there's only one run, seed doesn't matter
            return {0: runs}
            
        grouped_runs = defaultdict(list)
        runs_without_seed = []
        
        for run in runs:
            seed = run.config.get('seed')
            if seed is not None:
                grouped_runs[seed].append(run)
            else:
                runs_without_seed.append(run)
        
        # If we have runs without seeds, add them to a default group
        if runs_without_seed:
            if self.verbose:
                logging.warning(f"Found {len(runs_without_seed)} runs without seed, grouping them together under seed 0")
            grouped_runs[0] = runs_without_seed
            
        if self.verbose:
            logging.info(f"Grouped runs into {len(grouped_runs)} seed groups")
            for seed, seed_runs in grouped_runs.items():
                logging.info(f"  Seed {seed}: {len(seed_runs)} runs")
                
        return dict(grouped_runs)
    
    def _stitch_runs(self, grouped_runs: Dict[int, List[wandb.apis.public.Run]], 
                    x_key: str, y_key: str, run_group_name: str,
                    samples: int = 100) -> Dict[int, pd.DataFrame]:
        """Stitch together runs with the same seed, handling overlapping x values.
        
        This method combines multiple runs from the same seed into a single continuous
        dataset, handling any overlapping x values by taking the mean of y values.
        
        Args:
            grouped_runs: Dictionary mapping seeds to lists of runs
            x_key: The key for the x-axis data
            y_key: The key for the y-axis data
            run_group_name: Name of the run group for logging
            samples: Number of samples to retrieve from wandb. Default is 100.
                    Higher values give more granular data but take longer to process.
            
        Returns:
            Dictionary mapping seeds to stitched DataFrames
        """
        stitched_data = {}
        
        for seed, runs in grouped_runs.items():
            if self.verbose:
                logging.info(f"Processing {len(runs)} runs for seed {seed} in group {run_group_name}")
                
            all_data = []
            
            for run in runs:
                history = run.history(keys=[x_key, y_key], pandas=True, samples=samples, x_axis=x_key)
                if not history.empty:
                    all_data.append(history)
                    if self.verbose:
                        logging.info(f"  Run {run.id}: found {len(history)} data points")
                else:
                    if self.verbose:
                        logging.warning(f"  Run {run.id}: no data found")
            
            if not all_data:
                if self.verbose:
                    logging.warning(f"No valid data found for seed {seed} in group {run_group_name}")
                continue
                
            # Combine all data
            combined_df = pd.concat(all_data)
            
            combined_df[y_key] = (
                combined_df[y_key]
                .replace("NaN", pd.NA)   # or np.nan
            )       
            if combined_df.isna().values.sum() > 0:
                logging.warning(f"Seed {seed} of group {run_group_name} has {combined_df.isna().values.sum()} NaNs, dropping them")
                combined_df = combined_df.dropna()

            # Handle overlapping x values by taking the mean of y values
            combined_df = combined_df.groupby(x_key)[y_key].mean().reset_index()
            
            if self.verbose:
                logging.info(f"  Final stitched data for seed {seed}: {len(combined_df)} unique x values")
            
            stitched_data[seed] = combined_df
            
        return stitched_data
    
    def get_stitched_runs(self, run_groups: List[RunGroup] | RunGroup, 
                         x_key: str, y_key: str,
                         samples: int = 100) -> Dict[str, Dict[int, pd.DataFrame]]:
        """Get stitched runs for each run group, organized by seed.
        
        This is the core method that handles grouping runs by experiment and seed,
        then stitching together runs from the same seed.
        
        Args:
            run_groups: List of RunGroup objects or single RunGroup
            x_key: The key for the x-axis data
            y_key: The key for the y-axis data
            samples: Number of samples to retrieve from wandb. Default is 100.
                    Higher values give more granular data but take longer to process.
            
        Returns:
            Dictionary mapping run group names to dictionaries of stitched data by seed
        """
        if isinstance(run_groups, RunGroup):
            run_groups = [run_groups]

        results = {}
        
        for run_group in tqdm(run_groups, desc="Processing run groups"):
            if self.verbose:
                logging.info(f"\nProcessing run group: {run_group.name}")
                
            # Get and group runs
            runs = self._get_runs(run_group)
            grouped_runs = self._group_runs_by_seed(runs)
            stitched_data = self._stitch_runs(grouped_runs, x_key, y_key, run_group.name, samples=samples)
            results[run_group.name] = stitched_data
            
            if self.verbose:
                logging.info(f"Completed processing {run_group.name}: {len(stitched_data)} seeds with valid data")
            
        return results
    
    def _transform_data(self, df: pd.DataFrame, x_key: str, y_key: str, 
                       interpolate_missing: bool = False,
                       smoothing_window: Optional[int] = None) -> pd.DataFrame:
        """Transform the data by interpolating missing values and/or applying smoothing.
        
        Args:
            df: Input DataFrame
            x_key: The key for the x-axis data
            y_key: The key for the y-axis data
            interpolate_missing: Whether to interpolate missing values
            smoothing_window: Window size for rolling mean smoothing. If None, no smoothing is applied.
            
        Returns:
            Transformed DataFrame
        """
        if interpolate_missing:
            # Interpolate NaNs linearly, forward & backward
            df[f"{y_key}_mean"] = (
                df.groupby("group_name")[f"{y_key}_mean"]
                .transform(lambda x: x.interpolate(method="linear", limit_direction="both"))
            )
            
            df[f"{y_key}_std"] = (
                df.groupby("group_name")[f"{y_key}_std"]
                .transform(lambda x: x.interpolate(method="linear", limit_direction="both"))
            )
        
        if smoothing_window is not None:
            # Apply rolling mean smoothing
            df[f"{y_key}_mean"] = (
                df.groupby("group_name")[f"{y_key}_mean"]
                .transform(lambda x: x.rolling(window=smoothing_window, min_periods=1, center=True).mean())
            )
            
            # For std, we use the mean of the std values in the window
            df[f"{y_key}_std"] = (
                df.groupby("group_name")[f"{y_key}_std"]
                .transform(lambda x: x.rolling(window=smoothing_window, min_periods=1, center=True).mean())
            )
        
        return df

    def compute_grouped_metrics(self, 
                              run_groups: List[RunGroup] | RunGroup | Dict[str, Dict[int, pd.DataFrame]], 
                              x_key: str, 
                              y_key: str,
                              interpolate_missing: bool = False,
                              min_seeds: Optional[int] = None,
                              smoothing_window: Optional[int] = None,
                              x_min: Optional[float] = None,
                              x_max: Optional[float] = None) -> pd.DataFrame:
        """Analyze metrics across multiple run groups.
        
        This is a specific use case of get_stitched_runs that computes statistics
        across seeds for each run group.
        
        Args:
            run_groups: Either:
                       - List of RunGroup objects or single RunGroup
                       - Pre-computed stitched runs from get_stitched_runs
            x_key: The key for the x-axis data
            y_key: The key for the y-axis data
            interpolate_missing: Whether to interpolate missing values
            min_seeds: Minimum number of seeds required for a valid measurement.
                      If None, all measurements are kept.
            smoothing_window: Window size for rolling mean smoothing. If None, no smoothing is applied.
            x_min: Minimum x value to include in the results. If None, no lower bound is applied.
            x_max: Maximum x value to include in the results. If None, no upper bound is applied.
            
        Returns:
            DataFrame containing the analyzed metrics
        """
        # Handle pre-computed stitched runs
        if isinstance(run_groups, dict) and all(isinstance(v, dict) for v in run_groups.values()):
            stitched_data = run_groups
        else:
            # Get stitched runs from run groups
            stitched_data = self.get_stitched_runs(run_groups, x_key, y_key)
            
        results_list = []
            
        for group_name, seed_data in stitched_data.items():
            if self.verbose:
                logging.info(f"\nAnalyzing metrics for group: {group_name}")
                
            # Aggregate data across seeds
            x_to_ys = defaultdict(list)
            for seed, df in seed_data.items():
                # Convert to numeric, handling errors
                df[x_key] = pd.to_numeric(df[x_key], errors='coerce')
                df[y_key] = pd.to_numeric(df[y_key], errors='coerce')
                
                # Skip NaN values
                valid_data = df.dropna(subset=[x_key, y_key])
                for x_val, y_val in zip(valid_data[x_key].values, valid_data[y_key].values):
                    x_to_ys[x_val].append(y_val)
            
            # Compute statistics
            xs = sorted(x_to_ys.keys())
            avgs = [np.mean(x_to_ys[x]) for x in xs]
            stds = [np.std(x_to_ys[x], ddof=0) for x in xs]
            counts = [len(x_to_ys[x]) for x in xs]
            
            if self.verbose:
                logging.info(f"  Found {len(xs)} unique x values")
                logging.info(f"  Number of seeds: {len(seed_data)}")
            
            for x, avg, std, count in zip(xs, avgs, stds, counts):
                result = {
                    "group_name": group_name,	
                    x_key: x,
                    f"{y_key}_mean": avg,
                    f"{y_key}_std": std,
                    f"{y_key}_count": count,
                    "num_seeds": len(seed_data)
                }
                results_list.append(result)
        
        # Convert to DataFrame
        results_df = pd.DataFrame(results_list)
        
        # Filter by x-axis range if specified
        if x_min is not None:
            results_df = results_df[results_df[x_key] >= x_min]
        if x_max is not None:
            results_df = results_df[results_df[x_key] <= x_max]
        
        # Filter by minimum seeds if specified
        if min_seeds is not None:
            mask = results_df[f"{y_key}_count"] < min_seeds
            results_df.loc[mask, f"{y_key}_mean"] = np.nan
            results_df.loc[mask, f"{y_key}_std"] = np.nan
        
        # Transform data (interpolate and smooth if requested)
        results_df = self._transform_data(
            results_df, 
            x_key, 
            y_key, 
            interpolate_missing=interpolate_missing,
            smoothing_window=smoothing_window
        )
                
        return results_df

# Example usage:
if __name__ == "__main__":
    import swizz
    import matplotlib.pyplot as plt

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Example 1: Using prefixes
    analyzer = WandbAnalyzer("claire-labo/pack", verbose=False)
    run_groups = [
        RunGroup(name="2", prefix="llama31bin2func"),
        RunGroup(name="4", prefix="llama31bin4func"),
        RunGroup(name="8", prefix="llama31bin8func"),
        RunGroup(name="16", prefix="llama31bin16func"),
        RunGroup(name="32", prefix="llama31bin32func"),
        RunGroup(name="48", prefix="llama31bin48func"),
        RunGroup(name="64", prefix="llama31bin64func"),
    ]

    stitched_runs = analyzer.get_stitched_runs(run_groups, x_key="round_num", y_key="Number of unique scores in program bank")
    
    # Get analyzed metrics
    results_df = analyzer.compute_grouped_metrics(stitched_runs, x_key="round_num", y_key="Number of unique scores in program bank", 
                                                  smoothing_window=15, interpolate_missing=True, x_min=0, x_max=1250, min_seeds=4)

    fig_scores, ax = swizz.plot(
        "multiple_std_lines_df",
        figsize=(8,5),
        data_df=results_df,
        label_key="group_name",
        x_key="round_num",
        y_key="Number of unique scores in program bank_mean",
        yerr_key="Number of unique scores in program bank_std",
        xlabel="Sampling Budget",
        ylabel="Number of unique scores",
        legend_title="Functions in Context",
        legend_ncol=2,
        legend_loc="lower right",
        x_formatter=lambda x, _: f"{x * 8:.0f}",
        y_formatter=lambda y, _: f"{-y/100:.1f}",
    )

    plt.show()
    print()

    # TODO: Return stiching as df instead of dict and group by custom stuff