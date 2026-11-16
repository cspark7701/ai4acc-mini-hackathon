# Benchmark Callback Examples & Integration Guide

This guide explains how to use **step callbacks** and **episode callbacks** in the
[`notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb`](../notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb)
evaluation harness. It provides full data schemas, copy-pasteable implementation examples, registration patterns, and best practices.

---

## 🧭 Overview & Motivation

The standardized hackathon benchmark evaluates controllers across 30 pseudo-random seeds (`seeds = range(1, 31)`) using `evaluate_hackathon_benchmark()` in `src/benchmark.py`.

While standard controllers execute their `act(obs, info)` loop statically, **callbacks** provide an active hook into the simulation loop after each environment step and after each episode.

### Why Use Callbacks?
1. **State & Memory Resets:** Reset integrators, step counters or a modified gain between seeds.
2. **Online Learning & Surrogate Refinement:** Collect measurements during the run to update a GP or a neural surrogate online.
3. **Adaptive Gain or Damping:** Change controller parameters during an episode, for example near the target.
4. **Cross-Seed Adaptation:** Adjust hyperparameters from the outcome of earlier seeds (allowed, with disclosure).
5. **Telemetry & Diagnostics:** Record per-step trajectories and per-seed results for your presentation.

### What Testing Showed
A callback is a mechanism, not a guaranteed gain. Every example below was run through the 30-seed benchmark. The Track 2 rows use the notebook's `MyCustomRLAgent` with `gain=1.05`, which scores **747.0** without callbacks; the Track 3 rows use the notebook's reference controller, which scores **878.4**.

| Callback | Score | What happened |
| --- | :---: | --- |
| Example 1, near-target damping, **without** a reset | **241.0** (40% success) | The reduced gain carries over to the next seed and keeps shrinking. Always pair it with a reset. |
| Example 1, near-target damping, with the reset from Example 3 | 738.5 | Slightly below no callback: the damping costs more than it gains for this agent. |
| Example 2, saturation watchdog, with a reset | 729.9 | Lowering the gain above 2.5 A slows the 18 seeds that need such currents. |
| Example 4, cross-seed meta-tuner | 747.0 | No change: every seed takes 3 to 5 steps, so no rule fires. |
| Example 5, online GP refit (Track 3) | **882.9** | A small real gain over 878.4. |

Most of the available points come from the controller's `act()` design (gain, saturation compensation, surrogate accuracy), not from callbacks. Use callbacks where they add something `act()` cannot do, and measure the result each time.

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
| `info` | `dict` | Environment metadata **after** the step: `{"rms": float, "initial_rms": float, "step": int, "is_success": bool, "currents": np.ndarray (6,)}` |

The controller instance is passed as the second argument, `agent`; it is not a key of `step_data`. `obs` is the reading the controller acted on, and `next_obs`, `info["rms"]` and `info["currents"]` describe the state after the action.

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

As above, the controller instance is the second argument, `agent`. `elapsed_ms` includes the time spent in your callbacks.

---

## 💡 Practical Implementation Examples

### Example 1: Adaptive Near-Target Damping (`step_callback`)
**Objective:** Reduce the gain as the orbit error approaches the $0.030\text{ mm}$ target, so that the last kicks respond less to sensor noise.

```python
def adaptive_damping_step_callback(step_data: dict, agent: Any) -> None:
    """Reduces the agent gain when the orbit error enters the fine-tuning zone."""
    current_rms = step_data["info"]["rms"]

    if hasattr(agent, "gain"):
        if current_rms < 0.040:
            agent.gain *= 0.94
        elif current_rms < 0.100:
            agent.gain *= 0.98
```

> [!WARNING]
> **This callback must be paired with a gain reset (Example 3).** The agent object is reused for all 30 seeds, so a gain reduced in one episode stays reduced in the next. Run alone, this callback drops the notebook agent from 747.0 to **241.0** points with only 40% success. With the reset it scores 738.5, still slightly below no callback: an episode ends at the first reading below $0.030\text{ mm}$, so there is little to gain from braking just before it. Treat it as a pattern to adapt and measure, not as a ready-made improvement.

---

