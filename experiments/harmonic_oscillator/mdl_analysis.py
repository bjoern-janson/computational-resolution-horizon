"""
MDL Horizon Analysis
====================

Computes the information-theoretic resolution horizon for the
harmonic oscillator calibration experiment.

Inputs:
    - estimated generator representations
    - invariant descriptions
    - trajectory data

Outputs:
    - Delta L(k)
    - C_G(k)
    - eta(k)
    - k*

This implements the operational measurement:

    k* = argmax_k DeltaL(k) / C_G(k)

Author: Computational Phase Boundary Project
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class MDLResult:
    k: int
    delta_L: float
    C_G: float
    eta: float


class MDLAnalyzer:
    """
    Evaluates the structural efficiency frontier.

    Delta L:
        Description length saved by invariant discovery.

    C_G:
        Description length required to specify
        remaining gauge ambiguity.

    eta:
        Structural efficiency.
    """

    def __init__(
        self,
        baseline_length: float = 10000.0,
        delta_resolution: float = 1e-3
    ):
        self.baseline_length = baseline_length
        self.delta_resolution = delta_resolution


    def compute_data_description_length(
        self,
        reconstruction_error: float,
        n_samples: int
    ) -> float:
        """
        Gaussian MDL approximation:

        L ~ N log(error)

        Lower error means shorter description length.
        """

        error = max(reconstruction_error, 1e-12)

        return (
            n_samples *
            np.log(error)
        )


    def compute_delta_L(
        self,
        baseline_error: float,
        invariant_error: float,
        n_samples: int
    ) -> float:
        """
        Compression gained from invariant model.
        """

        L_baseline = self.compute_data_description_length(
            baseline_error,
            n_samples
        )

        L_structure = self.compute_data_description_length(
            invariant_error,
            n_samples
        )

        return L_baseline - L_structure


    def compute_gauge_complexity(
        self,
        k: int,
        epsilon_k: float,
        parameter_dimension: int = 3
    ) -> float:
        """
        Two-part MDL gauge code:

            C_G(k)=L(theta_G)+log N(delta,G,d)

        Simplified covering-number approximation.
        """

        structural_cost = (
            parameter_dimension *
            np.log2(k + 1)
        )

        covering_cost = (
            np.log2(
                1 / epsilon_k
            )
            *
            parameter_dimension
        )

        return structural_cost + covering_cost


    def analyze_depth(
        self,
        depths: List[int],
        reconstruction_errors: Dict[int, float],
        epsilon_values: Dict[int, float],
        n_samples: int
    ) -> List[MDLResult]:

        results = []

        baseline_error = max(
            reconstruction_errors[0],
            1e-12
        )

        for k in depths:

            delta_L = self.compute_delta_L(
                baseline_error,
                reconstruction_errors[k],
                n_samples
            )

            C_G = self.compute_gauge_complexity(
                k,
                epsilon_values[k]
            )

            eta = delta_L / C_G

            results.append(
                MDLResult(
                    k=k,
                    delta_L=delta_L,
                    C_G=C_G,
                    eta=eta
                )
            )

        return results


    def extract_horizon(
        self,
        results: List[MDLResult]
    ) -> int:
        """
        Resolution horizon:

            k*=argmax eta(k)
        """

        return max(
            results,
            key=lambda x: x.eta
        ).k



if __name__ == "__main__":

    print(
        "[MDL HORIZON ANALYSIS]"
    )

    depths = list(range(0, 10))


    # Synthetic calibration data.
    # Replace with estimate_generator.py output.

    reconstruction_errors = {
        0: 1.0,
        1: 0.45,
        2: 0.18,
        3: 0.10,
        4: 0.12,
        5: 0.20,
        6: 0.35,
        7: 0.55,
        8: 0.80,
        9: 1.10
    }


    epsilon_values = {
        k:
        0.002 * (1.35 ** k)
        for k in depths
    }


    analyzer = MDLAnalyzer()


    results = analyzer.analyze_depth(
        depths,
        reconstruction_errors,
        epsilon_values,
        n_samples=100000
    )


    k_star = analyzer.extract_horizon(
        results
    )


    print()
    print(
        "Depth | ΔL(k) | C_G(k) | η(k)"
    )
    print("--------------------------------")


    for r in results:

        print(
            f"{r.k:5d} | "
            f"{r.delta_L:7.2f} | "
            f"{r.C_G:7.3f} | "
            f"{r.eta:8.3f}"
        )


    print()
    print(
        f"Measured resolution horizon k*: {k_star}"
    )
