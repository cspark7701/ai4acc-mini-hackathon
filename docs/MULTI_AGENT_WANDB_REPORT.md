# Multi-Agent W&B Submission Test — Report

**Date:** 2026-11-14
**Protocol:** [`MULTI_AGENT_BENCHMARK_INSTRUCTIONS.md`](MULTI_AGENT_BENCHMARK_INSTRUCTIONS.md), with one deliberate change: W&B submission was **on**, so the shared leaderboard could be tested end to end.
**Scoring:** per-seed 0–1000 points (`score_seed()` in `src/benchmark.py`), mean over seeds `range(1, 31)`.
**Raw data:** [`experiments/multi_agent_benchmark_results.json`](experiments/multi_agent_benchmark_results.json) (all values taken from W&B) and each agent's executed notebook in [`experiments/agent_notebooks/`](experiments/agent_notebooks/).

---

## 1. Result: every sub-agent's runs reached W&B

Ten sub-agents each ran the participant notebook once in their own git worktree. The notebook evaluates four controllers, so each agent submits four runs.

| Check | Result |
| --- | --- |
| Runs expected (10 agents × 4 controllers) | 40 |
| Runs found on W&B with a `MA_` team name | **40** |
| Teams with exactly 4 runs | **10 / 10** |
| Run state | all `finished` |
| Duplicate submissions | none |
| Agent-reported score, success, steps and RMS vs. W&B record | **40 / 40 match** |
| Notebooks containing the API key | none |
| Agents that modified `src/` or `tests/` | none |
| Benchmark calls on seeds other than `range(1, 31)` | none |

Runs were created between 12:59 and 13:02 UTC. The check queried the W&B API directly, so it does not rely on what the agents reported.

How the submission path works, as exercised here: each notebook kept `USE_WANDB = True`, `WANDB_ENTITY = WANDB_PROJECT = "ai4acc-mini-hackathon-2026"`, and received the shared service key as the `WANDB_API_KEY` environment variable, the same way the launchers pass `wandb.apikey`. No agent called `wandb.login()`.

---

## 2. How to see the leaderboard

1. Open **https://wandb.ai/ai4acc-mini-hackathon-2026/ai4acc-mini-hackathon-2026**
   W&B now redirects this to `https://forge.coreweave.com/wandb/ai4acc-mini-hackathon-2026/ai4acc-mini-hackathon-2026` (CoreWeave Forge). Both addresses work. Log in with an account that is a member of the `ai4acc-mini-hackathon-2026` team; the project is Team-only.
2. Switch to the **Runs** table (table icon in the left sidebar).
3. Click **Columns** and show `challenge_score`, `score_success`, `score_speed`, `score_precision`, `success_rate_pct`, `mean_steps`, `mean_final_rms_mm`, and the config fields `team` and `agent`. Pin `challenge_score`.
4. Click the `challenge_score` header and sort **descending**. Each row is one controller of one team.
5. For one row per team, **Group** by `team`. Grouped rows show an aggregate of their runs; set the aggregation for `challenge_score` to its maximum if you want each team's best controller rather than the mean of its four. (Aggregation options are in the column menu; check the label in your W&B version.)
6. To see only these test runs, add a filter `team` *starts with* `MA_`; to hide them, use *does not start with* `MA_`.
7. Save the layout as a view and use its URL on the projector. Full setup details are in [`WANDB_LEADERBOARD_GUIDE.md`](WANDB_LEADERBOARD_GUIDE.md).

Each run's page also holds the `seed_breakdown_table` with per-seed RMS, steps and score.

**Before the event:** these 40 test runs are on the real leaderboard. Delete them (select rows → Delete), or keep a few as reference rows.

---

## 3. Leaderboard (best controller per agent)

