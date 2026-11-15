# Benchmark Callback Examples & Integration Guide

This guide explains how to use **step callbacks** and **episode callbacks** in the
[`notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb`](../notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb)
evaluation harness. It provides full data schemas, copy-pasteable implementation examples, registration patterns, and best practices.

---

## 🧭 Overview & Motivation

The standardized hackathon benchmark evaluates controllers across 30 pseudo-random seeds (`seeds = range(1, 31)`) using `evaluate_hackathon_benchmark()` in `src/benchmark.py`.

While standard controllers execute their `act(obs, info)` loop statically, **callbacks** provide an active hook into the simulation loop after each environment step and after each episode.

### Why Use Callbacks?
1. **Adaptive Precision Landing:** Throttle controller gain when orbit error drops below $0.050\text{ mm}$ to glide smoothly toward the $0.010\text{ mm}$ sensor noise floor without oscillation.
2. **Actuator & Saturation Watchdogs:** Monitor total current draw ($\mathbf{I}$) and prevent correctors from operating deep in non-linear cubic saturation.
3. **State & Memory Resets:** Cleanly reset internal integrator states, step counters, or momentum buffers between seeds.
4. **Online Learning & Surrogate Refinement:** Collect active transition data $(I, Y)$ to update GP kernels or fine-tune neural surrogates online.
5. **Cross-Seed Meta-Adaptation:** Adapt hyperparameters across seeds based on aggregate performance metrics (e.g., the Cohort A winning strategy from Tournament 3).
6. **Detailed Telemetry & Diagnostics:** Track per-step trajectories, convergence rates, and actuator energy for post-run presentation slides.

---

## 📋 Callback Rules & Permissions

| Controller / Track | Callbacks Allowed? | Registration Key in `CALLBACKS` |
| --- | :---: | :---: |
| **Baseline 0** — Classical Linear SVD (`Baseline0_LinearSVD`) | ❌ **No** | None (always evaluated without callbacks as the fixed reference) |
| **Baseline 1 / Track 1** — Supervised MLP Inversion (`Baseline1_SupervisedMLP`) | ✅ **Yes** | `CALLBACKS["b1"]` |
| **Track 2** — Closed-Loop RL / Adaptive Policy (`Track2_RLAgent`) | ✅ **Yes** | `CALLBACKS["b2"]` |
| **Track 3** — Bayesian Optimization (`Track3_BayesianOpt`) | ✅ **Yes** | `CALLBACKS["b3"]` |

> [!IMPORTANT]
> **Presentation Disclosure Rule:** Callbacks that carry information across seeds (such as meta-learned gains or persistent cross-seed online models) are fully permitted under the challenge rules, but you **must disclose** this architectural feature in your team's final 3-minute presentation.

---

## 🔍 Data Signatures & Schemas

### 1. `step_callback(step_data: dict, agent: Any) -> None`
Invoked immediately after `env.step(action)` executes inside `src/benchmark.py`.

```python
def my_step_callback(step_data: dict, agent: Any) -> None:
    ...
```

#### Fields in `step_data`:
| Key | Type | Description |
| --- | --- | --- |
| `seed` | `int` | Current evaluation seed index (1 to 30) |
| `step` | `int` | 1-based step counter for the current episode (1 to 50) |
| `obs` | `np.ndarray` (12,) | BPM readings at the start of the step in mm |
| `action` | `np.ndarray` (6,) | Delta current vector applied by the agent in A (clipped to $[-0.8, 0.8]$) |
| `reward` | `float` | Reward returned by environment (for RL training telemetry) |
| `next_obs` | `np.ndarray` (12,) | BPM readings after applying the action in mm |
| `terminated` | `bool` | `True` if residual $\text{RMS} < 0.030\text{ mm}$ (success criterion met) |
| `truncated` | `bool` | `True` if `step >= 50` without reaching target RMS |
| `info` | `dict` | Environment metadata: `{"rms": float, "initial_rms": float, "step": int, "is_success": bool, "currents": np.ndarray (6,)}` |
| `agent` | `Any` | Direct reference to the active controller instance being evaluated |

