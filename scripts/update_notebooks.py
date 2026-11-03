"""
scripts/update_notebooks.py
Regenerate streamlined hackathon notebooks:
- Imports core simulation, controllers, and benchmarks from src/
- Adds comprehensive instructions and newbie examples for TODO 1 and TODO 2
- Hides the raw proprietary scoring formula in the participant notebook
- Adds strategic tuning cheat-sheet and hints showing which values to modify to get higher scores
"""
import json

def make_cell(cell_type, text):
    lines = [line + '\n' for line in text.split('\n')]
    if lines and lines[-1] == '\n':
        lines = lines[:-1]
    return {
        'cell_type': cell_type,
        'metadata': {},
        'source': lines,
        **({'execution_count': None, 'outputs': []} if cell_type == 'code' else {})
    }

# ------------------------------------------------------------------------------
# Cell 0: Header Markdown
# ------------------------------------------------------------------------------
c0_md = """# Accelerator Orbit Alignment Hackathon: Beam Orbit Benchmark
## Participant Edition (with Weights & Biases / W&B Leaderboard Integration)

**Workshop & Challenge Context:**
* **Venue:** Korea Multi-purpose Accelerator Complex (KOMAC) / KAERI
* **Target Audience:** Graduate Students & Early-Career Accelerator Researchers
* **Curricular Alignment:** 
  * **Lecture 1:** Chong Shik Park — AI/ML Fundamentals & Neural Surrogate Modeling
  * **Lecture 2:** Thorsten Hellert — Agentic AI, Autonomous Operations & Scientific Workflows

---

### 🎯 Challenge Mission
In modern particle accelerators and beam transport lines, beam alignment is critical to ensure high transmission efficiency and prevent beam loss. 
In this hackathon, you will develop closed-loop control algorithms to steer the beam through a **15-meter transport line** with:
* **6 Dipole Steering Magnets:** $X = [\\mathrm{HCM1}, \\mathrm{VCM1}, \\mathrm{HCM2}, \\mathrm{VCM2}, \\mathrm{HCM3}, \\mathrm{VCM3}]^T \\in [-5.0\\text{ A}, +5.0\\text{ A}]$
* **12 Beam Position Monitors (BPMs):** $Y \\in \\mathbb{R}^{12}$, measuring transverse beam offsets in millimeters (mm).
* **Non-Linear Iron Saturation:** $B(I) \\approx I - 0.015 \\cdot I^3$, causing progressive softening at higher corrector currents.
* **Objective:** Align the beam so that the Root-Mean-Square (RMS) displacement is below **$0.030\\text{ mm}$** within a budget of **20 control steps**:
  $$\\text{RMS} = \\sqrt{\\frac{1}{12}\\sum_{i=1}^{12} Y_i^2} < 0.030\\text{ mm}$$

---

### 🏆 Two Parallel Competition Tracks:
1. **Track 1 (Supervised Digital Twin Inversion):** Train a non-linear neural surrogate model (MLP) on offline tracking data, and use an optimization solver to invert the surrogate for optimal corrective kicks.
2. **Track 2 (Closed-Loop Reinforcement Learning / Adaptive Policy):** Design an interactive feedback policy agent that continuously senses BPM offsets and outputs delta current kicks $\\Delta I_c$ with physics-informed priors and adaptive damping."""

# ------------------------------------------------------------------------------
# Cell 1: Step 0 Code (Imports & Setup)
# ------------------------------------------------------------------------------
c1_code = """# Step 0: Imports, Environment Setup, and Weights & Biases (W&B) Configuration
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error
from sklearn.linear_model import Ridge
from sklearn.neural_network import MLPRegressor

# Import standardized simulation, controllers, benchmark & visualization from src/
from src import (
    AcceleratorOrbitGymEnv,
    ClassicalSVDController,
    SupervisedMLPController,
    RLOrbitChallengeAgent,
    generate_offline_dataset,
    evaluate_hackathon_benchmark,
    print_benchmark_leaderboard,
    draw_beamline,
    plot_benchmark_trajectories
)

# ------------------------------------------------------------------------------
# Hackathon Configuration (Customize for Your Team!)
# ------------------------------------------------------------------------------
TEAM_NAME = "Team_Alpha"                    # <-- CHANGE THIS: Your registered team name!
WANDB_PROJECT = "accelerator-orbit-hackathon" # [DO NOT CHANGE] Workshop project name for live leaderboard
WANDB_ENTITY = None                          # [DO NOT CHANGE] Leave None for personal account or preset workspace
USE_WANDB = True                             # [DO NOT CHANGE] Keep True to submit scores to the live leaderboard

print(f"Setup complete! Ready to compete as: {TEAM_NAME}")"""

