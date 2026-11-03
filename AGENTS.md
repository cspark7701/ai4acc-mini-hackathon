# AGENTS.md — AI Agent & Developer Operational Guide

This document defines the architecture, simulation mechanics, interfaces, and operational protocols for autonomous AI agents, coding assistants (such as Antigravity, Claude, ChatGPT, Cursor, Copilot), and accelerator domain engineers working in this repository.

---

## 🧭 Repository Mission

This repository contains the simulation environment and benchmark harness for the **AI Applications in Accelerators Tutorial & Mini-Hackathon** at KOMAC / KAERI.

The objective for AI agents operating in this workspace is:
1. Assist participants in understanding the beam physics, Gymnasium environment, and baseline controllers.
2. Develop, tune, and benchmark closed-loop accelerator orbit control policies.
3. Validate policy convergence and telemetry reporting without modifying underlying physical ground truths or benchmark seed constraints.

---

## 🧬 Physical System & Simulation Specifications

### 1. Lattice Geometry & Diagnostics
- **Transport Section Length:** 15.0 meters.
- **Beam Position Monitors (BPMs):** 12 diagnostic stations measuring transverse displacement in millimeters ($mm$).
  - Observation Vector: $\mathbf{Y} \in \mathbb{R}^{12}$, bounded in $[-10.0, +10.0]\text{ mm}$.
- **Dipole Steering Correctors:** 6 magnet actuators (3 Horizontal `HCM1-3`, 3 Vertical `VCM1-3`).
  - Total Current State: $\mathbf{I} \in \mathbb{R}^6$, hardware bounds $[-5.0\text{ A}, +5.0\text{ A}]$.
  - Control Action: $\Delta \mathbf{I} \in \mathbb{R}^6$, per-step delta bound $[-0.8\text{ A}, +0.8\text{ A}]$.
- **Quadrupole Focusing:** Alternating `QF` and `QD` magnetic elements shaping the betatron phase advance $\psi(s)$ and beta functions $\beta(s)$.

### 2. Physical Response Model
The environment calculates BPM readings from corrector currents $\mathbf{I}$ via:
$$\mathbf{Y} = \mathbf{I} \cdot \mathbf{R} - 0.015 \cdot (\mathbf{I}^3 \cdot \mathbf{R}) + \mathbf{Y}_0 + \boldsymbol{\epsilon}$$

- **Linear Transfer Matrix ($\mathbf{R}$):** $6 \times 12$ matrix modeling betatron oscillation:
  $$R_{ij} = \frac{\sqrt{\beta_i \beta_j}}{2 \sin(\pi \nu)} \cos(|\psi_i - \psi_j| - \pi \nu)$$
- **Non-Linear Core Saturation:** Modeled as cubic soft-saturation: $-0.015 \cdot \mathbf{I}^3 \cdot \mathbf{R}$.
- **Gaussian Measurement Noise:** $\boldsymbol{\epsilon} \sim \mathcal{N}(0, 0.010^2)$ representing sensor jitter.
- **Initial Distortion ($\mathbf{Y}_0$):** Random quadrupole alignment errors drawn at episode reset based on the random seed:
  $$Y_{0, k} = A_1 \sin(2\pi s_k / \lambda_1 + \phi_1) + A_2 \cos(2\pi s_k / \lambda_2 + \phi_2)$$
  producing an initial orbit distortion typically between $0.4\text{ mm}$ and $1.0\text{ mm}$ RMS.

### 3. Gymnasium Environment Contract (`AcceleratorOrbitGymEnv`)
- **`reset(seed=None)`** $\rightarrow$ `(obs, info)`:
  - Initializes corrector currents $\mathbf{I} = \mathbf{0}$.
  - Computes initial distortion $\mathbf{Y}_0$ and initial BPM readings `obs`.
  - `info` contains: `{"step": 0, "rms": float, "initial_rms": float, "currents": np.ndarray}`.
- **`step(action)`** $\rightarrow$ `(obs, reward, terminated, truncated, info)`:
  - `action`: Array of shape `(6,)`, clipped to $[-0.8, 0.8]$ A.
  - State update: $\mathbf{I}_{t+1} = \text{clip}(\mathbf{I}_t + \text{action}, -5.0, 5.0)$.
  - Orbit computation: updates $\mathbf{Y}_{t+1}$ and calculates current RMS:
    $$\text{RMS} = \sqrt{\frac{1}{12}\sum_{i=1}^{12} Y_i^2}$$
  - **Termination (`terminated`):** Triggered if $\text{RMS} < 0.030\text{ mm}$ (`is_success = True`).
  - **Truncation (`truncated`):** Triggered if step count reaches `max_steps = 20` (`is_success = False`).
  - **Reward:**
    $$r_t = - \text{RMS}_{t+1} - 0.01 \cdot \|\text{action}\|_2 + (50.0 \text{ if terminated else } 0.0)$$