| Rank | Agent | Cohort | Best controller | Score | Success / speed / precision pts | Mean steps | Final RMS (mm) |
| :---: | --- | --- | --- | ---: | --- | ---: | ---: |
| 1 | `MA_B6_AggressiveGain` | B (no callbacks) | Track 2 | **955.0** | 400 / 291.1 / 264.0 | 1.57 | 0.0110 |
| 2 | `MA_B7_CubicCompensator` | B (no callbacks) | Track 3 | **954.8** | 400 / 291.6 / 263.2 | 1.53 | 0.0110 |
| 3 | `MA_A2_MomentumBraking` | A (callbacks) | Track 2 | **954.5** | 400 / 290.5 / 264.0 | 1.60 | 0.0110 |
| 4 | `MA_A5_OnlineResponseFit` | A (callbacks) | Track 2 | **945.9** | 400 / 290.5 / 255.4 | 1.60 | 0.0117 |
| 5 | `MA_A1_AdaptiveDamp` | A (callbacks) | Track 2 | **944.7** | 400 / 290.5 / 254.2 | 1.60 | 0.0116 |
| 6 | `MA_B10_StaticHybrid` | B (no callbacks) | Track 2 | **944.7** | 400 / 290.5 / 254.2 | 1.60 | 0.0116 |
| 7 | `MA_A3_MetaEpisodeTuner` | A (callbacks) | Track 2 | **943.1** | 400 / 291.6 / 251.5 | 1.53 | 0.0117 |
| 8 | `MA_A4_DualStageDecay` | A (callbacks) | Track 3 | **934.2** | 400 / 291.6 / 242.6 | 1.53 | 0.0122 |
| 9 | `MA_B9_BayesOptTuner` | B (no callbacks) | Track 3 | **920.9** | 400 / 291.6 / 229.4 | 1.53 | 0.0130 |
| 10 | `MA_B8_DeepTwinInversion` | B (no callbacks) | Baseline 1 | **920.8** | 400 / 291.6 / 229.2 | 1.53 | 0.0131 |

All 40 runs reached 100 % success, so every score has the full 400 success points. Differences come from speed and landing precision.

### All 40 runs

| Agent | Baseline 0 | Baseline 1 | Track 2 | Track 3 | W&B runs |
| --- | ---: | ---: | ---: | ---: | --- |
| `MA_A1_AdaptiveDamp` | 917.4 | 941.8 | 944.7 | 937.9 | 4 / 4 finished |
| `MA_A2_MomentumBraking` | 925.9 | 916.5 | 954.5 | 953.8 | 4 / 4 finished |
| `MA_A3_MetaEpisodeTuner` | 906.3 | 937.1 | 943.1 | 939.9 | 4 / 4 finished |
| `MA_A4_DualStageDecay` | 908.6 | 929.7 | 928.6 | 934.2 | 4 / 4 finished |
| `MA_A5_OnlineResponseFit` | 906.3 | 925.4 | 945.9 | 926.2 | 4 / 4 finished |
| `MA_B6_AggressiveGain` | 705.3 | 906.3 | 955.0 | 954.2 | 4 / 4 finished |
| `MA_B7_CubicCompensator` | 705.3 | 886.6 | 954.7 | 954.8 | 4 / 4 finished |
| `MA_B8_DeepTwinInversion` | 705.3 | 920.8 | 919.5 | 920.3 | 4 / 4 finished |
| `MA_B9_BayesOptTuner` | 705.3 | 894.0 | 919.5 | 920.9 | 4 / 4 finished |
| `MA_B10_StaticHybrid` | 705.3 | 906.6 | 944.7 | 943.5 | 4 / 4 finished |

### Per controller, compared with the unmodified reference code

| Controller | Reference code | Agents min | Agents mean | Agents max |
| --- | ---: | ---: | ---: | ---: |
| Baseline 0 | 705.3 | 705.3 | 809.1 | 925.9 |
| Baseline 1 | 371.0 | 886.6 | 916.5 | 941.8 |
| Track 2 | 686.9 | 919.5 | 941.0 | 955.0 |
| Track 3 | 873.2 | 920.3 | 938.6 | 954.8 |

### Cohort comparison (best score per agent)