# ------------------------------------------------------------------------------
# Cell 2: Section 1 Markdown
# ------------------------------------------------------------------------------
c2_md = """## 1. Accelerator Lattice Physics & 2D Schematic

The challenge beamline section consists of:
* **Actuators:** 6 dipole steering magnets (3 Horizontal `HCM1-3`, 3 Vertical `VCM1-3`).
* **Optics:** Alternating quadrupole magnets (`QF` focusing, `QD` defocusing) shaping betatron oscillations.
* **Diagnostics:** 12 Beam Position Monitors (`BPM1` to `BPM12`) spaced along the 15-meter transport axis.

The 2D schematic diagram below illustrates the arrangement of steering magnets, quadrupoles, and diagnostic monitors along the longitudinal beam axis $s$."""

# ------------------------------------------------------------------------------
# Cell 3: Step 1 Code
# ------------------------------------------------------------------------------
c3_code = """# Step 1: Display 2D Accelerator Beamline Schematic Diagram
fig = draw_beamline(save_path="img/beamline.png", show=True)"""

# ------------------------------------------------------------------------------
# Cell 4: Section 2 Markdown
# ------------------------------------------------------------------------------
c4_md = """## 2. Standard Gymnasium Environment (`AcceleratorOrbitGymEnv`)

The accelerator simulator is encapsulated in a standardized **Gymnasium** environment (`src/environment.py`):
* **Observation Space:** $\\mathbf{Y} \\in \\mathbb{R}^{12}$, bounded in $[-10.0\\text{ mm}, +10.0\\text{ mm}]$ (12 BPM readings).
* **Action Space:** $\\Delta \\mathbf{I} \\in \\mathbb{R}^6$, bounded in $[-0.8\\text{ A}, +0.8\\text{ A}]$ per step.
* **Hardware Limit:** Total current state $\\mathbf{I}_{t+1} = \\text{clip}(\\mathbf{I}_t + \\Delta \\mathbf{I}, -5.0, +5.0)\\text{ A}$.
* **Physical Response Model:**
  $$\\mathbf{Y} = \\mathbf{I} \\cdot \\mathbf{R} - 0.015 \\cdot (\\mathbf{I}^3 \\cdot \\mathbf{R}) + \\mathbf{Y}_0 + \\boldsymbol{\\epsilon}$$
  where $\\mathbf{R}$ is the $6 \\times 12$ linear transfer matrix, $-0.015 \\mathbf{I}^3 \\mathbf{R}$ represents soft iron core saturation, $\\mathbf{Y}_0$ is initial alignment drift, and $\\boldsymbol{\\epsilon} \\sim \\mathcal{N}(0, 0.010^2\\text{ mm}^2)$ is Gaussian sensor noise.
* **Reward:** $r_t = - 10.0 \\times \\text{RMS}_{t+1} - 0.01 \\|\\Delta \\mathbf{I}\\|_2^2 + (50.0 \\text{ if success else } 0.0)$.
* **Termination:** Episode succeeds when $\\text{RMS} < 0.030\\text{ mm}$, or truncates after `max_steps = 20` steps."""

# ------------------------------------------------------------------------------
# Cell 5: Step 2 Code
# ------------------------------------------------------------------------------
c5_code = """# Step 2: Instantiate Standardized Hackathon Gymnasium Environment
env = AcceleratorOrbitGymEnv()

# Reset to canonical test seed 42 to inspect initial uncorrected orbit distortion
obs, info = env.reset(seed=42)

print("=" * 68)
print("   Hackathon Gymnasium Environment Instantiated Successfully!")
print("=" * 68)
print(f"  • Observation Vector Shape : {obs.shape} (12 BPM stations in mm)")
print(f"  • Action Vector Shape      : {env.action_space.shape} (6 Corrector kick deltas in A)")
print(f"  • Action Limits (per step) : [{env.action_space.low[0]:.1f} A, +{env.action_space.high[0]:.1f} A]")
print(f"  • Hardware Current Bounds  : [-5.0 A, +5.0 A]")
print(f"  • Target RMS Tolerance     : < {env.target_rms:.3f} mm")
print(f"  • Max Control Budget       : {env.max_steps} steps per episode")
print(f"  • Initial Uncorrected RMS  : {info['rms']:.4f} mm")
print("=" * 68)"""

