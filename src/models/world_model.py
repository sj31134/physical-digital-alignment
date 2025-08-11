"""World model module for the physical–digital alignment study.

This module implements a simple linear regression model as a stand‑in
for the more complex world models (e.g., transformers) described in
the research plan. The model is trained using ordinary least squares
and can be used to generate predictions and compute error metrics.

Classes
-------
LinearWorldModel
    Encapsulates fitting and prediction logic for a univariate linear
    regression model.

Functions
---------
rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float
    Compute the root mean squared error between true and predicted
    values.

mae(y_true: np.ndarray, y_pred: np.ndarray) -> float
    Compute the mean absolute error between true and predicted values.
"""

from __future__ import annotations

import numpy as np
from typing import Tuple


class LinearWorldModel:
    """Simple linear regression model.

    This class fits a line to a univariate dataset of the form
    ``y = a * x + b`` using the closed‑form least squares solution. It
    provides methods for fitting the model, making predictions, and
    retrieving parameters.
    """

    def __init__(self) -> None:
        self.coef_: float | None = None
        self.intercept_: float | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """Fit the linear model to the data.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, 1)
            Input features.
        y : np.ndarray of shape (n_samples,)
            Target values.
        """
        if X.ndim != 2 or X.shape[1] != 1:
            raise ValueError("X must be a 2D array with a single feature column")
        if y.ndim != 1:
            raise ValueError("y must be a 1D array")

        # Append a bias (column of ones) to X for intercept calculation
        X_design = np.hstack([X, np.ones((X.shape[0], 1))])

        # Compute the least squares solution: beta = (X^T X)^{-1} X^T y
        beta = np.linalg.pinv(X_design.T @ X_design) @ X_design.T @ y
        self.coef_, self.intercept_ = float(beta[0]), float(beta[1])

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Generate predictions using the fitted model.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, 1)
            Input features.

        Returns
        -------
        np.ndarray
            Predicted values of shape (n_samples,).
        """
        if self.coef_ is None or self.intercept_ is None:
            raise RuntimeError("Model must be fitted before calling predict().")
        return self.coef_ * X[:, 0] + self.intercept_

    def get_params(self) -> Tuple[float, float]:
        """Return the learned parameters (coefficient and intercept)."""
        if self.coef_ is None or self.intercept_ is None:
            raise RuntimeError("Model must be fitted before getting parameters.")
        return self.coef_, self.intercept_


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute root mean squared error."""
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute mean absolute error."""
    return float(np.mean(np.abs(y_true - y_pred)))


__all__ = ["LinearWorldModel", "rmse", "mae"]
