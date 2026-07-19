# Computational Phase Boundary

# Mathematical Notation Reference

## Version 0.1 — Symbol Dictionary

---

# 1. Purpose

This document defines the notation used throughout the Computational Phase Boundary framework.

The goal is to maintain a strict separation between:

1. Physical objects.
2. Estimated objects.
3. Observer-dependent quantities.
4. Information-theoretic measurements.
5. Experimental control variables.

---

# 2. Core Dynamical Objects

| Symbol | Meaning |
|---|---|
| \(\mathcal M\) | State manifold |
| \(x\) | State variable |
| \(t\) | Time |
| \(F\) | True dynamical vector field |
| \(\hat F_N^\sigma\) | Estimated vector field from finite noisy data |
| \(\mathcal D_N\) | Dataset of observed trajectories |

The underlying system:

\[
\boxed{
\dot{x}=F(x)
}
\]

The observer never accesses \(F\) directly.

The observer reconstructs:

\[
\boxed{
\hat F_N^\sigma
}
\]

---

# 3. Observation Parameters

## Sample Size

\[
N
\]

Number of observations.

Increasing:

\[
N\uparrow
\]

should improve structural resolution.

Prediction:

\[
\frac{\partial k^*}{\partial N}>0
\]

---

## Noise Level

\[
\sigma
\]

Measurement uncertainty amplitude.

Increasing:

\[
\sigma\uparrow
\]

reduces recoverable structure.

Prediction:

\[
\frac{\partial k^*}{\partial\sigma}<0
\]

---

## Coverage Error

\[
E_{\mathrm{cov}}
\]

Measures mismatch between sampled trajectory support and the true state manifold.

Large:

\[
E_{\mathrm{cov}}
\]

means poor global exploration.

---

## Excitation Matrix

\[
\Gamma
\]

Represents diversity of interventions.

The quantity:

\[
\lambda_{\min}(\Gamma)
\]

is the smallest eigenvalue.

Interpretation:

larger values indicate more complete directional excitation.

---

# 4. Reconstruction Operators

## Regularized Reconstruction

\[
\mathcal R_{\lambda_N}
\]

Maps observations into an estimated generator:

\[
\boxed{
\mathcal R_{\lambda_N}:
\mathcal D_N
\rightarrow
\hat F_N^\sigma
}
\]

---

## Regularization Parameter

\[
\lambda_N
\]

Controls smoothing or complexity penalty.

Examples:

- derivative penalties,
- Sobolev regularization,
- kernel bandwidth,
- neural operator constraints.

---

# 5. Algebraic Depth

## Lie Closure

\[
\mathrm{Lie}_k(\hat F)
\]

The algebraic structure accessible at depth \(k\).

The hierarchy:

\[
\mathrm{Lie}_0
\subseteq
\mathrm{Lie}_1
\subseteq
...
\subseteq
\mathrm{Lie}_k
\]

---

## Resolution Depth

\[
k
\]

Represents the depth of structural extraction.

Higher:

\[
k
\]

means:

- deeper derivatives,
- more invariant constraints,
- greater numerical instability.

---

## Resolution Horizon

\[
\boxed{k^*}
\]

The maximum useful structural depth.

Defined by:

\[
k^*
=
\arg\max_k\eta(k)
\]

---

# 6. Invariant Objects

## Ideal Invariant Space

\[
\mathrm{Inv}
(
\mathrm{Lie}_k(F)
)
\]

All invariant quantities preserved by the depth-\(k\) algebra.

---

## Estimated Invariant Space

\[
\widehat{\mathrm{Inv}}_k
\]

Finite-data approximation.

Depends on:

- \(N\),
- \(\sigma\),
- estimator quality.

---

# 7. Symmetry and Gauge Notation

## Diffeomorphism Group

\[
\mathrm{Diff}^{k+1}(\mathcal M)
\]

The set of smooth coordinate transformations with derivatives through order \(k+1\).

---

## Pushforward Operator

\[
g_*
\]

Transforms structures under coordinate change.

---

## Ideal Gauge Group

\[
G^{(k)}
\]

The exact transformations preserving depth-\(k\) invariants:

\[
G^{(k)}
=
\{
g:
g_*\phi=\phi
\}
\]

---

## Estimated Gauge Group

\[
\hat G^{(k)}(\epsilon_k)
\]

Finite-data confidence region:

\[
\boxed{
\hat G^{(k)}(\epsilon_k)
=
\{
g:
d(\phi,g_*\phi)<\epsilon_k
\}
}
\]

---

## Confidence Radius

\[
\epsilon_k
\]

Tolerance describing uncertainty in invariant preservation.

Typical model:

\[
\boxed{
\epsilon_k
=
C_k\frac{\sigma}{\sqrt N}
+
\epsilon_{\mathrm{model}}
}
\]