# ------------------------------------------------------------------------------
# Cell 6: Section 3 Markdown
# ------------------------------------------------------------------------------
c6_md = """## 3. Supervised Forward Modeling: Linear Model vs. Neural Surrogate

In accelerator operations, numerical tracking simulation datasets can be converted into fast machine learning digital twins (Lecture 1).
Here, we collect 1,500 simulation shots (80% train, 20% test) across currents $[-3.0\\text{ A}, +3.0\\text{ A}]$ and train:
1. **A Linear Ridge Model:** Serves as a baseline, but cannot account for non-linear core saturation.
2. **A Multi-Layer Perceptron (MLP):** A deep neural network capable of fitting the non-linear cubic saturation curve."""

# ------------------------------------------------------------------------------
# Cell 7: Step 3 Code (Participant with TODO 1 & Hints)
# ------------------------------------------------------------------------------
c7_code_part = """# Step 3: Offline Data Generation & Surrogate Training
# Generate 1500 training samples covering [-3.0, +3.0] A with non-linear saturation and noise
X_offline, Y_offline = generate_offline_dataset(
    env,
    n_samples=1500,
    current_range=(-3.0, 3.0),
    noise_std=0.010,
    random_state=42
)
X_train, X_test, Y_train, Y_test = train_test_split(X_offline, Y_offline, test_size=0.20, random_state=42)
print(f"Dataset generated: X_train shape={X_train.shape}, Y_train shape={Y_train.shape}")

# ==============================================================================
# TODO 1: Train Linear Baseline & Neural Surrogate Model
# ==============================================================================
# INSTRUCTIONS FOR PARTICIPANTS:
# Train two surrogate models to predict the 12 BPM readings from 6 corrector currents:
#   1. Linear Model (Ridge Regression): Fast baseline, but linear only.
#   2. Multi-Layer Perceptron (MLPRegressor): Deep feedforward neural network that
#      learns the cubic iron core magnetic saturation: B(I) ~ I - 0.015 * I^3.
#
# ------------------------------------------------------------------------------
# EXAMPLES FOR NEWBIE PARTICIPANTS:
#
# Example 1: Train Ridge Linear Regression
#   linear_model = Ridge(alpha=1.0)
#   linear_model.fit(X_train, Y_train)
#
# Example 2: Train Multi-Layer Perceptron (MLPRegressor)
#   surrogate_model = MLPRegressor(
#       hidden_layer_sizes=(128, 64, 32), # 3 hidden layers: 128 -> 64 -> 32 neurons
#       activation='relu',               # Activation function: f(x) = max(0, x)
#       solver='adam',                   # Adam gradient-based optimizer
#       alpha=1e-4,                      # L2 regularization penalty
#       learning_rate_init=0.001,        # Initial learning rate
#       max_iter=400,                    # Training epochs
#       random_state=42
#   )
#   surrogate_model.fit(X_train, Y_train)
#
# ------------------------------------------------------------------------------
# 💡 HINTS TO GET HIGHER SCORES:
#   • Network Architecture: Try wider or deeper layers like (128, 128), (256, 128, 64).
#     A more expressive surrogate provides a more accurate gradient for the optimizer in Track 1!
#   • Training Sample Size: Increasing n_samples (e.g. 2000 or 3000) improves test generalization.
#   • Regularization: Tune alpha (e.g., 1e-4 vs 1e-5) to avoid overfitting the sensor noise.
#   • Accuracy Benchmark: Target test RMSE is < 0.015 mm (near the 0.010 mm sensor noise floor).
# ==============================================================================

# 1. Train Linear Baseline
linear_model = Ridge(alpha=1.0).fit(X_train, Y_train)
rmse_linear = root_mean_squared_error(Y_test, linear_model.predict(X_test))

# 2. Train Multi-Layer Perceptron (MLP) Neural Surrogate
surrogate_model = MLPRegressor(
    hidden_layer_sizes=(128, 64, 32),
    activation='relu',
    solver='adam',
    alpha=1e-4,
    max_iter=400,
    random_state=42
).fit(X_train, Y_train)
rmse_mlp = root_mean_squared_error(Y_test, surrogate_model.predict(X_test))

print("=" * 68)
print("SURROGATE MODEL PREDICTIVE ACCURACY (TEST SET):")
print("=" * 68)
print(f"  • Linear Ridge Test RMSE   : {rmse_linear:.4f} mm")
print(f"  • Neural MLP Test RMSE     : {rmse_mlp:.4f} mm (Captures cubic core saturation)")
print(f"  • Gaussian BPM Noise Floor : {env.noise_std:.4f} mm")
print("=" * 68)"""

