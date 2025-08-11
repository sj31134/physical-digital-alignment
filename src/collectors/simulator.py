"""Simulator module for generating synthetic data.

This module provides functions to simulate data for the physical–digital
alignment research. The simulation aims to mimic the effect of
robot​ebabled data collection versus manual data collection under
different noise and complexity conditions. The resulting dataset can
then be used to train and evaluate a world model.

Functions
---------
simulate_dataset(n_samples: int, noise_level: float, complexity: int) -> dict
    Generate a synthetic dataset with a single numerical feature and a
    continuous target. The feature–target relationship can be linear
    or nonlinear depending on the ``complexity`` argument. Random
    Gaussian noise is added to the target to emulate measurement
    errors. Returns a dictionary with keys ``X`` and ``y`` containing
    numpy arrays.

simulate_experiment(num_conditions: int, n_samples: int) -> dict
    Create a set of experimental conditions by varying noise levels and
    complexity. Returns a dictionary keyed by condition index where
    each value is the dataset dictionary returned by
    ``simulate_dataset``.
"""

from __future__ import annotations

import numpy as np
from typing import Dict, Tuple


def simulate_dataset(n_samples: int, noise_level: float, complexity: int) -> Dict[str, np.ndarray]:
    """Generate a synthetic regression dataset.

    Parameters
    ----------
    n_samples : int
        Number of samples to generate.
    noise_level : float
        Standard deviation of Gaussian noise added to the target.
    complexity : int
        Complexity of the relationship. ``1`` yields a linear
        relationship; any value greater than ``1`` introduces a
        nonlinear term (quadratic).

    Returns
    -------
    Dict[str, np.ndarray]
        A dictionary containing feature matrix ``X`` of shape
        (n_samples, 1) and target vector ``y`` of shape (n_samples,).
    """
    # Ensure reproducibility
    rng = np.random.default_rng(seed=42)
    X = rng.uniform(low=0.0, high=10.0, size=(n_samples, 1))

    # Define a base linear relationship y = 2 * x + 5
    y = 2.0 * X[:, 0] + 5.0

    if complexity > 1:
        # Introduce non‑linearity by adding a quadratic term
        y += 0.3 * (X[:, 0] ** 2)

    # Add Gaussian noise
    y_noisy = y + rng.normal(loc=0.0, scale=noise_level, size=n_samples)

    return {"X": X, "y": y_noisy}


def simulate_experiment(num_conditions: int, n_samples: int) -> Dict[int, Dict[str, np.ndarray]]:
    """Generate multiple datasets under varying conditions.

    This helper iterates over a fixed set of noise levels and complexity
    levels to produce ``num_conditions`` datasets. The intention is to
    emulate different operational scenarios (e.g., high noise vs. low
    noise, simple vs. complex dynamics). If more conditions are
    requested than combinations available, the patterns repeat.

    Parameters
    ----------
    num_conditions : int
        Number of experimental conditions (datasets) to generate.
    n_samples : int
        Number of samples per dataset.

    Returns
    -------
    Dict[int, Dict[str, np.ndarray]]
        Dictionary keyed by condition index with dataset dictionaries.
    """
    # Predefined levels; adjust these lists to expand the design space
    noise_levels = [0.5, 1.0]  # simulate low vs. high sensor noise
    complexities = [1, 2]      # linear vs. nonlinear dynamics
    datasets: Dict[int, Dict[str, np.ndarray]] = {}

    for i in range(num_conditions):
        noise = noise_levels[i % len(noise_levels)]
        complexity = complexities[i // len(noise_levels) % len(complexities)]
        datasets[i] = simulate_dataset(n_samples, noise, complexity)

    return datasets


__all__ = ["simulate_dataset", "simulate_experiment"]