---

## 🤖 Controller & Policy Interface Contract

All controllers (classical, supervised, or reinforcement learning) **must** implement the standardized `act` method:

```python
class BenchmarkController:
    """Standard interface required for all competitor controllers."""
    def act(self, obs: np.ndarray, info: Optional[dict] = None) -> np.ndarray:
        """
        Parameters:
            obs: np.ndarray of shape (12,) - current BPM readings in mm
            info: dict containing optional runtime metadata, e.g., info.get('step', 0)
        Returns:
            action: np.ndarray of shape (6,) - delta currents delta_I in [-0.8, 0.8] A
        """
        ...
```

### Baseline Controllers Reference

1. **Baseline 0 — Classical SVD Controller:**
   - Inverts the linear Orbit Response Matrix $\mathbf{R}$ using Moore-Penrose pseudo-inverse:
     $$\Delta \mathbf{I} = - \alpha \cdot (\mathbf{R}^T)^{\dagger} \cdot \mathbf{Y}$$
   - Typical gain $\alpha \approx 0.45$, clipped to $[-0.8, 0.8]$ A.

2. **Baseline 1 — Supervised Neural Surrogate Inversion:**
   - Trains an `MLPRegressor` (e.g. layers `(128, 64, 32)`, ReLU activation) as a forward digital twin: $\hat{\mathbf{Y}} = f_{\theta}(\mathbf{I})$.
   - Solves a bounded optimization problem per step via SciPy `L-BFGS-B`:
     $$\min_{\Delta \mathbf{I}} \|\mathbf{Y} + f_{\theta}(\Delta \mathbf{I})\|^2 + \lambda \|\Delta \mathbf{I}\|^2$$

3. **Track 2 — Closed-Loop RL / Adaptive Policy Agent:**
   - Combines a physics-informed prior with learned parameter residual and adaptive damping:
     $$\Delta \mathbf{I} = \text{damping}(t) \cdot \left[ - \alpha \cdot (\mathbf{R}^T)^{\dagger} \mathbf{Y} + \mathbf{W}_{\text{learned}} \mathbf{Y} + \mathbf{b} \right]$$
   - Uses dynamic decay (e.g., $1.0 / (1.0 + 0.03 \cdot t)$) to prevent terminal limit-cycle oscillations around the sub-$0.03\text{ mm}$ target boundary.

4. **Track 3 — Closed-Loop Bayesian Optimization Controller:**
   - Uses a `GaussianProcessRegressor` (Matérn-5/2 kernel with sensor noise floor) to model orbit error with epistemic uncertainty estimation:
     $$\alpha_{\text{LCB}}(\Delta \mathbf{I}) = \text{RMS}\left( \mathbf{Y} + \boldsymbol{\mu}_{\text{GP}}(\Delta \mathbf{I}) \right) - \kappa \cdot \overline{\boldsymbol{\sigma}}_{\text{GP}}(\Delta \mathbf{I}) + \lambda \|\Delta \mathbf{I}\|^2$$
   - Balances exploration ($\kappa > 0$) against exploitation ($\kappa = 0$) under non-linear saturation, converging in an average of $1.5$ steps.

---

## 📏 Official Scoring & Evaluation Protocol

AI agents evaluating controllers must run the standardized benchmark across **30 evaluation seeds** (`seeds = range(1, 31)`).

### Official Scoring Formula:
$$\text{Score} = (\text{Success Rate} \times 10.0) - (2.0 \times \overline{\text{Steps}}) + \left(\frac{0.03}{\max(\overline{\text{RMS}}, 0.005)} \times 20.0\right) - (2.0 \times \overline{\|\mathbf{I}\|})$$

### Metrics Tracked in Weights & Biases:
- `challenge_score`: Official total benchmark score (target: $> 1000$ points).
- `success_rate_pct`: Percentage of the 30 seeds reaching $\text{RMS} < 0.03\text{ mm}$ within 20 steps.
- `mean_steps`: Average iterations to reach convergence.
- `mean_final_rms_mm`: Average residual orbit error across all seeds.
- `mean_current_norm_A`: Average cumulative corrector current norm $\sqrt{\sum I_k^2}$.
- `mean_latency_ms`: Mean policy compute execution time per seed in milliseconds.
- `seed_breakdown_table`: Detailed table recording each seed's initial RMS, final RMS, step count, success flag, and final current norm.