---

# 8. Metric Notation

## Jet Metric

\[
d_{C^{k+1}}
\]

Measures distance between transformations including derivatives up to order:

\[
k+1
\]

---

## Compact Transformation Budget

\[
B_R
\]

Restricts allowed transformations to an experimentally meaningful region.

The operational gauge:

\[
\boxed{
\hat G^{(k)}
\cap B_R
}
\]

---

# 9. Information-Theoretic Quantities

## Description Length

\[
L(X)
\]

Number of bits required to encode object \(X\).

---

## Compression Gain

\[
\Delta L(k)
\]

Information gained by discovering structure:

\[
\boxed{
\Delta L(k)
=
L(\mathcal D_N|\mathrm{Baseline})
-
L(\mathcal D_N|\mathrm{Structure}_k)
}
\]

---

## Gauge Complexity

\[
C_G(k)
\]

Description length of remaining symmetry uncertainty:

\[
\boxed{
C_G(k)
=
L(\theta_G)
+
\log N(\delta,\hat G^{(k)},d_{C^{k+1}})
}
\]

---

## Covering Number

\[
N(\delta,X,d)
\]

Number of metric balls of radius:

\[
\delta
\]

required to cover:

\[
X
\]

under metric:

\[
d
\]

---

# 10. Structural Efficiency

\[
\boxed{
\eta(k)
}
\]

Information gained per unit symmetry complexity:

\[
\eta(k)
=
\frac{\Delta L(k)}
{C_G(k)}
\]

---

# 11. Error Decomposition

The framework separates failure into:

\[
\boxed{
\mathcal E
=
\begin{pmatrix}
E_{\mathrm{learn}}\\
E_{\mathrm{gauge}}\\
E_{\mathrm{truncate}}\\
E_{\mathrm{cover}}
\end{pmatrix}
}
\]

---

## Learning Error

\[
E_{\mathrm{learn}}
\]

Failure to estimate the dynamics.

Cause:

- insufficient data,
- poor estimator,
- excessive noise.

---

## Gauge Error

\[
E_{\mathrm{gauge}}
\]

Failure of coordinate transfer.

Cause:

- insufficient excitation,
- incorrect symmetry class.

---

## Truncation Error

\[
E_{\mathrm{truncate}}
\]

Failure caused by exceeding recoverable algebraic depth.

Cause:

- derivative amplification,
- unstable high-order structure.

---

## Coverage Error

\[
E_{\mathrm{cover}}
\]

Failure caused by incomplete exploration.

Cause:

- local sampling,
- missing manifold regions.

---

# 12. Phase Diagram Symbols

## Structural Acquisition

\[
\Delta L'(k)>0
\]

\[
C_G'(k)<0
\]

Real invariants are being discovered.

---

## Resolution Horizon

\[
\Delta L'(k)\approx0
\]

\[
C_G'(k)\approx0
\]

The optimal balance point.

---

## Misresolution

\[
\Delta L'(k)<0
\]

\[
C_G'(k)>0
\]

Noise is interpreted as structure.

---

# 13. Experimental System Symbols

## Harmonic Oscillator

\[
\dot{x}=p
\]

\[
\dot p=-\omega^2x
\]

Invariant:

\[
H=
\frac12p^2+
\frac12\omega^2x^2
\]

---

## Euler Top

\[
\dot L=L\times I^{-1}L
\]

Invariants:

\[
T=
\frac12L\cdot I^{-1}L
\]

and:

\[
M^2=||L||^2
\]

---

# 14. Final Object

The complete observable structure:

\[
\boxed{
\mathfrak O_{\mathrm{comp}}
=
\left(
\frac{
\mathrm{Lie}_{k^*}
(
\mathcal R_{\lambda_N}(\hat F_N^\sigma)
)
}
{
\hat G^{(k^*)}(\epsilon_{k^*})
},
k^*,
\epsilon
\right)
}
\]

---

# 15. Notation Principles

The framework follows five notation rules:

## Rule 1

True objects and estimated objects are never conflated.

\[
F\neq\hat F
\]

---

## Rule 2

Intrinsic symmetry and observable symmetry are distinct.

\[
G^{(k)}
\neq
\hat G^{(k)}
\]

---

## Rule 3

Complexity depth is not automatically meaningful.

\[
k>k^*
\]

does not imply additional recoverable structure.

---

## Rule 4

Measurement resolution is resource-dependent.

\[
k^*
=
f(N,\sigma,E_{\mathrm{cov}},\lambda_{\min}(\Gamma))
\]

---

## Rule 5

The object of study is not the full system.

It is the recoverable structural boundary:

\[
\boxed{
\text{maximum stable structure observable by a bounded agent}
}
\]