### Example 2: Saturation & Current Monitor (`step_callback`)
**Objective:** Watch the total corrector currents, reported in `step_data["info"]["currents"]`. The cubic term reduces the corrector strength by a fraction $0.015\,I^2$: 6% at 2 A, 9% at 2.5 A, 12% at 2.84 A (the largest current the evaluation seeds need) and 24% at 4 A.

```python
import numpy as np

def saturation_watchdog_step_callback(step_data: dict, agent: Any) -> None:
    """Lowers the gain once any corrector exceeds 2.5 A."""
    currents = step_data["info"]["currents"]
    max_current = np.max(np.abs(currents))

    if max_current > 2.5:
        if hasattr(agent, "gain"):
            agent.gain = min(agent.gain, 0.70)
```

**Measured effect:** 18 of the 30 seeds need more than 2.5 A, so this rule fires often and slows them: 729.9 points with a gain reset against 747.0 without the callback (683.3 if the gain is not reset). Raising `l2_reg` to 0.05 in the Track 3 controller the same way lowers it from 878.4 to 866.0. Under saturation the response is *weaker* than the linear model predicts, so a controller needs larger kicks at high current, not smaller ones. The effective fix is to compensate the saturation inside `act()` using the total current (TODO 2, hint 4), which reaches about 924 points. Use this callback pattern for monitoring or logging rather than for throttling.

---

### Example 3: Per-Seed State Reset (`episode_callback`)
**Objective:** Restore anything a step callback changed, so that every seed starts from the same controller state. The factory below remembers the gain the agent had when the callback was created, so it works with any agent that has a `gain` attribute.

```python
def make_gain_reset(agent: Any):
    """Returns an episode_callback that restores the agent's original gain after every seed."""
    initial_gain = agent.gain

    def reset_episode_callback(episode_data: dict, agent: Any) -> None:
        agent.gain = initial_gain
        # Reset any other per-episode state your agent keeps:
        if hasattr(agent, "integral_error"):
            agent.integral_error = np.zeros(6)

    return reset_episode_callback

# Create it after the agent, and register it together with the step callback:
#   b2 = MyCustomRLAgent(env.R, gain=1.05)
#   CALLBACKS["b2"] = {"step_callback": adaptive_damping_step_callback,
#                      "episode_callback": make_gain_reset(b2)}
```

`episode_callback` runs after each seed finishes, before the next `env.reset()`.

---

### Example 4: Cross-Seed Meta-Tuning (`episode_callback`)
**Objective:** Adjust the base gain for later seeds from the outcome of earlier ones. This carries information across seeds, so it falls under the disclosure rule.

```python
class MetaGainTuner:
    """Adapts the starting controller gain across evaluation seeds."""
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
                # A failed seed: reduce the gain for safety
                self.default_gain = max(0.60, self.default_gain * 0.85)
            elif steps > 6:
                # Slow convergence: reduce slightly
                self.default_gain = max(0.75, self.default_gain * 0.95)
            elif steps <= 3 and final_rms < 0.020:
                # Fast, precise convergence: increase slightly
                self.default_gain = min(1.20, self.default_gain * 1.02)

            # Apply the updated gain for the next seed
            agent.gain = self.default_gain

meta_tuner = MetaGainTuner(default_gain=1.05)
# CALLBACKS["b2"] = {"step_callback": None, "episode_callback": meta_tuner.on_episode_end}
```

**Measured effect:** with the notebook agent at gain 1.05 the score stays at 747.0. Every seed converges in 3 to 5 steps, the 3-step seeds land above $0.020\text{ mm}$, and so none of the three rules fires. To make such a tuner useful, choose thresholds that your controller actually crosses, and compare against simply setting a better constant gain (a constant 1.2 scores 808.9 for this agent).

---

### Example 5: Online Gaussian Process Refit for Track 3 (`step_callback`)
**Objective:** Add the measurements taken during the benchmark to the GP's training data and refit it, turning the fixed offline model into online Bayesian optimization.

Two details matter:
- The GP models the corrector **response** $f(\mathbf{I})$, while a BPM reading is response plus the unknown initial distortion $\mathbf{Y}_0$. The first reading of each episode is taken at $\mathbf{I} = \mathbf{0}$, where the response is zero, so it measures $\mathbf{Y}_0$. The response at later currents is therefore `next_obs - first_obs`.
- Refit from the original training arrays. Do not read them back from `gp.y_train_`, which holds normalized values when `normalize_y=True`.

