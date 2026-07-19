"""
Computational Phase Boundary

Experiment: Harmonic Oscillator Calibration

Purpose:
    Generate controlled trajectory data for the Phase I calibration experiment.

System:
    dx/dt = p
    dp/dt = -omega^2 x

The script produces:
    - clean trajectories
    - noisy observations
    - optional nonlinear coordinate distortions

These datasets are intended for:
    - generator reconstruction
    - invariant extraction
    - gauge estimation
    - resolution horizon measurement

"""

import argparse
from pathlib import Path
from typing import Tuple

import numpy as np


# ------------------------------------------------------------
# Harmonic oscillator dynamics
# ------------------------------------------------------------

def harmonic_oscillator(
    state: np.ndarray,
    omega: float
) -> np.ndarray:
    """
    Continuous-time dynamics.

    Parameters
    ----------
    state:
        Array [x, p]

    omega:
        Oscillator frequency

    Returns
    -------
    derivative:
        Array [dx/dt, dp/dt]
    """

    x, p = state

    return np.array([
        p,
        -(omega ** 2) * x
    ])


# ------------------------------------------------------------
# Numerical integrator
# ------------------------------------------------------------

def rk4_step(
    state: np.ndarray,
    dt: float,
    omega: float
) -> np.ndarray:
    """
    Fourth-order Runge-Kutta integration step.
    """

    k1 = harmonic_oscillator(state, omega)

    k2 = harmonic_oscillator(
        state + 0.5 * dt * k1,
        omega
    )

    k3 = harmonic_oscillator(
        state + 0.5 * dt * k2,
        omega
    )

    k4 = harmonic_oscillator(
        state + dt * k3,
        omega
    )

    return state + (
        dt / 6.0
    ) * (
        k1 +
        2 * k2 +
        2 * k3 +
        k4
    )


# ------------------------------------------------------------
# Coordinate transformations
# ------------------------------------------------------------

def nonlinear_coordinate_transform(
    trajectory: np.ndarray,
    alpha: float = 0.2
) -> np.ndarray:
    """
    Apply nonlinear coordinate distortion.

    Transformation:

        y1 = x + alpha*x^3
        y2 = p + alpha*p^3

    This tests whether invariant recovery
    survives coordinate changes.
    """

    transformed = trajectory.copy()

    x = trajectory[:, 0]
    p = trajectory[:, 1]

    transformed[:, 0] = x + alpha * x**3
    transformed[:, 1] = p + alpha * p**3

    return transformed


# ------------------------------------------------------------
# Dataset generation
# ------------------------------------------------------------

def generate_trajectory(
    N: int,
    dt: float,
    omega: float,
    x0: float,
    p0: float
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate clean oscillator trajectory.
    """

    states = np.zeros((N, 2))
    times = np.arange(N) * dt

    state = np.array([x0, p0], dtype=float)

    for i in range(N):
        states[i] = state
        state = rk4_step(
            state,
            dt,
            omega
        )

    return times, states


def add_noise(
    trajectory: np.ndarray,
    sigma: float
) -> np.ndarray:
    """
    Add Gaussian measurement noise.
    """

    noise = np.random.normal(
        0,
        sigma,
        trajectory.shape
    )

    return trajectory + noise


# ------------------------------------------------------------
# Energy invariant
# ------------------------------------------------------------

def compute_energy(
    trajectory: np.ndarray,
    omega: float
) -> np.ndarray:
    """
    Compute analytical Hamiltonian invariant.

    H = 1/2 p^2 + 1/2 omega^2 x^2
    """

    x = trajectory[:, 0]
    p = trajectory[:, 1]

    return (
        0.5 * p**2
        +
        0.5 * omega**2 * x**2
    )


# ------------------------------------------------------------
# Save experiment data
# ------------------------------------------------------------

def save_dataset(
    path: Path,
    times: np.ndarray,
    clean: np.ndarray,
    noisy: np.ndarray,
    transformed: np.ndarray,
    energy: np.ndarray
):
    """
    Save generated experiment data.
    """

    path.mkdir(
        parents=True,
        exist_ok=True
    )

    np.save(
        path / "time.npy",
        times
    )

    np.save(
        path / "clean_states.npy",
        clean
    )

    np.save(
        path / "noisy_states.npy",
        noisy
    )

    np.save(
        path / "coordinate_warp.npy",
        transformed
    )

    np.save(
        path / "energy.npy",
        energy
    )


# ------------------------------------------------------------
# Main experiment runner
# ------------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description=
        "Generate harmonic oscillator calibration data."
    )

    parser.add_argument(
        "--N",
        type=int,
        default=100000,
        help="Number of samples"
    )

    parser.add_argument(
        "--dt",
        type=float,
        default=0.001,
        help="Integration timestep"
    )

    parser.add_argument(
        "--omega",
        type=float,
        default=1.0,
        help="Oscillator frequency"
    )

    parser.add_argument(
        "--sigma",
        type=float,
        default=0.02,
        help="Measurement noise"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="data",
        help="Output directory"
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42
    )

    args = parser.parse_args()


    np.random.seed(args.seed)


    print(
        "[HARMONIC OSCILLATOR DATA GENERATION]"
    )

    print(
        f"N={args.N}"
    )

    print(
        f"omega={args.omega}"
    )

    print(
        f"sigma={args.sigma}"
    )


    times, clean = generate_trajectory(
        N=args.N,
        dt=args.dt,
        omega=args.omega,
        x0=1.0,
        p0=0.0
    )


    noisy = add_noise(
        clean,
        args.sigma
    )


    warped = nonlinear_coordinate_transform(
        clean
    )


    energy = compute_energy(
        clean,
        args.omega
    )


    save_dataset(
        Path(args.output),
        times,
        clean,
        noisy,
        warped,
        energy
    )


    print(
        "[DONE]"
    )

    print(
        f"Saved dataset to {args.output}"
    )

    print(
        "Invariant baseline:"
    )

    print(
        f"Energy mean={np.mean(energy):.6f}"
    )

    print(
        f"Energy std={np.std(energy):.6e}"
    )


if __name__ == "__main__":
    main()