---

### 2. `episode_callback(episode_data: dict, agent: Any) -> None`
Invoked once per evaluation seed after the episode finishes (upon termination, truncation, or reaching `max_steps`).

```python
def my_episode_callback(episode_data: dict, agent: Any) -> None:
    ...
```

#### Fields in `episode_data`:
| Key | Type | Description |
| --- | --- | --- |
| `seed` | `int` | Evaluation seed index (1 to 30) |
| `steps` | `int` | Total steps taken to complete or truncate the episode |
| `initial_rms` | `float` | Starting orbit distortion in mm before any action |
| `final_rms` | `float` | Final residual orbit error in mm upon episode conclusion |
| `is_success` | `bool` | `True` if episode reached $\text{RMS} < 0.030\text{ mm}$ |
| `current_norm` | `float` | Final Euclidean norm of total corrector currents $\|\mathbf{I}\|_2$ in A |
| `elapsed_ms` | `float` | Wall-clock execution time for this seed in milliseconds |
| `info` | `dict` | Final step metadata dictionary from environment |
| `agent` | `Any` | Direct reference to the active controller instance |

---

## 💡 Practical Implementation Examples

### Example 1: Adaptive Near-Target Damping (`step_callback`)
**Objective:** Prevent terminal oscillations around the $0.030\text{ mm}$ success boundary and maximize the precision score (earning up to 300 points as RMS approaches the $0.010\text{ mm}$ sensor noise floor).

```python
def adaptive_damping_step_callback(step_data: dict, agent: Any) -> None:
    """Dynamically throttles agent gain when orbit error enters the fine-tuning zone."""
    current_rms = step_data["info"]["rms"]

    if hasattr(agent, "gain"):
        if current_rms < 0.040:
            # Entering precision zone: damp aggressively to settle into sensor noise floor
            agent.gain *= 0.94
        elif current_rms < 0.100:
            # Moderate damping to avoid overshoot
            agent.gain *= 0.98
```

---

### Example 2: Saturation & Current Limit Watchdog (`step_callback`)
**Objective:** Monitor total magnet current $\mathbf{I} = \sum \Delta \mathbf{I}$. When correctors approach hardware limits ($\pm 5.0\text{ A}$) or strong cubic saturation ($|\mathbf{I}| > 2.5\text{ A}$), adjust the agent's regularizer or scale actions back.

```python
import numpy as np

def saturation_watchdog_step_callback(step_data: dict, agent: Any) -> None:
    """Monitors corrector currents and dampens aggressive steps if saturation is detected."""
    currents = step_data["info"]["currents"]
    max_current = np.max(np.abs(currents))

    # Cubic non-linearity term is -0.015 * I^3 * R.
    # At I = 2.5 A, non-linear error is ~23% of linear response.
    if max_current > 2.5:
        if hasattr(agent, "gain"):
            # Reduce step size to avoid non-linear overshoots
            agent.gain = min(agent.gain, 0.70)
        if hasattr(agent, "l2_reg"):
            # Increase regularizer in optimization-based controllers
            agent.l2_reg = max(agent.l2_reg, 0.05)
```

---

### Example 3: Per-Seed State Reset (`episode_callback`)
**Objective:** If your agent maintains internal state (such as an accumulator, momentum vector, or dynamic gain), use `episode_callback` to reset it at the start of each new seed so previous seeds do not cause drift.

```python
def state_reset_episode_callback(episode_data: dict, agent: Any) -> None:
    """Resets internal controller state back to initial values after every seed."""
    # Reset internal gain if agent was dynamically damped during the episode
    if hasattr(agent, "initial_gain") and hasattr(agent, "gain"):
        agent.gain = agent.initial_gain

    # Reset any integrator or momentum memory
    if hasattr(agent, "integral_error"):
        agent.integral_error = np.zeros(6)
    if hasattr(agent, "step_count"):
        agent.step_count = 0
```

