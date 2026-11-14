# What Participants Can Modify

This guide lists, for each of the four benchmarked controllers, what participants may change in
[`notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb`](../notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb)
and what must stay fixed. It follows the `[CAN MODIFY]` and `[DO NOT MODIFY]` markers in the notebook.

The notebook benchmarks four controllers, and each is submitted to the leaderboard as its own W&B run:
**Baseline 0**, **Baseline 1** (also called **Track 1** in the notebook), **Track 2** and **Track 3**.

---

## Per controller

| Controller (W&B run name) | Where in the notebook | Participants **can** modify | Participants **must not** modify |
| --- | --- | --- | --- |
| **Baseline 0** — Classical SVD (`Baseline0_LinearSVD`) | Step 4, `b0 = ClassicalSVDController(env.R, gain=0.45)` | Nothing; it is the fixed reference | The whole line, including `gain=0.45` (marked "DO NOT MODIFY - Standard Reference Baseline 0"). Baseline 0 always runs without callbacks |
| **Baseline 1 / Track 1** — Supervised MLP inversion (`Baseline1_SupervisedMLP`) | Step 3 (TODO 1) and Step 4 `b1 = …` | **TODO 1 MLP surrogate:** `hidden_layer_sizes`, `activation`, `solver`, `alpha`, `learning_rate_init`, `max_iter`<br>**Training data:** `n_samples`, `current_range`<br>**Ridge baseline:** `alpha`<br>**Controller:** the `b1` line (marked optional)<br>**Callbacks:** `CALLBACKS["b1"]` in Step 4 | `noise_std=0.010` in data generation, the 80/20 train/test split, the test-RMSE evaluation lines |
| **Track 2** — Closed-loop RL / adaptive policy (`Track2_RLAgent`) | Step 4, TODO 2: class `MyCustomRLAgent` and `b2 = …` | **The whole `act()` design:** gain (`self.gain`), adaptive gain schedule, residual weights `W_tune` / `bias`, saturation compensation, damping factor<br>**Constructor and instantiation:** `__init__` contents and the `b2` line<br>**RL training:** reward-shaping parameters in Step 2 (`rms_weight`, `action_weight`, `step_penalty`, `success_bonus`, `reward_fn`)<br>**Callbacks:** `CALLBACKS["b2"]` in Step 4 | The final `np.clip(…, -0.8, 0.8)` output bounds (hardware limits) |
| **Track 3** — Bayesian optimization (`Track3_BayesianOpt`) | Step 4, TODO 3: class `MyBayesianOptAgent`, GP fit, and `b3 = …` | **GP surrogate:** kernel (e.g. `Matern` length scale and `nu`, `WhiteKernel`), number of calibration shots (default 300), `normalize_y`<br>**Acquisition:** `kappa` (exploration), `l2_reg`, and the acquisition and optimizer inside `act()`<br>**Instantiation:** the `b3` line<br>**Callbacks:** `CALLBACKS["b3"]` in Step 4 | Actions must stay within ±0.8 A per step |

---

## Shared settings

| Setting | Can modify | Must not modify |
| --- | --- | --- |
| Step 0 configuration | `TEAM_NAME` (your registered team name) | `WANDB_PROJECT`, `WANDB_ENTITY`, `USE_WANDB` |
| Step 2 environment | Reward-shaping weights; these only affect RL training, not the official score | Physics: `R`, `target_rms`, `max_steps = 50`, saturation `0.015`, BPM noise |
| Step 4 callbacks | `CALLBACKS`: a `step_callback` and/or `episode_callback` for Baseline 1, Track 2 and Track 3 | Callbacks for Baseline 0 (it has no entry) |
| Step 5 benchmark | — | The four `evaluate_hackathon_benchmark` calls and seeds `range(1, 31)`; they pass your `CALLBACKS` automatically |
| Steps 1, 6, 7 | — | Beamline diagram, trajectory plots, showcase scorecard |

---

## Callback rules

Callbacks let a controller adapt online while the benchmark runs.

- **Allowed for:** Baseline 1, Track 2 and Track 3. Define the function in the Step 4 cell and register it in
  `CALLBACKS`, for example `"b2": {"step_callback": my_step_callback, "episode_callback": None}`. The
  locked Step 5 cell passes each entry to its benchmark call.
- **Not allowed for:** Baseline 0, which stays the fixed reference.
- **Signatures:** `step_callback(step_data, agent)` runs after every environment step, with `step_data`
  holding `seed`, `step`, `obs`, `action`, `reward`, `next_obs`, `terminated`, `truncated` and `info`.
  `episode_callback(episode_data, agent)` runs after each seed, with `seed`, `steps`, `initial_rms`,
  `final_rms`, `is_success`, `current_norm`, `elapsed_ms` and `info`.
- **Disclosure:** a callback that carries information from earlier evaluation seeds into later ones
  (for example a prior learned across seeds) is allowed, but say so in your team presentation.