```python
class OnlineGPRefit:
    """Adds each (currents, response) measurement to the GP data and refits the GP."""
    def __init__(self, X_calib, Y_calib, refit_every: int = 1, max_new: int = 200):
        self.X_calib, self.Y_calib = X_calib, Y_calib   # original calibration data
        self.X_new, self.Y_new = [], []
        self.first_obs = None
        self.refit_every, self.max_new, self.count = refit_every, max_new, 0

    def step(self, step_data: dict, agent: Any) -> None:
        if step_data["step"] == 1:
            # Reading at zero current: the initial distortion Y0 of this seed
            self.first_obs = np.asarray(step_data["obs"], dtype=float)
        currents = np.asarray(step_data["info"]["currents"], dtype=float)
        response = np.asarray(step_data["next_obs"], dtype=float) - self.first_obs
        self.X_new.append(currents)
        self.Y_new.append(response)
        self.count += 1
        if self.count % self.refit_every == 0:
            agent.gp.fit(np.vstack([self.X_calib] + self.X_new[-self.max_new:]),
                         np.vstack([self.Y_calib] + self.Y_new[-self.max_new:]))

online_gp = OnlineGPRefit(X_train[:300], Y_train[:300])
# CALLBACKS["b3"] = {"step_callback": online_gp.step, "episode_callback": None}
```

**Measured effect:** 882.9 points against 878.4 for the fixed GP when refitting after every step (880.4 when refitting every 5 steps). The run takes about 23 s instead of 5 s, because the GP is refitted about 110 times. The gain is small because the 300 calibration shots already cover the currents the correction needs. The new data stays in the model for later seeds, so disclose this in your presentation.

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
Navigate to the **Step 4** notebook cell. Define your callback functions or class instances above the `CALLBACKS` dictionary, after the controller they act on:

```python
# --- Your Custom Callbacks (after  b2 = MyCustomRLAgent(env.R, gain=1.05)) ---
def track2_step_cb(step_data, agent):
    # Reduce the gain when approaching the target RMS
    if step_data["info"]["rms"] < 0.040:
        agent.gain *= 0.95

TRACK2_GAIN = b2.gain   # remember the gain the agent starts with

def track2_ep_cb(episode_data, agent):
    # Restore the starting gain for the next seed (required whenever a callback changes it)
    agent.gain = TRACK2_GAIN
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

With `gain=1.05` this pair scores 744.9 against 747.0 without callbacks: it shows the mechanics, and it is a starting point for your own experiments rather than an improvement in itself.

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

1. **Check That Your Callback Acts:**  
   A guard such as `if hasattr(agent, "gain"): ...` avoids an `AttributeError`, but it also hides mistakes: if the attribute name is wrong, the callback silently does nothing. Print or assert once to confirm that the attribute exists and changes.
2. **Keep Step Callbacks Lightweight:**  
   `step_callback` runs on every simulation step. Heavy computations (e.g., long optimization loops or disk I/O) will increase `mean_latency_ms` and slow down benchmark execution.
3. **Avoid Unbounded Gain Growth:**  
   If your callback multiplies gain (e.g., `agent.gain *= 1.05`), ensure it has an upper bound (e.g., `min(agent.gain, 1.25)`). Unbounded gains lead to severe overshoot, actuator clipping, and benchmark divergence.
4. **Always Reset What You Change:**  
   The same agent object is used for all 30 seeds. If a step callback lowers `agent.gain` and nothing restores it, the gain keeps shrinking from seed to seed: the near-target damping of Example 1 alone drops the notebook agent from 747.0 to 241.0 points with 40% success. Restore the starting value in an `episode_callback` (Example 3).
5. **Measure Every Callback:**  
   Compare the benchmark score with and without the callback. Several plausible ideas (near-target braking, throttling at high current) lowered the score in testing.
6. **Baseline 0 Has No Callbacks:**  
   Do not register callbacks for `b0`. Baseline 0 is the fixed classical SVD benchmark and is evaluated without callbacks to preserve standard comparisons across all teams.