---

### Example 4: Cross-Seed Meta-Tuning (`episode_callback`)
**Objective:** The winning strategy from Tournament 3 Cohort A. Learn from previous seed outcomes to adjust the base gain for subsequent seeds. If previous seeds succeeded in $\le 3$ steps, maintain aggressive gains; if any seed required $> 5$ steps or failed, introduce conservative damping.

```python
class MetaGainTuner:
    """Meta-learner that adapts starting controller gain across evaluation seeds."""
    def __init__(self, default_gain: float = 1.05):
        self.default_gain = default_gain
        self.history = []

    def on_episode_end(self, episode_data: dict, agent: Any) -> None:
        steps = episode_data["steps"]
        success = episode_data["is_success"]
        final_rms = episode_data["final_rms"]

        self.history.append((steps, success, final_rms))

        if hasattr(agent, "gain"):
            if not success:
                # If a seed failed, significantly dial back gain for safety
                self.default_gain = max(0.60, self.default_gain * 0.85)
            elif steps > 6:
                # Slower convergence suggests mild oscillation: damp slightly
                self.default_gain = max(0.75, self.default_gain * 0.95)
            elif steps <= 3 and final_rms < 0.020:
                # Clean, rapid convergence: slightly boost speed
                self.default_gain = min(1.20, self.default_gain * 1.02)

            # Re-apply updated baseline gain to agent for next seed
            agent.gain = self.default_gain

meta_tuner = MetaGainTuner(default_gain=1.05)
```

---

### Example 5: Online Bayesian Optimization Model Refinement (`step_callback`)
**Objective:** Collect observed $(I_t, Y_t)$ transitions during benchmark execution and incrementally update the Gaussian Process training dataset or hyperparameters online.

```python
def online_gp_update_step_callback(step_data: dict, agent: Any) -> None:
    """Optionally caches online measurements to augment GP training data."""
    if hasattr(agent, "gp") and hasattr(agent, "X_train_") and hasattr(agent, "y_train_"):
        currents = step_data["info"]["currents"].reshape(1, -1)
        bpm_reading = step_data["next_obs"].reshape(1, -1)

        # Store sample into agent cache
        if not hasattr(agent, "online_buffer_X"):
            agent.online_buffer_X = []
            agent.online_buffer_y = []

        agent.online_buffer_X.append(currents)
        agent.online_buffer_y.append(bpm_reading)

        # Periodically refit GP every 10 collected samples
        if len(agent.online_buffer_X) % 10 == 0:
            X_aug = np.vstack([agent.X_train_] + agent.online_buffer_X[-10:])
            y_aug = np.vstack([agent.y_train_] + agent.online_buffer_y[-10:])
            agent.gp.fit(X_aug, y_aug)
```

---

### Example 6: Modular Telemetry & Diagnostic Logger Class
**Objective:** An all-in-one stateful callback object that tracks performance across all steps and episodes, calculating statistics and latencies without modifying the agent class.