# ------------------------------------------------------------------------------
# Cell 8: Section 4 Markdown
# ------------------------------------------------------------------------------
c8_md = """---
## 4. Benchmark Controllers: Classical, Supervised, and RL Agents

Every competitor controller must implement the standardized agent interface:
```python
def act(self, obs: np.ndarray, info: Optional[dict] = None) -> np.ndarray
```
where `obs` has shape `(12,)` and the returned action is an array of shape `(6,)` in $[-0.8\\text{ A}, +0.8\\text{ A}]$.

1. **Baseline 0 (Classical SVD Controller):** Inverts the linear Orbit Response Matrix via Moore-Penrose pseudo-inverse: $\\Delta \\mathbf{I} = - \\alpha (\\mathbf{R}^T)^{\\dagger} \\mathbf{Y}$.
2. **Baseline 1 (Supervised Neural Inversion):** Solves an optimization problem per step using the trained neural surrogate digital twin:
   $$\\min_{\\Delta \\mathbf{I}} \\|\\mathbf{Y} + f_{\\theta}(\\Delta \\mathbf{I})\\|^2 + \\lambda \\|\\Delta \\mathbf{I}\\|^2$$
3. **Challenge Track 2 (Closed-Loop RL / Adaptive Agent):** Combines physics prior feedback with adaptive step damping:
   $$\\Delta \\mathbf{I}_t = \\text{damping}(t) \\cdot \\left[ - \\alpha (\\mathbf{R}^T)^{\\dagger} \\mathbf{Y} + \\mathbf{W}_{\\text{tune}} \\mathbf{Y} + \\mathbf{b} \\right]$$"""

