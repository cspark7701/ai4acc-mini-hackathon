# 🤖 Multi-Agent Benchmark Experiment Protocol & Agent Instructions

This document provides complete instructions for running a **10-agent autonomous benchmarking experiment** using the participant notebook ([notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb](file:///home/cspark/Work/projects/ai4acc-mini-hackathon/notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb)) on independent Git worktrees.

---

## 🎯 Experiment Mission & Division of Labor

Ten autonomous agents compete simultaneously to maximize the official accelerator orbit control score across 30 evaluation seeds (`range(1, 31)`).

### Division of 10 Agents:
- **Cohort A (Agents 1 – 5): Callback-Driven Adaptive Optimization**
  - **Strategy:** Leverage the callback system (`step_callback` and/or `episode_callback`) in `evaluate_hackathon_benchmark`.
  - **Focus:** Online adaptive damping, gain decay near the target boundary ($\text{RMS} < 0.04\text{ mm}$), online parameter updates, and trajectory momentum tracking.
  - **Rule:** Must design and connect callback functions to enhance closed-loop performance across all Tracks.

- **Cohort B (Agents 6 – 10): Architectural & Hyperparameter Exploration**
  - **Strategy:** Do **NOT** modify or add callback functions.
  - **Focus:** Explore diverse architectural strategies, forward surrogate training hyperparameters (e.g. MLP hidden layer depths, activations, regularizers in `TODO 1`), policy feedback gains $\alpha \in [0.45, 0.72]$, analytical cubic desaturation kicks, damping factor functions ($\gamma$), and reward shaping in `TODO 2`.
  - **Rule:** Rely purely on offline learning, policy parameter tuning, and analytical compensations.

---

## ⚙️ Operating Environment & Execution Rules

1. **No Docker:** All sub-agents operate directly in isolated local Git worktrees on the host environment.
2. **Standardized Python Runtime:**
   ```bash
   /home/cspark/Work/simulation_codes-working/miniforge3/envs/rl4aa26-challenge/bin/python
   ```
3. **No W&B Account (Local Offline Reporting):**
   - Sub-agents must set `USE_WANDB = False` in their notebooks or use `use_wandb=False` in benchmark calls.
   - All telemetry and scores are calculated locally.
4. **Preserve Ground Truth Boundaries (Strict Benchmark Integrity):**
   - **Never** modify `src/environment.py` physics constants (`target_rms = 0.03`, `noise_std = 0.010`, `max_steps = 20`, or cubic saturation `0.015`).
   - Benchmark evaluation must strictly evaluate on `seeds = range(1, 31)`.
5. **Standardized Scoring Metric:**
   $$\text{Score} = (\text{Success Rate} \times 10.0) - (2.0 \times \overline{\text{Steps}}) + \left(\frac{0.03}{\max(\overline{\text{RMS}}, 0.005)} \times 20.0\right) - (2.0 \times \overline{\|\mathbf{I}\|})$$

---

## 🏗️ Git Worktree Setup Guide (For Main Agent Orchestrator)

The main agent creates 10 isolated worktree branches cloned from `main`:

```bash
# From repository root (/home/cspark/Work/projects/ai4acc-mini-hackathon)
mkdir -p worktrees

for i in $(seq 1 10); do
  git worktree add -b "agent-test-$i" "worktrees/agent-$i" main
done
```

Each sub-agent receives its dedicated workspace path:
- Agent 1: `/home/cspark/Work/projects/ai4acc-mini-hackathon/worktrees/agent-1`
- Agent 2: `/home/cspark/Work/projects/ai4acc-mini-hackathon/worktrees/agent-2`
- ...
- Agent 10: `/home/cspark/Work/projects/ai4acc-mini-hackathon/worktrees/agent-10`

---

## 📋 Sub-Agent Instructions & Operational Flow

Each sub-agent executes the following steps autonomously within its assigned worktree:

### Step 1: Choose Identity
Arbitrarily select a unique name (e.g., `Agent_A1_AdaptiveDamp`, `Agent_A2_OnlineKalman`, `Agent_B6_DeepSurrogate`, `Agent_B7_AggressiveGain`). Set:
```python
TEAM_NAME = "Your_Chosen_Name"
USE_WANDB = False
```

### Step 2: Implement Strategy in Participant Notebook
Target file: `notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb`.

- **If in Cohort A (Agents 1–5):**
  Implement custom callback functions:
  ```python
  def custom_step_callback(step_data, agent):
      # Online adaptive logic, dynamic damping, or parameter tuning
      current_rms = step_data["info"]["rms"]
      if current_rms < 0.040:
          agent.gain *= 0.95
  ```
  Pass the callback to the benchmark call:
  ```python
  res_b2 = evaluate_hackathon_benchmark(
      env, b2,
      agent_name="Track2_RLAgent",
      team_name=TEAM_NAME,
      use_wandb=False,
      step_callback=custom_step_callback
  )
  ```

- **If in Cohort B (Agents 6–10):**
  Do not use callbacks. Optimize `TODO 1` surrogate architecture and `TODO 2` policy dynamics:
  - Hyperparameter sweeps on `MLPRegressor(hidden_layer_sizes=..., alpha=...)`.
  - Tuning `gain` $\in [0.50, 0.72]$ and damping function `damping = 1.0 / (1.0 + gamma * step)`.
  - Non-linear cubic desaturation: $\Delta \mathbf{I} + 0.015 \cdot \Delta \mathbf{I}^3$.

### Step 3: Headless Execution & Benchmark Run
Sub-agents execute the notebook headlessly to generate outputs:
```bash
/home/cspark/Work/simulation_codes-working/miniforge3/envs/rl4aa26-challenge/bin/jupyter nbconvert \
  --to notebook \
  --execute notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb \
  --output Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb
```
*(Alternatively, execute the Python verification script that runs the exact benchmark function).*

### Step 4: Report Results to Main Agent
Each sub-agent formats its final telemetry into a standardized JSON payload and delivers it to the main agent:

```json
{
  "agent_id": 1,
  "agent_name": "Agent_AdaptiveDamping_Alpha",
  "cohort": "A_Callback",
  "track2_results": {
    "score": 1018.4,
    "success_rate_pct": 100.0,
    "mean_steps": 2.1,
    "mean_final_rms_mm": 0.0215,
    "mean_current_norm_A": 0.74,
    "mean_latency_ms": 0.32
  },
  "best_track": "Track 2",
  "summary_of_modifications": "Introduced step-wise exponential gain decay triggered when RMS < 0.045 mm."
}
```

---

## 🏆 Main Agent Responsibilities: Leaderboard & Selection

The Main Agent (orchestrator):
1. **Monitors Worktrees:** Launches or messages the 10 subagents.
2. **Collects Results:** Receives completion payloads from all 10 agents.
3. **Persists Log:** Saves the full multi-agent experiment results to:
   `docs/experiments/multi_agent_benchmark_results.json`
4. **Calculates Official Rankings:**
   Sorts all 10 agents by their `challenge_score` in descending order.
5. **Declares Winner:** Identifies the top-ranking agent (`#1 Leader`), records winning hyperparameters and techniques, and presents a comparison table between Cohort A (Callback) and Cohort B (No-Callback).

---

## 🧹 Worktree Cleanup Protocol (After Benchmark Completion)

Once the experiment log is saved:
```bash
for i in $(seq 1 10); do
  git worktree remove --force "worktrees/agent-$i"
  git branch -D "agent-test-$i"
done
rm -rf worktrees
```