```python
class DiagnosticTelemetryLogger:
    """Self-contained logger capturing per-step and per-seed performance metrics."""
    def __init__(self):
        self.step_records = []
        self.episode_records = []

    def step_hook(self, step_data: dict, agent: Any) -> None:
        self.step_records.append({
            "seed": step_data["seed"],
            "step": step_data["step"],
            "rms": step_data["info"]["rms"],
            "action_norm": float(np.linalg.norm(step_data["action"])),
            "current_norm": float(np.linalg.norm(step_data["info"]["currents"])),
        })

    def episode_hook(self, episode_data: dict, agent: Any) -> None:
        self.episode_records.append({
            "seed": episode_data["seed"],
            "steps": episode_data["steps"],
            "initial_rms": episode_data["initial_rms"],
            "final_rms": episode_data["final_rms"],
            "is_success": episode_data["is_success"],
            "elapsed_ms": episode_data["elapsed_ms"],
        })

    def summary(self) -> None:
        if not self.episode_records:
            print("No episodes recorded yet.")
            return
        succs = [r["is_success"] for r in self.episode_records]
        steps = [r["steps"] for r in self.episode_records]
        rms = [r["final_rms"] for r in self.episode_records]
        print(f"Recorded {len(self.episode_records)} seeds:")
        print(f"  Success Rate: {100.0 * sum(succs) / len(succs):.1f}%")
        print(f"  Mean Steps:   {np.mean(steps):.2f}")
        print(f"  Mean Final RMS: {np.mean(rms):.4f} mm")

# Instantiate logger
telemetry = DiagnosticTelemetryLogger()
```

---

## 🛠️ Step-by-Step Registration in the Participant Notebook

To use your callbacks in [`Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb`](../notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb):

### Step 1: Define Your Callbacks in Step 4
Navigate to the **Step 4** notebook cell. Define your callback functions or class instances directly above the `CALLBACKS` dictionary:

```python
# --- Your Custom Callbacks ---
def track2_step_cb(step_data, agent):
    # Precision damping when approaching target RMS
    if step_data["info"]["rms"] < 0.040 and hasattr(agent, "gain"):
        agent.gain *= 0.95

def track2_ep_cb(episode_data, agent):
    # Reset starting gain for next seed
    if hasattr(agent, "gain"):
        agent.gain = 1.05
```

### Step 2: Register in the `CALLBACKS` Dictionary
At the bottom of Step 4, assign your functions to the appropriate controller key:

```python
# ==============================================================================
# Optional callbacks for Baseline 1, Track 2 and Track 3
# ==============================================================================
CALLBACKS = {
    "b1": {"step_callback": None, "episode_callback": None},
    "b2": {"step_callback": track2_step_cb, "episode_callback": track2_ep_cb},
    "b3": {"step_callback": None, "episode_callback": None},
}
```

### Step 3: Execute Step 5 Benchmark
Run the locked Step 5 evaluation cell. It automatically unpacks your registered callbacks into the benchmark runner:

```python
# Step 5 benchmark invocation (locked cell):
res_b2 = evaluate_hackathon_benchmark(
    env,
    b2,
    agent_name="Track2_RLAgent",
    team_name=TEAM_NAME,
    use_wandb=USE_WANDB,
    project=WANDB_PROJECT,
    entity=WANDB_ENTITY,
    **CALLBACKS["b2"]  # <-- Passes your step_callback and episode_callback automatically!
)
```

---

## ⚠️ Common Pitfalls & Best Practices

1. **Check Attribute Existence with `hasattr()`:**  
   Always verify attributes before modifying them (e.g. `if hasattr(agent, "gain"): ...`). This ensures your callback does not raise an `AttributeError` if tested with different agent classes.
2. **Keep Step Callbacks Lightweight:**  
   `step_callback` runs on every simulation step. Heavy computations (e.g., long optimization loops or disk I/O) will increase `mean_latency_ms` and slow down benchmark execution.
3. **Avoid Unbounded Gain Growth:**  
   If your callback multiplies gain (e.g., `agent.gain *= 1.05`), ensure it has an upper bound (e.g., `min(agent.gain, 1.25)`). Unbounded gains lead to severe overshoot, actuator clipping, and benchmark divergence.
4. **Remember Episode Reset:**  
   If you adapt `agent.gain` downward during an episode, remember to restore the initial gain in `episode_callback`. Otherwise, later seeds will start with an excessively low gain and take many steps to converge.
5. **Baseline 0 Has No Callbacks:**  
   Do not register callbacks for `b0`. Baseline 0 is the fixed classical SVD benchmark and is evaluated without callbacks to preserve standard comparisons across all teams.