# ------------------------------------------------------------------------------
# Cell 9: Step 4 Code (Participant with TODO 2 & Hints)
# ------------------------------------------------------------------------------
c9_code_part = """# Step 4: Define Benchmark Controllers

# 1. Baseline 0: Classical Linear ORM Pseudo-Inverse Controller (from src)
b0 = ClassicalSVDController(env.R, gain=0.45)

# 2. Baseline 1: Supervised Forward Surrogate + SciPy Inversion Optimizer (from src)
b1 = SupervisedMLPController(surrogate_model)

# ==============================================================================
# TODO 2 (Challenge Track 2): Design & Tune Closed-Loop Policy Agent
# ==============================================================================
# INSTRUCTIONS FOR PARTICIPANTS:
# Implement your closed-loop policy by writing the act(obs, info) method.
# Your agent receives current BPM readings obs (12,) and returns delta currents action (6,).
#
# ------------------------------------------------------------------------------
# EXAMPLES FOR NEWBIE PARTICIPANTS:
#
# Example A: Damped Physics Prior (Simple & Robust)
#   class DampedSVDController:
#       def __init__(self, R_matrix, gain=0.45, decay=0.03):
#           self.R_pinv = np.linalg.pinv(R_matrix.T)
#           self.gain = gain
#           self.decay = decay
#       def act(self, obs, info=None):
#           step = info.get("step", 0) if info else 0
#           damping = 1.0 / (1.0 + self.decay * step)
#           action = - self.gain * (self.R_pinv @ obs) * damping
#           return np.clip(action, -0.8, 0.8)
#
# Example B: Physics Prior + Tunable Linear Residual Correction
#   class RLOrbitChallengeAgent:
#       def __init__(self, R_matrix, gain=0.45):
#           self.base_R_pinv = np.linalg.pinv(R_matrix.T)
#           self.gain = gain
#           self.W_tune = np.zeros((6, 12))  # Adjust weights to compensate saturation
#           self.bias = np.zeros(6)
#       def act(self, obs, info=None):
#           step = info.get("step", 0) if info else 0
#           action_phys = - self.gain * (self.base_R_pinv @ obs)
#           action_learned = self.W_tune @ obs + self.bias
#           action = action_phys + 0.05 * np.tanh(action_learned)
#           damping = 1.0 / (1.0 + 0.03 * step)
#           return np.clip(action * damping, -0.8, 0.8)
#
# ------------------------------------------------------------------------------
# 💡 STRATEGIC TUNING HINTS: WHICH VALUES TO MODIFY TO GET HIGHER SCORES!
#
# 1. Feedback Gain (alpha): Default is 0.45.
#    • Increasing gain to 0.55–0.72 dramatically speeds up convergence (reduces step count).
#    • Warning: If gain is too high (>0.75), the policy may overshoot due to non-linear saturation!
#
# 2. Adaptive Gain Scheduling:
#    • Instead of fixed gain, check the current RMS error:
#        rms = np.sqrt(np.mean(obs**2))
#        gain = 0.72 if rms > 0.15 else (0.55 if rms > 0.05 else 0.38)
#    • This takes large strides when far away, and delicate micro-steps near the 0.030 mm target!
#
# 3. Dynamic Damping (gamma):
#    • damping = 1.0 / (1.0 + gamma * step).
#    • Tuning gamma in [0.015, 0.035] suppresses limit-cycle oscillations around 0.030 mm.
#
# 4. Non-Linear Cubic Desaturation Compensation:
#    • The magnet response softens as B(I) ~ I - 0.015 * I^3.
#    • Apply analytical series inversion to your kick:
#        delta_I_corrected = delta_I_lin + 0.015 * (delta_I_lin ** 3)
#    • This compensates for iron core softening in 1 shot!
#
# 5. Energy Efficiency (Current Norm):
#    • Avoid unnecessary opposing kicks between adjacent correctors; keeping total current
#      low gives an energy-efficiency score bonus!
# ==============================================================================

class MyCustomRLAgent:
    \"\"\"Track 2: Participant Custom Closed-Loop Policy Agent.\"\"\"
    def __init__(self, R_matrix, gain=0.45):
        self.base_R_pinv = np.linalg.pinv(R_matrix.T)
        self.gain = gain
        self.W_tune = np.zeros((6, 12), dtype=np.float64)
        self.bias = np.zeros(6, dtype=np.float64)

    def act(self, obs, info=None):
        step_idx = info.get("step", 0) if info else 0
        action_phys = - self.gain * (self.base_R_pinv @ obs)
        action_learned = self.W_tune @ obs + self.bias
        action = action_phys + 0.05 * np.tanh(action_learned)
        damping = 1.0 / (1.0 + 0.03 * step_idx)
        return np.clip(action * damping, -0.8, 0.8)

b2 = MyCustomRLAgent(env.R, gain=0.45)
print("All three competitor controllers initialized successfully.")"""

