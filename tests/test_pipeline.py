"""Test the simulation and world model pipeline.

This module contains simple unit tests that verify the basic
functionality of the simulator and world model components. The tests
ensure that datasets are generated with correct shapes and that the
world model can be fitted and yield finite error metrics.
"""

from __future__ import annotations

import numpy as np

from collectors.simulator import simulate_dataset
from models.world_model import LinearWorldModel, rmse, mae


def test_simulation_shapes() -> None:
    """Ensure that simulate_dataset returns arrays of expected shapes."""
    data = simulate_dataset(n_samples=10, noise_level=0.1, complexity=1)
    X, y = data["X"], data["y"]
    assert X.shape == (10, 1)
    assert y.shape == (10,)


def test_model_fit_and_metrics() -> None:
    """Test that the LinearWorldModel can fit and compute metrics."""
    data = simulate_dataset(n_samples=50, noise_level=0.2, complexity=1)
    X, y = data["X"], data["y"]
    model = LinearWorldModel()
    model.fit(X, y)
    assert model.coef_ is not None
    assert model.intercept_ is not None
    y_pred = model.predict(X)
    # Metrics should be finite positive numbers
    assert np.isfinite(rmse(y, y_pred))
    assert np.isfinite(mae(y, y_pred))
