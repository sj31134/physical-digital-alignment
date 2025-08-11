"""Run experiments for the physical–digital alignment study.

This script orchestrates the simulation of datasets under multiple
conditions, trains a simple world model on the simulated data, and
computes evaluation metrics. The workflow loosely follows the
research plan described in the documentation.

Usage
-----
This script can be executed from the command line:

    python scripts/run_experiments.py --conditions 4 --samples 100

The results of each condition will be printed to stdout and saved
optionally as a CSV file in the `data` directory.
"""

from __future__ import annotations

import argparse
import csv
import os
import time
from typing import Dict, List

import numpy as np

# Ensure that the src directory is on the Python path so that modules can be imported
import sys
import pathlib
ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from collectors.simulator import simulate_experiment
from models.world_model import LinearWorldModel, rmse, mae


def run_condition(cond_idx: int, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
    """Train a world model on a given dataset and compute metrics.

    Parameters
    ----------
    cond_idx : int
        Index of the current condition.
    X : np.ndarray
        Feature matrix of shape (n_samples, 1).
    y : np.ndarray
        Target vector.

    Returns
    -------
    Dict[str, float]
        Dictionary containing metrics for the condition.
    """
    # Fit the linear world model
    model = LinearWorldModel()
    t_start = time.perf_counter()
    model.fit(X, y)
    fit_time = time.perf_counter() - t_start

    # Generate predictions
    y_pred = model.predict(X)

    # Compute error metrics
    metrics = {
        "condition": cond_idx,
        "coef": model.coef_,
        "intercept": model.intercept_,
        "rmse": rmse(y, y_pred),
        "mae": mae(y, y_pred),
        "fit_time": fit_time,
    }
    return metrics


def save_results(results: List[Dict[str, float]], output_path: str) -> None:
    """Save experiment results to a CSV file."""
    fieldnames = list(results[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run simulated world model experiments.")
    parser.add_argument("--conditions", type=int, default=4, help="Number of experimental conditions.")
    parser.add_argument("--samples", type=int, default=100, help="Number of samples per dataset.")
    parser.add_argument("--output", type=str, default="", help="Optional path to save results CSV.")
    args = parser.parse_args()

    print(f"Generating {args.conditions} conditions with {args.samples} samples each...")
    datasets = simulate_experiment(args.conditions, args.samples)
    results: List[Dict[str, float]] = []

    for idx, data in datasets.items():
        X = data["X"]
        y = data["y"]
        metrics = run_condition(idx, X, y)
        results.append(metrics)
        print(
            f"Condition {idx}: RMSE={metrics['rmse']:.4f}, MAE={metrics['mae']:.4f}, "
            f"coef={metrics['coef']:.3f}, intercept={metrics['intercept']:.3f}, "
            f"fit_time={metrics['fit_time']:.6f}s"
        )

    # Save results if specified
    if args.output:
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        save_results(results, args.output)
        print(f"Saved results to {args.output}")


if __name__ == "__main__":
    main()