| Cohort | Mean | Max | Min |
| --- | ---: | ---: | ---: |
| A — callbacks | 944.5 | 954.5 | 934.2 |
| B — no callbacks | 939.2 | 955.0 | 920.8 |

The cohorts are within about 5 points of each other; callbacks were not decisive. Track 2 was the best controller for 6 of 10 agents.

---

## 4. What the agents found

- **One technique carried every top score:** track the total corrector currents from `info["currents"]`, estimate the static orbit distortion as `obs − f(I)` averaged over the episode, and solve for the absolute currents that cancel it, including the exact inversion of the `I − 0.015·I³` saturation. With that, every controller converges in about 1.5 steps.
- **The ceiling is near 955 points.** On 16–18 of the 30 seeds the required correction exceeds the 0.8 A per-step limit, so 2 steps are unavoidable; agents B7 and B9 confirmed this with noise-free bounded solves. Final RMS bottoms out near 0.011 mm because of the 0.010 mm BPM noise.
- **"Stop short" landing guard (A1, A2, B10):** when two steps are unavoidable, deliberately leave a residual above about 0.05 mm after step 1, so the episode does not end early on a low-precision 0.025–0.029 mm reading. Worth about 25 points on Track 2 for A1.
- **Baseline 1 is fixed by a better surrogate.** Every agent replaced the MLP with a small `tanh` network trained with the `lbfgs` solver (for example `(64, 64)`, `alpha=1e-5`, 1500+ iterations). Test RMSE fell from 0.11 mm to 0.010–0.014 mm and Baseline 1 went from 56.7 % to 100 % success (371 → up to 941.8 points).
- **Lower gains near the target did not help.** Agents A1, A4 and B6 all found gain 1.0 best; the precision gain came from averaging the distortion estimate, not from damping.

---

## 5. Points that need a rules decision

Some agents used information that the protocol does not clearly allow or forbid. They disclosed it themselves.

| Agent | What it used | Why it matters |
| --- | --- | --- |
| A2, A3, A5 | `episode_callback` learns a prior (distortion directions or corrector covariance) from earlier **evaluation** seeds and applies it to later seeds in the same run | Online learning across test seeds; within the callback rules, but scores depend on seed order |
| B6, B7 | Calibrated a distortion prior by calling `env.reset()` on seeds 1000–3999 / 1000–1399, outside the evaluation set | No test-seed data, but relies on how the simulator generates distortions |
| A1, A4, B10 | Explicitly **declined** to exploit the fact that the distortion lies in the span of two rows of R | — |

Recommendation: state in the participant rules whether cross-seed learning in callbacks and calibration on non-evaluation seeds are allowed.

---

## 6. Observations about the scoring

The new score separated the reference controllers well (371–873), and every agent beat the reference. Among the optimised controllers the spread is much narrower: all ten agents' best scores lie within 35 points (920.8–955.0), and the top seven within 12, because they all reach the physical ceiling. Speed points are nearly identical (290.5–291.6), so ranks depend almost entirely on landing precision (229–264 of 300 points). If a wider spread among strong teams is wanted, precision would need more weight or a finer scale near the noise floor.

---

## 7. Execution notes

- **CPU overload.** Ten agents ran multi-threaded NumPy/scikit-learn at once on an 8-core host; load average reached about 88 and tuning slowed heavily. After the agents were told to set `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1` and run one process at a time, load fell to about 10. Add these limits to the protocol for future runs. Most agents cut tuning short as a result, so scores are not fully optimised.
- **Notebook runs.** Agents B7, A2 and B10 each started nbconvert twice; in every case the first attempt stopped before any W&B call, so no duplicate runs were created. Agent B6's final run started before the thread-limit message and ran multi-threaded.
- **Kernel and path.** The notebook's kernel metadata names `ai4acc`, and the notebook needs the repository root on `PYTHONPATH`. Agents passed `PYTHONPATH=.` or a kernel override.
- **Latency** values are inflated by the load and are not comparable to an idle machine.
- **Worktrees** were removed after the run, as the protocol requires. The executed notebooks are preserved in `docs/experiments/agent_notebooks/`.