---

## 🔒 Agent Operational Rules & Ground Truth Boundaries

To preserve scientific rigor, academic honesty, and benchmark validity, all AI agents operating in this workspace must abide by the following constraints:

1. **Do Not Alter Physical Constants:**
   - Never modify `env.R`, `env.target_rms = 0.03`, `env.max_steps = 20`, or the non-linear saturation factor (`0.015`) in `AcceleratorOrbitGymEnv`.
   - Never modify or bypass the observation noise $\boldsymbol{\epsilon} \sim \mathcal{N}(0, 0.010)$.
2. **Preserve Standardized Evaluation Seeds:**
   - Benchmark evaluation must strictly run on `seeds = range(1, 31)`.
   - Do not cherry-pick or alter test seed indices.
3. **Respect Participant vs. Solution Notebook Separation:**
   - [notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb](file:///home/cspark/Work/projects/ai4acc-mini-hackathon/notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb): Must preserve the clear `TODO 1`, `TODO 2`, and `TODO 3` instructional structure for attendees.
   - [notebooks/Single_Notebook_Beam_Orbit_Predictor_Solution.ipynb](file:///home/cspark/Work/projects/ai4acc-mini-hackathon/notebooks/Single_Notebook_Beam_Orbit_Predictor_Solution.ipynb): Contains reference baseline implementations and benchmark outputs.
4. **Action Space Adherence:**
   - The returned action must strictly be a 1D NumPy array or sequence of 6 numerical values.
   - Values exceeding $[-0.8, +0.8]$ A will be hard-clipped by the environment, but well-behaved agents should handle bounds internally.
5. **Git Commit Message Format Adherence:**
   - All commits created in this repository must strictly follow the `Title/Body/Files` three-part structure detailed below.

---

## 📝 Git Commit Message Format Specification

All AI agents and developers committing changes to this repository **must** format their commit messages according to the structured **`Title / Body / Files`** convention:

### Format Structure:
```text
<Imperative Summary Title>

<Detailed explanation body explaining the motivation, architectural changes, context, and validation steps taken.>

Files:
 <Status>  <RelativeFilePath>
 <Status>  <RelativeFilePath>
```

- **Title:** Concise single line summarizing the change in imperative mood (e.g., `Add...`, `Implement...`, `Update...`).
- **Body:** Multi-sentence paragraph explaining *why* the change was made, technical context, and how it was validated.
- **Files:** A literal `Files:` heading followed by git status indicator flags (`M` for modified, `A` for added, `D` for deleted, `R` for renamed) and the affected file paths.

### Standard Example:
```text
Merge origin/main while preserving local training history

Integrate journal-paper workspace documentation without rebasing the local CI and orbit-control commits. Preserve existing commit identities referenced by training records. Validate three orbit-control tests, staged whitespace and the local Actions command dry run.

Files:
 M  AGENTS.md
 M  README.md
```

---

## 🧪 Headless Verification Recipe for Agents

AI agents wishing to test or verify a controller design without opening Jupyter can execute a headless verification script:

```python
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.neural_network import MLPRegressor

# 1. Instantiate environment
from src.environment import AcceleratorOrbitGymEnv
env = AcceleratorOrbitGymEnv()

# 2. Test controller on canonical seed 42
obs, info = env.reset(seed=42)
print(f"Initial RMS: {info['rms']:.4f} mm")

# 3. Step controller until termination
for step in range(20):
    action = agent.act(obs, info)
    obs, reward, terminated, truncated, info = env.step(action)
    print(f"Step {step+1}: RMS = {info['rms']:.4f} mm, Action Norm = {np.linalg.norm(action):.3f}")
    if terminated:
        print(f"Converged successfully in {step+1} steps! Final RMS = {info['rms']:.4f} mm")
        break
```

---

## 💡 Practical Advice for AI Agents Assisting Participants

- **If an agent's policy diverges or oscillates:** Check the feedback gain $\alpha$. A gain above $0.6$ often causes overcorrection in non-linear regimes. Introduce step damping: $\alpha_t = \alpha_0 / (1.0 + \gamma \cdot t)$.
- **If the surrogate model exhibits high holdout error:** Ensure sample coverage in offline training covers $[-3.0, 3.0]$ A and that the non-linear cubic term is represented.
- **If W&B logging fails:** Ensure `wandb.login()` was called or that `WANDB_ENTITY` matches the team's organization handle. If offline, the harness gracefully falls back to local reporting.
