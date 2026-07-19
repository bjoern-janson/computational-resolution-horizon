"""
Generator field estimation for the harmonic oscillator benchmark.

Purpose
-------
Estimate the dynamical vector field

    F(x,p) = (p, -omega^2 x)

from noisy trajectory observations.

This module intentionally implements a simple baseline estimator.
The goal is not maximum predictive performance, but controlled
measurement of the resolution horizon k* under changes in:

    - sample size N
    - noise sigma
    - regularization lambda_N

Pipeline position:

    trajectory data
          |
          v
    estimate_generator.py
          |
          v
    F_hat_N^sigma
          |
          v
    Lie depth / invariant extraction
"""


import numpy as np
from dataclasses import dataclass
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge


@dataclass
class GeneratorEstimate:
    """
    Container for estimated vector field.
    """

    model: Ridge
    polynomial_map: PolynomialFeatures
    omega: float
    regularization: float


class PolynomialGeneratorEstimator:
    """
    Polynomial regression estimator for continuous dynamics.

    Approximates:

        dx/dt = f_theta(x)

    where x = (position, momentum)

    The estimator is deliberately simple so that the effect of
    derivative amplification can be measured independently from
    model complexity.
    """

    def __init__(
        self,
        degree: int = 3,
        lambda_N: float = 1e-6,
        omega: float = 1.0,
    ):

        self.degree = degree
        self.lambda_N = lambda_N
        self.omega = omega

        self.poly = PolynomialFeatures(
            degree=degree,
            include_bias=True
        )

        self.model = Ridge(
            alpha=lambda_N
        )


    def fit(
        self,
        states: np.ndarray,
        derivatives: np.ndarray,
    ):
        """
        Fit:

            x_dot = F_hat(x)

        Parameters
        ----------
        states:
            Array shape (N,2)

            Columns:
                x position
                p momentum

        derivatives:
            Array shape (N,2)

            Columns:

                dx/dt
                dp/dt
        """

        features = self.poly.fit_transform(states)

        self.model.fit(
            features,
            derivatives
        )

        return GeneratorEstimate(
            model=self.model,
            polynomial_map=self.poly,
            omega=self.omega,
            regularization=self.lambda_N
        )


    def predict(
        self,
        states: np.ndarray
    ):
        """
        Evaluate estimated vector field.
        """

        features = self.poly.transform(states)

        return self.model.predict(features)



def estimate_generator(
    states,
    derivatives,
    degree=3,
    lambda_N=1e-6,
    omega=1.0
):
    """
    Convenience interface.
    """

    estimator = PolynomialGeneratorEstimator(
        degree=degree,
        lambda_N=lambda_N,
        omega=omega
    )

    return estimator.fit(
        states,
        derivatives
    )


if __name__ == "__main__":

    print(
        "Generator estimation module ready."
    )

    print(
        """
Expected input:

states:
[
 [x_1,p_1],
 [x_2,p_2],
 ...
]

derivatives:
[
 [dx/dt_1,dp/dt_1],
 [dx/dt_2,dp/dt_2],
 ...
]

Output:

F_hat_N^sigma(x)

"""
    )