# ------------------------------------------------------------------------------
# Cell 10: Section 5 Markdown (Hides formula, adds multi-objective description & cheat-sheet)
# ------------------------------------------------------------------------------
c10_md_part = """---
## 5. Standardized Benchmark Evaluation & Live W&B Scoring

To ensure fair and rigorous comparison, agents are evaluated across **30 standardized evaluation seeds** (`seeds = range(1, 31)`) featuring diverse physical drift perturbations.

### 🎯 Official Multi-Objective Evaluation Criteria
The benchmark evaluation engine (`src/benchmark.py`) computes an aggregated **Hackathon Benchmark Score** evaluating four competitive dimensions:
1. **Alignment Success Rate (%):** Did the agent achieve $\\text{RMS} < 0.030\\text{ mm}$ within the 20-step budget? (Primary requirement).
2. **Convergence Speed (Mean Steps):** Reaching the target in fewer steps earns substantial speed bonuses.
3. **Residual Precision (Final RMS):** Pushing residual orbit error below the $0.030\\text{ mm}$ threshold down towards the $0.010\\text{ mm}$ sensor noise floor earns significant precision bonuses!
4. **Actuator Current Efficiency (Mean Norm):** Minimizing cumulative corrector currents $\\overline{\\|\\mathbf{I}\\|}$ preserves magnet power supplies and avoids energy penalties.

*(Note: The exact proprietary weighting coefficients are encapsulated inside the evaluation engine in `src/benchmark.py`)*.

---

### 💡 Strategic Tuning Cheat-Sheet: How to Beat the Baseline Leaderboard!

| Tuning Target | What to Modify | Impact on Performance & Score |
| :--- | :--- | :--- |
| **Faster Convergence** | Feedback gain $\\alpha \\in [0.55, 0.72]$ in `act()` | Cuts mean steps from 6 down to 3, earning a large speed bonus. |
| **Adaptive Gain Schedule** | Dynamic gain based on current RMS in `act()` | Aggressive kicks when far (`> 0.15 mm`); fine-tuned kicks when close (`< 0.05 mm`). |
| **Precision RMS Bonus** | Damping cooling factor $\\gamma \\in [0.015, 0.035]$ | Prevents terminal oscillations, allowing the beam to land near the $0.010\\text{ mm}$ noise floor. |
| **Non-Linear Boost** | $\\Delta \\mathbf{I}_{\\text{act}} = \\Delta \\mathbf{I}_{\\text{lin}} + 0.015 \\cdot \\Delta \\mathbf{I}_{\\text{lin}}^3$ | Cancels cubic iron saturation in one shot, avoiding under-correction. |
| **Track 1 Optimizer Fix** | Bound search to `[(-0.8, 0.8)]` & warm-start | Prevents action clipping and boosts Track 1 success rate dramatically! |

When `USE_WANDB = True`, telemetry, seed breakdowns, and scores are automatically uploaded to **Weights & Biases (W&B)**."""

# ------------------------------------------------------------------------------
# Cell 11: Step 5 Code (Clean call to benchmark engine)
# ------------------------------------------------------------------------------
c11_code_part = """# Step 5: Standardized Evaluation Harness with Weights & Biases Logging
# Evaluates each competitor controller across 30 standardized seeds (range 1 to 31)
# Telemetry, seed breakdowns, and scores are automatically uploaded to W&B
print("Running Official Hackathon Benchmark across 30 Test Seeds...")

res_b0 = evaluate_hackathon_benchmark(env, b0, agent_name="Baseline0_LinearSVD", team_name=TEAM_NAME, use_wandb=USE_WANDB, project=WANDB_PROJECT, entity=WANDB_ENTITY)
res_b1 = evaluate_hackathon_benchmark(env, b1, agent_name="Baseline1_SupervisedMLP", team_name=TEAM_NAME, use_wandb=USE_WANDB, project=WANDB_PROJECT, entity=WANDB_ENTITY)
res_b2 = evaluate_hackathon_benchmark(env, b2, agent_name="Track2_RLAgent", team_name=TEAM_NAME, use_wandb=USE_WANDB, project=WANDB_PROJECT, entity=WANDB_ENTITY)

# Display Official Leaderboard Table
print_benchmark_leaderboard([
    ("Baseline 1 (Supervised MLP Inversion)", res_b1),
    ("Baseline 0 (Linear ORM SVD Controller)", res_b0),
    ("Track 2 (RL Closed-Loop Agent)", res_b2),
])"""

# ------------------------------------------------------------------------------
# Cell 12: Section 6 Markdown
# ------------------------------------------------------------------------------
c12_md = """---
## 6. Visualizing Trajectory Alignment & Dynamic Convergence

In this step, we evaluate each controller on canonical test seed 42 to inspect:
1. **Beamline Trajectory Alignment (Subplot 1):** Uncorrected beam displacement vs. final corrected orbits across all 12 BPM stations.
2. **Convergence Dynamics (Subplot 2):** Orbit RMS error decay over successive interaction steps towards the $0.030\\text{ mm}$ tolerance line."""

# ------------------------------------------------------------------------------
# Cell 13: Step 6 Code
# ------------------------------------------------------------------------------
c13_code = """# Step 6: Generate Dual Trajectory Overlay & Dynamic Convergence Curves
fig = plot_benchmark_trajectories(
    env,
    controllers={
        "Linear SVD": b0,
        "Supervised MLP": b1,
        "RL Agent": b2
    },
    seed=42,
    save_path="img/benchmark_trajectories.png",
    show=True
)"""

