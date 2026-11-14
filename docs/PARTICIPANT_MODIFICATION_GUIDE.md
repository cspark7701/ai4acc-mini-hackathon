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
| **Baseline 0** — Classical SVD (`Baseline0_LinearSVD`) | Step 4, `b0 = ClassicalSVDController(env.R, gain=0.45)` | Nothing; it is the fixed reference | The whole line, including `gain=0.45` (marked "DO NOT MODIFY - Standard Reference Baseline 0") |
| **Baseline 1 / Track 1** — Supervised MLP inversion (`Baseline1_SupervisedMLP`) | Step 3 (TODO 1) and Step 4 `b1 = …` | **TODO 1 MLP surrogate:** `hidden_layer_sizes`, `activation`, `solver`, `alpha`, `learning_rate_init`, `max_iter`<br>**Training data:** `n_samples`, `current_range`<br>**Ridge baseline:** `alpha`<br>**Controller:** the `b1` line (marked optional) | `noise_std=0.010` in data generation, the 80/20 train/test split, the test-RMSE evaluation lines |
| **Track 2** — Closed-loop RL / adaptive policy (`Track2_RLAgent`) | Step 4, TODO 2: class `MyCustomRLAgent` and `b2 = …` | **The whole `act()` design:** gain (`self.gain`), adaptive gain schedule, residual weights `W_tune` / `bias`, saturation compensation, damping factor<br>**Constructor and instantiation:** `__init__` contents and the `b2` line<br>**RL training:** reward-shaping parameters in Step 2 (`rms_weight`, `action_weight`, `step_penalty`, `success_bonus`, `reward_fn`) | The final `np.clip(…, -0.8, 0.8)` output bounds (hardware limits) |
| **Track 3** — Bayesian optimization (`Track3_BayesianOpt`) | Step 4, TODO 3: class `MyBayesianOptAgent`, GP fit, and `b3 = …` | **GP surrogate:** kernel (e.g. `Matern` length scale and `nu`, `WhiteKernel`), number of calibration shots (default 300), `normalize_y`<br>**Acquisition:** `kappa` (exploration), `l2_reg`, and the acquisition and optimizer inside `act()`<br>**Instantiation:** the `b3` line | Actions must stay within ±0.8 A per step |

---

## Shared settings

| Setting | Can modify | Must not modify |
| --- | --- | --- |
| Step 0 configuration | `TEAM_NAME` (your registered team name) | `WANDB_PROJECT`, `WANDB_ENTITY`, `USE_WANDB` |
| Step 2 environment | Reward-shaping weights; these only affect RL training, not the official score | Physics: `R`, `target_rms`, `max_steps = 50`, saturation `0.015`, BPM noise |
| Step 5 benchmark | — | The four `evaluate_hackathon_benchmark` calls and seeds `range(1, 31)` |
| Steps 1, 6, 7 | — | Beamline diagram, trajectory plots, showcase scorecard |

---

## Open issues in the notebook

These inconsistencies were found while compiling this guide and still need a decision or a fix.

1. **Callbacks:** the TODO 2 hints (Example D) suggest passing `step_callback` to the benchmark, but the
   Step 5 benchmark cell is marked DO NOT MODIFY, so there is no allowed place to pass one. Several agents
   in the multi-agent benchmark run used callbacks there, and some also used them to change Baseline 0's
   gain. Decide whether callbacks are allowed, and whether they may touch Baseline 0.
2. **Outdated hint:** TODO 2 hint 5 promises an "energy-efficiency score bonus" for low corrector current.
   Current norm is no longer scored, so that hint is now wrong.
3. **Outdated gain advice:** the gain hints recommend 0.55–0.72 and warn above 0.75. In the multi-agent
   benchmark run, gain 1.0 with saturation compensation scored best.
4. **Score precision:** the Step 7 showcase scorecard still prints the score with one decimal. The W&B
   record and the leaderboard table use three.
