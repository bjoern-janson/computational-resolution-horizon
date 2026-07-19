"""
Compute Lie algebra depth for the estimated harmonic oscillator generator.

Phase 1 objective:
    Verify that the invariant discovery pipeline can track finite algebraic
    closure on a known dynamical system.

The harmonic oscillator:

    dx/dt = p
    dp/dt = -omega^2 x

has a linear generator field:

    F(x,p) = (p, -omega^2 x)

The Lie closure should stabilize quickly because the vector field belongs
to a finite-dimensional linear algebra.

This module provides the experimental abstraction:

    F_hat
      |
      v
    Lie_k(F_hat)
      |
      v
    closure depth k*

"""

import numpy as np
from typing import List, Dict


class VectorField:
    """
    Minimal vector field representation.

    Components are functions:
        F(x) = [f1(x), f2(x), ...]
    """

    def __init__(self, components):
        self.components = components

    def evaluate(self, x):
        return np.array([f(x) for f in self.components])


def numerical_jacobian(field: VectorField, x, eps=1e-6):
    """
    Finite difference Jacobian estimate.
    """

    x = np.asarray(x, dtype=float)
    n = len(x)

    J = np.zeros((n, n))

    for i in range(n):
        dx_plus = x.copy()
        dx_minus = x.copy()

        dx_plus[i] += eps
        dx_minus[i] -= eps

        J[:, i] = (
            field.evaluate(dx_plus)
            -
            field.evaluate(dx_minus)
        ) / (2 * eps)

    return J


def lie_bracket(F: VectorField, G: VectorField):
    """
    Compute Lie bracket:

        [F,G] = DG F - DF G

    using numerical Jacobians.
    """

    def bracket(x):

        JF = numerical_jacobian(F, x)
        JG = numerical_jacobian(G, x)

        return JG @ F.evaluate(x) - JF @ G.evaluate(x)

    return VectorField(
        [
            lambda x, i=i: bracket(x)[i]
            for i in range(len(bracket(np.zeros(2))))
        ]
    )


def sample_vector_field(field, samples):
    """
    Evaluate field on a collection of points.

    Used for estimating linear independence of generated fields.
    """

    values = []

    for x in samples:
        values.append(field.evaluate(x))

    return np.concatenate(values)


def estimate_rank(fields, samples, tolerance=1e-8):
    """
    Estimate dimension of generated Lie span.
    """

    matrix = np.column_stack(
        [
            sample_vector_field(F, samples)
            for F in fields
        ]
    )

    return np.linalg.matrix_rank(
        matrix,
        tol=tolerance
    )


def compute_lie_depth(
    generator: VectorField,
    max_depth=8,
    samples=None
):
    """
    Build Lie closure tree.

    Returns:

        {
          depth:
              estimated algebra rank
        }

    """

    if samples is None:
        samples = [
            np.array([x, p])
            for x in np.linspace(-2,2,8)
            for p in np.linspace(-2,2,8)
        ]

    closure = [generator]

    results = {}

    for k in range(max_depth + 1):

        rank = estimate_rank(
            closure,
            samples
        )

        results[k] = rank

        print(
            f"Lie depth {k}: "
            f"closure dimension = {rank}"
        )

        new_fields = []

        for F in closure:
            new_fields.append(
                lie_bracket(generator, F)
            )

        closure.extend(new_fields)

        # remove numerical duplicates
        unique = []

        for F in closure:

            if estimate_rank(
                unique + [F],
                samples
            ) > estimate_rank(
                unique,
                samples
            ):
                unique.append(F)

        closure = unique

    return results


def harmonic_generator(omega=1.0):

    return VectorField(
        [
            lambda z: z[1],
            lambda z: -omega**2 * z[0]
        ]
    )


if __name__ == "__main__":

    print(
        "[LIE DEPTH ANALYSIS — HARMONIC OSCILLATOR]"
    )
    print("=" * 60)

    F_hat = harmonic_generator(
        omega=1.0
    )

    lie_profile = compute_lie_depth(
        F_hat,
        max_depth=6
    )

    print("\nFinal Lie closure profile:")
    print(lie_profile)

    print(
        "\nExpected behavior:"
    )
    print(
        "Finite-dimensional closure should appear quickly."
    )
