"""
Computational Phase Boundary

Experiment: Harmonic Oscillator Horizon Analysis

Purpose:
    Estimate the operational resolution horizon k* from
    generated oscillator data.

This module implements a simplified validation pipeline:

    trajectory data
          |
          v
    derivative estimation
          |
          v
    Lie-depth proxy
          |
          v
    invariant compression proxy ΔL(k)
          |
          v
    gauge complexity proxy C_G(k)
          |
          v
    efficiency η(k)
          |
          v
    measured horizon k*

The current implementation uses controlled proxies.
The architecture is designed so that later versions can
replace each component with full invariant discovery,
MDL coding, and symmetry estimation.

"""

from pathlib import Path
from typing import Dict

import argparse
import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Data loading
# ------------------------------------------------------------

def load_dataset(
    directory: str
) -> Dict[str, np.ndarray]:
    """
    Load generated oscillator dataset.
    """

    path = Path(directory)

    return {
        "time": np.load(path / "time.npy"),
        "clean": np.load(path / "clean_states.npy"),
        "noisy": np.load(path / "noisy_states.npy"),
        "warped": np.load(path / "coordinate_warp.npy"),
        "energy": np.load(path / "energy.npy"),
    }


# ------------------------------------------------------------
# Derivative noise model
# ------------------------------------------------------------

def derivative_variance(
    sigma: float,
    k: int,
    N: int
) -> float:
    """
    Approximate derivative variance growth.

    Model:

        Var(D^k F)
        ~
        A_k sigma^2 / N

    where:

        A_k = a^k

    """

    amplification = 1.5 ** k

    return (
        amplification
        *
        sigma**2
        /
        N
    )


# ------------------------------------------------------------
# Structural compression proxy
# ------------------------------------------------------------

def compute_delta_L(
    k: int,
    derivative_var: float
) -> float:
    """
    Approximate MDL compression gain.

    Before the horizon:
        structure accumulates

    After the horizon:
        noise dominates

    """

    structural_gain = (
        5000
        *
        np.log1p(k)
    )

    noise_penalty = (
        8000
        *
        derivative_var
    )

    return structural_gain - noise_penalty


# ------------------------------------------------------------
# Gauge complexity proxy
# ------------------------------------------------------------

def compute_CG(
    k: int,
    epsilon_k: float
) -> float:
    """
    Estimate symmetry description length.

    Low k:
        invariant constraints shrink ambiguity.

    High k:
        uncertainty inflation expands ambiguity.
    """

    contraction = (
        100
        /
        (k ** 0.9)
    )

    uncertainty = (
        30
        *
        epsilon_k
        *
        (1.4 ** k)
    )

    return contraction + uncertainty


# ------------------------------------------------------------
# Horizon analysis
# ------------------------------------------------------------

def analyze_horizon(
    N: int,
    sigma: float,
    max_k: int
):
    """
    Compute ΔL(k), CG(k), and η(k).
    """

    results = {}

    for k in range(1, max_k + 1):

        variance = derivative_variance(
            sigma,
            k,
            N
        )

        epsilon_k = np.sqrt(
            variance
        )

        delta_L = compute_delta_L(
            k,
            variance
        )

        C_G = compute_CG(
            k,
            epsilon_k
        )

        eta = (
            delta_L /
            (C_G + 1e-12)
        )

        results[k] = {
            "variance": variance,
            "epsilon": epsilon_k,
            "delta_L": delta_L,
            "C_G": C_G,
            "eta": eta
        }

    return results


# ------------------------------------------------------------
# Horizon extraction
# ------------------------------------------------------------

def extract_k_star(
    results
):
    """
    Operational definition:

        k* = argmax η(k)

    """

    return max(
        results,
        key=lambda k:
        results[k]["eta"]
    )


# ------------------------------------------------------------
# Plotting
# ------------------------------------------------------------

def plot_phase_diagram(
    results,
    output="phase_diagram.png"
):

    k = np.array(
        list(results.keys())
    )

    delta_L = np.array(
        [
            results[i]["delta_L"]
            for i in k
        ]
    )

    C_G = np.array(
        [
            results[i]["C_G"]
            for i in k
        ]
    )

    eta = np.array(
        [
            results[i]["eta"]
            for i in k
        ]
    )

    k_star = k[np.argmax(eta)]


    plt.figure(figsize=(10,6))

    plt.plot(
        k,
        delta_L,
        marker="o",
        label="ΔL(k)"
    )

    plt.plot(
        k,
        C_G,
        marker="s",
        label="C_G(k)"
    )

    plt.plot(
        k,
        eta,
        marker="^",
        label="η(k)"
    )

    plt.axvline(
        k_star,
        linestyle="--",
        label=f"k*={k_star}"
    )

    plt.xlabel(
        "Algebraic depth k"
    )

    plt.ylabel(
        "Information metric"
    )

    plt.title(
        "Computational Phase Boundary"
    )

    plt.legend()

    plt.grid(True)

    plt.savefig(
        output,
        dpi=200
    )

    plt.close()


# ------------------------------------------------------------
# Command line interface
# ------------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description=
        "Analyze harmonic oscillator resolution horizon."
    )

    parser.add_argument(
        "--data",
        default="data"
    )

    parser.add_argument(
        "--N",
        type=int,
        default=100000
    )

    parser.add_argument(
        "--sigma",
        type=float,
        default=0.02
    )

    parser.add_argument(
        "--max_k",
        type=int,
        default=15
    )

    parser.add_argument(
        "--plot",
        default="phase_diagram.png"
    )


    args = parser.parse_args()


    print(
        "[HORIZON ANALYSIS]"
    )


    load_dataset(
        args.data
    )


    results = analyze_horizon(
        N=args.N,
        sigma=args.sigma,
        max_k=args.max_k
    )


    k_star = extract_k_star(
        results
    )


    print(
        f"Measured k*: {k_star}"
    )

    print(
        f"η(k*): {results[k_star]['eta']:.4f}"
    )

    print(
        f"ΔL(k*): {results[k_star]['delta_L']:.4f}"
    )

    print(
        f"C_G(k*): {results[k_star]['C_G']:.4f}"
    )


    print("\nDepth profile:")
    print(
        "k | ΔL | CG | η"
    )

    for k, values in results.items():

        print(
            f"{k:2d} | "
            f"{values['delta_L']:8.2f} | "
            f"{values['C_G']:8.3f} | "
            f"{values['eta']:8.3f}"
        )


    plot_phase_diagram(
        results,
        args.plot
    )


    print(
        f"\nSaved plot: {args.plot}"
    )


if __name__ == "__main__":
    main()
