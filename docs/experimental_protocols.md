# Computational Phase Boundary

# Experimental Protocols

## Version 0.1 — Validation Procedures

---

# 1. Purpose

This document defines the experimental procedures used to evaluate the Computational Phase Boundary framework.

The objective is not merely to determine whether a model predicts trajectories accurately.

The objective is to measure whether a bounded observer exhibits a finite **structural resolution horizon**:

\[
k^*
\]

defined as the maximum depth at which additional algebraic structure produces net informational benefit.

The experimental program tests:

1. Whether structural compression increases before the horizon.
2. Whether uncertainty dominates after the horizon.
3. Whether the horizon follows predicted resource scaling laws.
4. Whether failure modes can be separated diagnostically.

---

# 2. Experimental Philosophy

The framework predicts that structural discovery follows:

\[
\text{data}
\rightarrow
\hat F_N^\sigma
\rightarrow
\mathrm{Lie}_k(\hat F)
\rightarrow
\widehat{\mathrm{Inv}}_k
\rightarrow
\hat G^{(k)}
\rightarrow
\Delta L(k),C_G(k)
\rightarrow
k^*
\]

Experiments must therefore measure the entire chain.

A successful experiment must not only show a better predictor.

It must demonstrate:

\[
\boxed{
\text{compression gain}
+
\text{symmetry stabilization}
+
\text{resource scaling}
}
\]

---

# 3. Experimental Variables

## 3.1 Controlled Variables

The following parameters are independently manipulated.

---

## Sample Size

\[
N
\]

Controls observational density.

Expected effect:

\[
\frac{\partial k^*}{\partial N}>0
\]

---

## Noise Level

\[
\sigma
\]

Controls measurement uncertainty.

Expected effect:

\[
\frac{\partial k^*}{\partial\sigma}<0
\]

---

## Coverage Error

\[
E_{\mathrm{cov}}
\]

Controls exploration of the state manifold.

Expected effect:

\[
\frac{\partial k^*}{\partial E_{\mathrm{cov}}}<0
\]

---

## Excitation Diversity

\[
\lambda_{\min}(\Gamma)
\]

Controls intervention richness.

Expected effect:

\[
\frac{\partial k^*}{\partial\lambda_{\min}(\Gamma)}>0
\]

---

## Regularization

\[
\lambda_N
\]

Controls estimator stability.

Used primarily in causal bypass experiments.

---

# 4. Core Measurement Outputs

Every experiment must report:

---

## 4.1 Structural Compression Curve

\[
\Delta L(k)
\]

Measured using MDL comparison:

\[
\Delta L(k)
=
L(\mathcal D_N|\mathrm{Baseline})
-
L
\left(
\mathcal D_N
|
\frac{\mathrm{Lie}_k(\hat F)}
{\hat G^{(k)}}
\right)
\]

Expected:

- increase during discovery,
- maximum at \(k^*\),
- decrease after horizon.

---

## 4.2 Gauge Complexity Curve

\[
C_G(k)
\]

Measured as:

\[
C_G(k)
=
L(\theta_G)
+
\log
N
(
\delta,
\hat G^{(k)}
\cap B_R,
d_{C^{k+1}}
)
\]

Expected:

- contraction before horizon,
- minimum near horizon,
- rebound after horizon.

---

## 4.3 Efficiency Curve

\[
\eta(k)
=
\frac{\Delta L(k)}
{C_G(k)}
\]

The operational horizon is:

\[
\boxed{
k^*=
\arg\max_k\eta(k)
}
\]

---

# 5. Phase I — Harmonic Oscillator Calibration

## System Definition

The baseline system:

\[
\dot{x}=p
\]

\[
\dot{p}=-\omega^2x
\]

has invariant:

\[
\boxed{
H=
\frac12p^2
+
\frac12\omega^2x^2
}
\]

---

## Objective

Verify that the instrument can recover known structure under controlled conditions.

---

## Procedure

### Step 1

Generate trajectories:

\[
x(t_i),p(t_i)
\]

for known:

\[
\omega
\]

---

### Step 2

Add controlled noise:

\[
\eta_i\sim\sigma
\]

---

### Step 3

Estimate:

\[
\hat F_N^\sigma
\]

---

### Step 4

Compute:

\[
\Delta L(k)
\]

and:

\[
C_G(k)
\]

---

## Expected Result

A stable maximum:

\[
k^*
\]

with:

\[
E_{\mathrm{gauge}}\approx0
\]

---

# 6. Phase II — Coordinate Distortion Test

## Objective

Test whether the framework identifies invariant structure rather than coordinate-specific patterns.

