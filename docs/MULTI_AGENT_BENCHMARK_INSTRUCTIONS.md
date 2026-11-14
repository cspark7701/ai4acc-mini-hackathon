# 🤖 Multi-Agent Benchmark Experiment Protocol & Agent Instructions

This document provides complete instructions for running a **10-agent autonomous benchmarking experiment** using the participant notebook ([notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb](file:///home/cspark/Work/projects/ai4acc-mini-hackathon/notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb)) on independent Git worktrees.

---

## 🎯 Experiment Mission & Division of Labor

Ten autonomous agents compete simultaneously to maximize the official accelerator orbit control score across 30 evaluation seeds (`range(1, 31)`). Each agent submits its final runs to the live Weights & Biases leaderboard, which also tests the participant submission path end to end.

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
3. **Submit Final Runs to the W&B Leaderboard:**
   - The final notebook run of every sub-agent submits to the live leaderboard project `ai4acc-mini-hackathon-2026` (entity `ai4acc-mini-hackathon-2026`). Keep `USE_WANDB = True`, `WANDB_PROJECT` and `WANDB_ENTITY` as preset in the notebook.
   - Authenticate with the shared service key, passed as the `WANDB_API_KEY` environment variable on the command that runs the notebook: `WANDB_API_KEY="$(cat /home/cspark/Work/projects/ai4acc-mini-hackathon/dist/wandb.apikey)"`. Do not call `wandb.login()`, and never print the key, write it into a notebook, or commit it.
   - **Tune offline, submit once.** All exploration and parameter sweeps run with `use_wandb=False`. Only the single final notebook execution logs to W&B, producing exactly four runs per agent (one per controller). Rerun the submission only if the first attempt logged nothing, and report the rerun.
4. **Limit CPU Threads:** Ten agents share one host. Prefix every Python or Jupyter command with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`, and run at most one process at a time per agent. Without these limits NumPy and scikit-learn oversubscribe the cores (a load average near 90 was observed on 8 cores) and every run slows down severalfold.
5. **Preserve Ground Truth Boundaries (Strict Benchmark Integrity):**
   - **Never** modify `src/environment.py` physics constants (`target_rms = 0.03`, `noise_std = 0.010`, `max_steps = 50`, or cubic saturation `0.015`).
   - Benchmark evaluation must strictly evaluate on `seeds = range(1, 31)`.
6. **Standardized Scoring Metric:**
   $$\text{Score} = \frac{1}{30}\sum_{k=1}^{30} s_k,\quad s_k = 400 + 300\,\max\!\left(0,\frac{20-n_k}{19}\right) + 300\,\mathrm{clip}\!\left(\frac{\ln(0.030/\text{RMS}_k)}{\ln 3},0,1\right)\ \text{(0 if seed } k \text{ fails)}$$
   Each seed scores 0 to 1000 points (`score_seed()` in `src/benchmark.py`).

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
Select a unique name that starts with the prefix **`MA_`** (e.g., `MA_A1_AdaptiveDamp`, `MA_A2_OnlineKalman`, `MA_B6_DeepSurrogate`, `MA_B7_AggressiveGain`). The prefix marks the runs as test submissions, so they can be filtered or deleted on the leaderboard. Set it in the notebook's configuration cell and leave the W&B settings as preset:
```python
TEAM_NAME = "MA_Your_Chosen_Name"
WANDB_PROJECT = "ai4acc-mini-hackathon-2026"   # unchanged
WANDB_ENTITY = "ai4acc-mini-hackathon-2026"    # unchanged
USE_WANDB = True                               # unchanged
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
  Pass the callback to the notebook's benchmark calls, keeping their W&B arguments:
  ```python
  res_b2 = evaluate_hackathon_benchmark(
      env, b2,
      agent_name="Track2_RLAgent",
      team_name=TEAM_NAME,
      use_wandb=USE_WANDB,
      project=WANDB_PROJECT,
      entity=WANDB_ENTITY,
      step_callback=custom_step_callback
  )
  ```

- **If in Cohort B (Agents 6–10):**
  Do not use callbacks. Optimize `TODO 1` surrogate architecture and `TODO 2` policy dynamics:
  - Hyperparameter sweeps on `MLPRegressor(hidden_layer_sizes=..., alpha=...)`.
  - Tuning `gain` $\in [0.50, 0.72]$ and damping function `damping = 1.0 / (1.0 + gamma * step)`.
  - Non-linear cubic desaturation: $\Delta \mathbf{I} + 0.015 \cdot \Delta \mathbf{I}^3$.

### Step 3: Offline Tuning
Explore and tune with standalone scripts that call the benchmark with W&B off, so no exploratory run reaches the leaderboard:
```python
res = evaluate_hackathon_benchmark(env, agent, agent_name="Track2_RLAgent", use_wandb=False)
```
Keep the tuning budget well under an hour. Before the final submission, check that every notebook cell still compiles (an edit error discovered during the submission run wastes it).

### Step 4: Final Submission to W&B
Execute the notebook **once**, from the worktree root, with the thread limits, the repository root on `PYTHONPATH`, and the shared key:
```bash
cd /home/cspark/Work/projects/ai4acc-mini-hackathon/worktrees/agent-N
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONPATH=. \
WANDB_API_KEY="$(cat /home/cspark/Work/projects/ai4acc-mini-hackathon/dist/wandb.apikey)" \
/home/cspark/Work/simulation_codes-working/miniforge3/envs/rl4aa26-challenge/bin/jupyter nbconvert \
  --to notebook \
  --execute notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb \
  --output Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb \
  --ExecutePreprocessor.timeout=1800
```
If the notebook's kernel metadata names a kernel that is not installed, add `--ExecutePreprocessor.kernel_name=<installed kernel>`.

Then check the executed notebook's output:
- Each of the four benchmark calls must print `[W&B] Logged '<TEAM_NAME>_<agent_name>' to <run URL> (Score: X pts)`.
- A `[W&B Warning] Logging skipped: ...` line means that run was not submitted; report its error text.
- Confirm the API key does not appear in the saved notebook (`grep -c wandb_v1` must print 0).

### Step 5: Report Results to Main Agent
Each sub-agent writes its final telemetry, including the W&B run of every controller, as a JSON payload and delivers it to the main agent:

```json
{
  "agent_id": 1,
  "agent_name": "MA_A1_AdaptiveDamp",
  "cohort": "A_Callback",
  "tracks": {
    "Track2_RLAgent": {
      "score": 944.7,
      "success_rate_pct": 100.0,
      "mean_steps": 1.6,
      "mean_final_rms_mm": 0.0116,
      "mean_current_norm_A": 0.94,
      "mean_latency_ms": 5.2,
      "wandb_run_name": "MA_A1_AdaptiveDamp_Track2_RLAgent",
      "wandb_url": "https://wandb.ai/ai4acc-mini-hackathon-2026/ai4acc-mini-hackathon-2026/runs/<run_id>"
    }
  },
  "best_track": "Track2_RLAgent",
  "best_score": 944.7,
  "summary_of_modifications": "Running-mean distortion estimate with exact saturation inversion; split moves larger than 0.8 A.",
  "notes": "Any problems, reruns, or use of information beyond the evaluation seeds."
}
```
`tracks` holds all four controllers (`Baseline0_LinearSVD`, `Baseline1_SupervisedMLP`, `Track2_RLAgent`, `Track3_BayesianOpt`). For a run that failed to log, replace `wandb_url` with `wandb_error`. Disclose in `notes` any technique that learns from earlier evaluation seeds or calibrates on simulator seeds outside `range(1, 31)`.

---

## 🏆 Main Agent Responsibilities: Leaderboard & Selection

The Main Agent (orchestrator):
1. **Monitors Worktrees:** Launches or messages the 10 subagents. Confirms beforehand that the shared key works and notes how many runs the leaderboard project already holds.
2. **Collects Results:** Receives completion payloads from all 10 agents.
3. **Verifies W&B Submissions:** Queries the W&B API directly, not the agents' reports, and checks that:
   - every agent's `MA_` team has exactly four runs, all in state `finished`, with no duplicates;
   - each run's `challenge_score`, `success_rate_pct`, `mean_steps` and `mean_final_rms_mm` match the agent's payload.
   ```python
   import wandb  # run with WANDB_API_KEY set to the shared key
   runs = wandb.Api().runs("ai4acc-mini-hackathon-2026/ai4acc-mini-hackathon-2026")
   ma = [r for r in runs if str(r.config.get("team", "")).startswith("MA_")]
   ```
4. **Persists Log:** Saves the full multi-agent experiment results, using the W&B-recorded values and run IDs, to:
   `docs/experiments/multi_agent_benchmark_results.json`
5. **Calculates Official Rankings:**
   Sorts all 10 agents by their best `challenge_score` in descending order.
6. **Declares Winner:** Identifies the top-ranking agent (`#1 Leader`), records winning hyperparameters and techniques, and presents a comparison table between Cohort A (Callback) and Cohort B (No-Callback).
7. **Reports Leaderboard Access:** Explains how to view the results at `https://wandb.ai/ai4acc-mini-hackathon-2026/ai4acc-mini-hackathon-2026` (Runs table, sort by `challenge_score`, group by `team`, filter `team` starting with `MA_`); see [`WANDB_LEADERBOARD_GUIDE.md`](WANDB_LEADERBOARD_GUIDE.md).
8. **Cleans Up Test Runs:** The `MA_` runs are on the real leaderboard. Delete them before the workshop (or keep selected ones as reference rows), and stop any watcher or monitor processes the subagents left running.

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