# ------------------------------------------------------------------------------
# Cell 14: Section 7 Markdown
# ------------------------------------------------------------------------------
c14_md = """---
## 7. Final Team Showcase Cell (16:30–17:00)
Run this single summary cell during team presentations to display your official Hackathon submission score!"""

# ------------------------------------------------------------------------------
# Cell 15: Step 7 Code
# ------------------------------------------------------------------------------
c15_code = """# Step 7: Final Team Showcase Presentation Summary
best_agent_name, best_metrics = max(
    [("Track 2 (RL Closed-Loop Agent)", res_b2),
     ("Baseline 1 (Supervised MLP)", res_b1),
     ("Baseline 0 (Linear SVD)", res_b0)],
    key=lambda item: item[1]["score"]
)

print("=" * 68)
print(f"   TEAM: {TEAM_NAME} — OFFICIAL HACKATHON BENCHMARK SUBMISSION")
print("=" * 68)
print(f"  • Best Performing Agent  : {best_agent_name}")
print(f"  • Official Total Score   : {best_metrics['score']:.1f} points")
print(f"  • Alignment Success Rate : {best_metrics['success_rate']:.1f}%")
print(f"  • Mean Steps to Target   : {best_metrics['mean_steps']:.1f} steps")
print(f"  • Mean Residual Orbit RMS: {best_metrics['mean_rms']:.4f} mm")
print(f"  • Mean Corrector Norm    : {best_metrics['mean_norm']:.2f} A")
print(f"  • Mean Policy Latency    : {best_metrics['mean_latency']:.2f} ms")
print("=" * 68)"""

# ------------------------------------------------------------------------------
# Assembly
# ------------------------------------------------------------------------------
participant_cells = [
    make_cell('markdown', c0_md),
    make_cell('code', c1_code),
    make_cell('markdown', c2_md),
    make_cell('code', c3_code),
    make_cell('markdown', c4_md),
    make_cell('code', c5_code),
    make_cell('markdown', c6_md),
    make_cell('code', c7_code_part),
    make_cell('markdown', c8_md),
    make_cell('code', c9_code_part),
    make_cell('markdown', c10_md_part),
    make_cell('code', c11_code_part),
    make_cell('markdown', c12_md),
    make_cell('code', c13_code),
    make_cell('markdown', c14_md),
    make_cell('code', c15_code)
]

participant_nb = {
    'cells': participant_cells,
    'metadata': {
        'language_info': {'name': 'python', 'version': '3.12.3'},
        'kernelspec': {'name': 'ai4acc', 'display_name': 'Python (ai4acc)'}
    },
    'nbformat': 4,
    'nbformat_minor': 2
}

with open('notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb', 'w') as f:
    json.dump(participant_nb, f, indent=1)
print('Generated Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb (formula hidden, hints added)')

# Solution Notebook: includes the reference Track 2 agent in Step 4
solution_cells = list(participant_cells)
c9_code_sol = """# Step 4: Define Benchmark Controllers

# 1. Baseline 0: Classical Linear ORM Pseudo-Inverse Controller (from src)
b0 = ClassicalSVDController(env.R, gain=0.45)

# 2. Baseline 1: Supervised Forward Surrogate + SciPy Inversion Optimizer (from src)
b1 = SupervisedMLPController(surrogate_model)

# 3. Track 2: Reference Closed-Loop RL / Adaptive Agent (from src)
b2 = RLOrbitChallengeAgent(env.R, gain=0.45)

print("All three competitor controllers initialized successfully.")"""

solution_cells[9] = make_cell('code', c9_code_sol)

solution_nb = {
    'cells': solution_cells,
    'metadata': {
        'language_info': {'name': 'python', 'version': '3.12.3'},
        'kernelspec': {'name': 'ai4acc', 'display_name': 'Python (ai4acc)'}
    },
    'nbformat': 4,
    'nbformat_minor': 2
}

with open('notebooks/Single_Notebook_Beam_Orbit_Predictor_Solution.ipynb', 'w') as f:
    json.dump(solution_nb, f, indent=1)
print('Generated Single_Notebook_Beam_Orbit_Predictor_Solution.ipynb')

with open('notebooks/Single_Notebook_Beam_Orbit_Predictor.ipynb', 'w') as f:
    json.dump(solution_nb, f, indent=1)
print('Generated Single_Notebook_Beam_Orbit_Predictor.ipynb')