---

## Transformation

Apply nonlinear coordinate mapping:

\[
y=h(x)
\]

where:

\[
h
\]

is smooth and invertible.

Examples:

\[
y=x^3
\]

or:

\[
y=x+\alpha x^2
\]

---

## Comparison

Evaluate:

### Coordinate-dependent baseline

Expected:

\[
E_{\mathrm{gauge}}\uparrow
\]

---

### Quotient representation

\[
\frac{\mathrm{Lie}_{k^*}(\hat F)}
{\hat G^{(k^*)}}
\]

Expected:

\[
E_{\mathrm{gauge}}\downarrow
\]

---

# 7. Phase III — Noise Horizon Sweep

## Objective

Measure:

\[
k^*(\sigma)
\]

---

## Protocol

Run:

\[
\sigma_1<\sigma_2<...<\sigma_n
\]

while keeping:

\[
N,E_{\mathrm{cov}},\Gamma
\]

constant.

---

## Prediction

The horizon should satisfy:

\[
\sigma_i<\sigma_j
\Rightarrow
k^*(\sigma_i)>k^*(\sigma_j)
\]

---

## Failure Interpretation

If:

\[
k^*
\]

does not decrease:

Possible causes:

- derivative estimator too stable,
- incorrect noise model,
- insufficient depth range.

---

# 8. Phase IV — Data Scaling Sweep

## Objective

Measure:

\[
k^*(N)
\]

---

## Protocol

Run:

\[
N_1<N_2<...<N_n
\]

with fixed:

\[
\sigma
\]

---

## Prediction

\[
N_i<N_j
\Rightarrow
k^*(N_i)<k^*(N_j)
\]

---

# 9. Phase V — Coverage Expansion Experiment

## Objective

Separate:

\[
E_{\mathrm{cover}}
\]

from:

\[
E_{\mathrm{gauge}}
\]

---

## Procedure

Generate trajectories with increasing manifold coverage.

Measure:

\[
E_{\mathrm{cover}}
\]

and:

\[
E_{\mathrm{gauge}}
\]

---

## Expected Behavior

Poor coverage:

\[
E_{\mathrm{cover}}\uparrow
\]

may create false local symmetries.

Improved coverage should collapse these artifacts.

---

# 10. Phase VI — Excitation Diversity Experiment

## Objective

Test active intervention effects.

---

## Controlled Quantity

\[
\lambda_{\min}(\Gamma)
\]

---

## Procedure

Increase intervention diversity.

Measure:

\[
k^*
\]

and:

\[
E_{\mathrm{gauge}}
\]

---

## Prediction

Initially:

\[
E_{\mathrm{gauge}}\downarrow
\]

and:

\[
k^*\uparrow
\]

Later:

\[
\frac{\partial^2 k^*}
{\partial\lambda_{\min}(\Gamma)^2}<0
\]

---

# 11. Phase VII — Regularization Bypass Experiment

## Purpose

Determine whether the horizon is observer-limited.

---

## Intervention

Sweep:

\[
\lambda_N
\]

while holding:

\[
N,\sigma,E_{\mathrm{cov}},\Gamma
\]

fixed.

---

## Causal Chain

\[
\boxed{
\lambda_N
\rightarrow
\epsilon_k
\rightarrow
C_G(k)
\rightarrow
\eta(k)
\rightarrow
k^*
}
\]

---

# Observer-Limited Outcome

If:

\[
k^*
\]

moves with:

\[
\lambda_N
\]

then:

\[
A_k
\]

variance amplification is the dominant bottleneck.

---

# Structure-Limited Outcome

If:

\[
k^*
\]

remains fixed:

the limit is likely due to:

- intrinsic invariant exhaustion,
- insufficient representation class,
- structural mismatch.

---

# 12. Phase VIII — Nonlinear Rigid Body Test

## System

Euler equations:

\[
\dot L=L\times I^{-1}L
\]

---

## Known invariants

Energy:

\[
T=
\frac12L\cdot I^{-1}L
\]

Angular momentum magnitude:

\[
M^2=
||L||^2
\]

---

## Purpose

Test:

- nonlinear curvature,
- nontrivial Lie closure,
- higher-order invariant extraction.

---

# 13. Required Experimental Outputs

Each run must produce:

```text
Experiment ID

System:
Parameters:

N:
sigma:
E_cov:
lambda_min(Gamma):
lambda_N:

Estimated generator:
Invariant depth range:

Delta L(k):
C_G(k):
eta(k):

Measured k*:

Error vector:
E_learn
E_gauge
E_truncate
E_cover

Falsification status:
