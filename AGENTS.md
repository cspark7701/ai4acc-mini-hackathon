# AGENTS.md — AI Agent & Developer Operational Guide

This document defines the architecture, simulation mechanics, interfaces, and operational protocols for autonomous AI agents, coding assistants (such as Antigravity, Claude, ChatGPT, Cursor, Copilot), and accelerator domain engineers working in this repository.

---

## 🧭 Repository Mission

This repository contains the simulation environment and benchmark harness for the **AI Applications in Accelerators Tutorial & Mini-Hackathon**.

The objective for AI agents operating in this workspace is:
1. Assist participants in understanding the beam physics, Gymnasium environment, and baseline controllers.
2. Develop, tune, and benchmark closed-loop accelerator orbit control policies.
3. Validate policy convergence and telemetry reporting without modifying underlying physical ground truths or benchmark seed constraints.

---

## 🧬 Physical System & Simulation Specifications

### 1. Lattice Geometry & Diagnostics
- **Transport Section Length:** 15.0 meters.
- **Beam Position Monitors (BPMs):** 12 diagnostic stations measuring transverse displacement in millimeters ($mm$).
  - Observation Vector: $\mathbf{Y} \in \mathbb{R}^{12}$; the declared observation space is $[-10.0, +10.0]\text{ mm}$, but values are not clipped (on the evaluation seeds they reach about $6\text{ mm}$).
- **Dipole Steering Correctors:** 6 magnet actuators (3 Horizontal `HCM1-3`, 3 Vertical `VCM1-3`).
  - Total Current State: $\mathbf{I} \in \mathbb{R}^6$, hardware bounds $[-5.0\text{ A}, +5.0\text{ A}]$.
  - Control Action: $\Delta \mathbf{I} \in \mathbb{R}^6$, per-step delta bound $[-0.8\text{ A}, +0.8\text{ A}]$.
- **Quadrupole Focusing:** Alternating `QF` and `QD` magnetic elements shaping the betatron phase advance $\psi(s)$ and beta functions $\beta(s)$.

### 2. Physical Response Model
The environment calculates BPM readings from corrector currents $\mathbf{I}$ via:
$$\mathbf{Y} = \mathbf{I} \cdot \mathbf{R} - 0.015 \cdot (\mathbf{I}^3 \cdot \mathbf{R}) + \mathbf{Y}_0 + \boldsymbol{\epsilon}$$

- **Linear Response Matrix ($\mathbf{R}$):** $6 \times 12$, single-pass transport-line form: a corrector only moves the orbit at BPMs downstream of it. With correctors at $s_i \in$ `linspace(0.2, 8.0, 6)` m and BPMs at $s_j \in$ `linspace(1.0, 15.0, 12)` m:
  $$R_{ij} = \begin{cases} \dfrac{1.2\,\sin\!\big(2\pi \cdot 0.18\,(s_j - s_i)\big)}{1 + 0.05\,(s_j - s_i)} & s_j > s_i \\ 0 & \text{otherwise} \end{cases}$$
  This is the transport-line response $\sqrt{\beta_i \beta_j}\,\sin(\psi_j - \psi_i)$ with simplified optics: a constant phase advance of $2\pi \cdot 0.18$ rad/m and a slowly decaying amplitude. (The ring closed-orbit formula with $2\sin(\pi\nu)$ does not apply to a single-pass line.)
- **Non-Linear Core Saturation:** Modeled as cubic soft-saturation: $-0.015 \cdot \mathbf{I}^3 \cdot \mathbf{R}$.
- **Gaussian Measurement Noise:** $\boldsymbol{\epsilon} \sim \mathcal{N}(0, 0.010^2)$ representing sensor jitter.
- **Initial Distortion ($\mathbf{Y}_0$):** Unknown steering errors at all six corrector locations, drawn at episode reset from the seed: $\mathbf{Y}_0 = \mathbf{a} \cdot \mathbf{R}$ with $a_k \sim \mathcal{U}(-2.5, 2.5)$ A, $k = 1..6$ (`env.distortion_kicks`). It lies in the span of the corrector responses, so it can be cancelled, but this needs total currents up to $2.84\text{ A}$ (deep in the cubic saturation) and, with the $0.8\text{ A}$ per-step limit, about 3 to 4 steps. On the evaluation seeds 1–30 the initial RMS is $0.93$–$3.59\text{ mm}$ (mean $1.97\text{ mm}$). The lecture notes, slides and notebooks state this model in full; the six kick amplitudes are unknown to the controller.

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
  - **Truncation (`truncated`):** Triggered if step count reaches `max_steps = 50` (`is_success = False`).
  - **Reward** (used only for RL training; it does not affect the official score):
    $$r_t = - w_{\text{rms}}\,\text{RMS}_{t+1} - w_{\text{act}} \sum_k a_k^2 - c_{\text{step}} + (b \text{ if terminated else } 0)$$
    with constructor defaults $w_{\text{rms}} = 10$, $w_{\text{act}} = 0.01$, $c_{\text{step}} = 0$, $b = 50$ (the participant notebook sets $c_{\text{step}} = 0.5$), or any custom `reward_fn(rms, action, terminated, truncated, step)`.

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
     $$\min_{\Delta \mathbf{I}} \|\mathbf{Y} - f_{\theta}(\mathbf{I}) + f_{\theta}(\mathbf{I} + \Delta \mathbf{I})\|^2 + \lambda \|\Delta \mathbf{I}\|^2$$
   - $\mathbf{I}$ is the present total corrector current from `info["currents"]`, so $\mathbf{Y} - f_\theta(\mathbf{I}) + f_\theta(\mathbf{I} + \Delta \mathbf{I})$ is the predicted next orbit at every step. With the reference MLP settings this scores 779.169; a more accurate surrogate (TODO 1) scores higher.

3. **Track 2 — Closed-Loop RL / Adaptive Policy Agent:**
   - Combines a physics-informed prior with learned parameter residual and adaptive damping:
     $$\Delta \mathbf{I} = \text{damping}(t) \cdot \left[ - \alpha \cdot (\mathbf{R}^T)^{\dagger} \mathbf{Y} + \mathbf{W}_{\text{learned}} \mathbf{Y} + \mathbf{b} \right]$$
   - Uses dynamic decay (e.g., $1.0 / (1.0 + 0.03 \cdot t)$) so that late kicks respond less to sensor noise near the $0.03\text{ mm}$ target. This is a trade-off: with the plain pseudo-inverse it gains 18 points at gain 1.0 and loses 45 at gain 0.45 and 13 at gain 1.2.
   - In the reference `RLOrbitChallengeAgent`, $\mathbf{W}_{\text{learned}}$ and $\mathbf{b}$ start at zero and are never trained, so it is a damped pseudo-inverse controller; nothing is learned unless the participant trains or tunes the residual.

4. **Track 3 — Closed-Loop Bayesian Optimization Controller:**
   - Uses a `GaussianProcessRegressor` (Matérn-5/2 kernel with sensor noise floor) to model orbit error with epistemic uncertainty estimation:
     $$\alpha_{\text{LCB}}(\Delta \mathbf{I}) = \text{RMS}\left( \mathbf{Y} - \boldsymbol{\mu}_{\text{GP}}(\mathbf{I}) + \boldsymbol{\mu}_{\text{GP}}(\mathbf{I} + \Delta \mathbf{I}) \right) - \kappa \cdot \overline{\boldsymbol{\sigma}}_{\text{GP}}(\Delta \mathbf{I}) + \lambda \|\Delta \mathbf{I}\|^2$$
   - Balances exploration ($\kappa > 0$) against exploitation ($\kappa = 0$) under non-linear saturation, converging in about $3.6$ steps on average (878.384 points).
   - The reference GP is fitted once on 300 calibration shots and stays fixed; like Baseline 1 it predicts the next orbit around the present total current $\mathbf{I}$. Refitting the GP online (e.g. from a `step_callback`) turns it into true online Bayesian optimization.

---

## 📏 Official Scoring & Evaluation Protocol

AI agents evaluating controllers must run the standardized benchmark across **30 evaluation seeds** (`seeds = range(1, 31)`).

### Official Scoring Formula:
$$\text{Score} = \frac{1}{30}\sum_{k=1}^{30} s_k, \qquad
s_k = \begin{cases}
400 + 300\,\max\!\left(0,\,\dfrac{20 - n_k}{19}\right) + 300\,\text{clip}\!\left(\dfrac{\ln(0.030/\text{RMS}_k)}{\ln(0.030/0.010)},\,0,\,1\right) & \text{if seed } k \text{ succeeds} \\
0 & \text{otherwise}
\end{cases}$$

- **Per-seed score $s_k$ (0 to 1000 points):** a seed that does not reach $\text{RMS} < 0.030\text{ mm}$ within 50 steps scores 0. A successful seed earns:
  - **Success (400 pts):** for reaching the target at all.
  - **Speed (up to 300 pts):** full points when converging in 1 step ($n_k = 1$), falling linearly to 0 at 20 steps (episodes may run up to 50 steps).
  - **Precision (up to 300 pts):** 0 at the $0.030\text{ mm}$ target, rising on a log scale to full points at the $0.010\text{ mm}$ sensor noise floor. Each factor of improvement in residual orbit counts equally; $0.017\text{ mm}$ earns about half.
- **Score:** the mean of $s_k$ over the 30 seeds, from 0 to 1000. Failures cost the most, so robustness comes first; among robust controllers, speed and landing precision separate the ranks.
- **Current norm** $\overline{\|\mathbf{I}\|}$ is still reported but not scored: it is set mainly by the size of the initial distortion and varies by only a few percent between controllers.

The implementation is `score_seed()` in `src/benchmark.py`.

### Metrics Tracked in Weights & Biases:
- `challenge_score`: Official total benchmark score, 0 to 1000 points (reference controllers score 591 to 878).
- `score_success`, `score_speed`, `score_precision`: The three components of `challenge_score`, averaged over the 30 seeds.
- `success_rate_pct`: Percentage of the 30 seeds reaching $\text{RMS} < 0.03\text{ mm}$ within 50 steps.
- `mean_steps`: Average iterations to reach convergence.
- `mean_final_rms_mm`: Average residual orbit error across all seeds.
- `mean_current_norm_A`: Average cumulative corrector current norm $\sqrt{\sum I_k^2}$.
- `mean_latency_ms`: Mean policy compute execution time per seed in milliseconds.
- `seed_breakdown_table`: Detailed table recording each seed's initial RMS, final RMS, step count, success flag, final current norm, latency, and per-seed score.

---

## 🔒 Agent Operational Rules & Ground Truth Boundaries

To preserve scientific rigor, academic honesty, and benchmark validity, all AI agents operating in this workspace must abide by the following constraints:

1. **Do Not Alter Physical Constants:**
   - Never modify `env.R`, `env.target_rms = 0.03`, `env.max_steps = 50`, or the non-linear saturation factor (`0.015`) in `AcceleratorOrbitGymEnv`.
   - Never modify or bypass the observation noise $\boldsymbol{\epsilon} \sim \mathcal{N}(0, 0.010)$.
2. **Preserve Standardized Evaluation Seeds:**
   - Benchmark evaluation must strictly run on `seeds = range(1, 31)`.
   - Do not cherry-pick or alter test seed indices.
3. **Respect Participant vs. Solution Notebook Separation:**
   - [notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb](notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb): Must preserve the clear `TODO 1`, `TODO 2`, and `TODO 3` instructional structure for attendees.
   - [notebooks/Single_Notebook_Beam_Orbit_Predictor_Solution.ipynb](notebooks/Single_Notebook_Beam_Orbit_Predictor_Solution.ipynb): Contains the worked solution (accurate TODO 1 surrogate and model-inversion controllers for Tracks 1–3, scoring 924.192 / 939.981 / 909.942) with saved benchmark outputs. It is excluded from the participant Docker image; keep it out of anything distributed to participants.
   - [notebooks/Transfer_Matrix_Surrogate_Phase_Space.ipynb](notebooks/Transfer_Matrix_Surrogate_Phase_Space.ipynb): Companion to Lecture 1, slides 14–15 (a neural surrogate of a FODO transfer matrix compared with the matrix in phase space). It is independent of the benchmark, is generated by `scripts/build_transfer_matrix_notebook.py` (edit the script, then run it with `--execute`), and ships in the participant image.
   - **Participant image contents:** the participant notebook, the transfer-matrix notebook, the Lecture 1 notes and slides, the mini-hackathon slides, `PARTICIPANT_MODIFICATION_GUIDE.pdf` and `CALLBACK_EXAMPLES.pdf`. `scripts/image_common.sh` verifies each of them against the repository before a bundle or publish.
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
- **No attribution trailers:** The message must end with the `Files:` list. Do not append `Co-Authored-By:` lines (for example `Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>`), "Generated with" notices, or any other AI-assistant attribution trailer.

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
for step in range(env.max_steps):
    action = agent.act(obs, info)
    obs, reward, terminated, truncated, info = env.step(action)
    print(f"Step {step+1}: RMS = {info['rms']:.4f} mm, Action Norm = {np.linalg.norm(action):.3f}")
    if terminated:
        print(f"Converged successfully in {step+1} steps! Final RMS = {info['rms']:.4f} mm")
        break
```

---

## 💡 Practical Advice for AI Agents Assisting Participants

- **If an agent's policy diverges or oscillates:** Check the feedback gain $\alpha$. With the plain pseudo-inverse, gains up to about $1.2$ converge fastest (about 3.7 steps at $1.2$ versus 9.4 at $0.45$); above that the policy overshoots. The $0.8$ A per-step limit means most seeds need at least 3 to 4 steps. Compensate the cubic saturation using the total currents in `info["currents"]`, or introduce step damping: $\alpha_t = \alpha_0 / (1.0 + \gamma \cdot t)$.
- **Callbacks:** participants may register `step_callback` / `episode_callback` for Baseline 1, Track 2 and Track 3 in the notebook's `CALLBACKS` dictionary (Step 4); Baseline 0 always runs without callbacks.
- **If the surrogate model exhibits high holdout error:** Ensure sample coverage in offline training covers at least $[-3.0, 3.0]$ A (the correction needs up to $2.84$ A) and that the non-linear cubic term is represented.
- **If W&B logging fails:** Workshop participants authenticate with the shared service key that the launchers pass as `WANDB_API_KEY` (from `wandb.apikey` next to the launcher); no `wandb.login()` is needed. Check that the key file is present and that `WANDB_PROJECT` and `WANDB_ENTITY` are unchanged. If offline, the harness falls back to local reporting.
