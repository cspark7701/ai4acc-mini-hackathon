# 📊 Multi-Agent Tournament Report 3: 6-Kick Non-Linear Orbit Alignment Benchmark

**Document Location:** [docs/MULTI_AGENT_TOURNAMENT_REPORT3.md](MULTI_AGENT_TOURNAMENT_REPORT3.md)  
**Experiment Date:** November 15, 2026  
**Benchmark Configuration:** Hardened 6-Kick Initial Distortion ($\mathbf{Y}_0 = \mathbf{a} \cdot \mathbf{R}$, $a_k \sim \mathcal{U}(-2.5, 2.5)\text{ A}$, initial RMS $0.93$–$3.59\text{ mm}$), evaluated on 30 standardized seeds (`range(1, 31)`).  
**Telemetry Destination:** Weights & Biases Project [`ai4acc-mini-hackathon-2026/ai4acc-mini-hackathon-2026`](https://wandb.ai/ai4acc-mini-hackathon-2026/ai4acc-mini-hackathon-2026)  
**Worktree Status:** Executed in 10 isolated git worktrees (`worktrees/agent-1` through `worktrees/agent-10`) and wiped post-run.

---

## 🏆 Executive Summary & Official Tournament 3 Leaderboard

A comprehensive multi-agent tournament was executed across **10 autonomous competitor agents** divided into two cohorts:
- **Cohort A (Agents 1–5):** Online Adaptive Callback-Driven Agents (leveraging `step_callback` and `episode_callback`).
- **Cohort B (Agents 6–10):** Architectural, Parameter & Analytical Optimization Agents (offline tuning, static policies, no callbacks).

### Overall Official Leaderboard (Ranked by Best Score Across All Tracks)

| Rank | Agent Name | Cohort | Winning Track / Architecture | Best Score | Success Rate | Mean Steps | Mean Final RMS | Current Norm $\|\mathbf{I}\|$ |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **🥇 #1** | **`MA_B7_CubicCompensator`** | **Cohort B** | **Track 2 (Exact Newton Desaturation)** | **923.703 pts** | **100.0%** | **3.67** | **0.01100 mm** | **3.85 A** |
| **🥈 #2** | `MA_B8_DeepTwinInversion` | Cohort B | Track 2 (Deep Surrogate + Newton Inversion) | **911.727 pts** | 100.0% | 3.63 | 0.01190 mm | 3.85 A |
| **🥉 #3** | `MA_A3_MetaEpisodeTuner` | Cohort A | Track 2 (Cross-Seed Episode Meta-Tuner) | **883.565 pts** | 100.0% | 3.67 | 0.01340 mm | 3.86 A |
| **#4** | `MA_B10_OptimalStaticHybrid` | Cohort B | Track 3 (Bayesian Optimization) | **878.382 pts** | 100.0% | 3.63 | 0.01360 mm | 3.85 A |
| **#5** | `MA_A5_EnergyAwareLimiter` | Cohort A | Track 3 (Bayesian Optimization) | **878.382 pts** | 100.0% | 3.63 | 0.01360 mm | 3.85 A |
| **#6** | `MA_A4_DualStageDecay` | Cohort A | Track 3 (Bayesian Optimization) | **878.382 pts** | 100.0% | 3.63 | 0.01360 mm | 3.85 A |
| **#7** | `MA_A2_MomentumBraking` | Cohort A | Track 3 (Bayesian Optimization) | **878.382 pts** | 100.0% | 3.63 | 0.01360 mm | 3.85 A |
| **#8** | `MA_B6_AggressiveGain` | Cohort B | Track 3 (Bayesian Optimization) | **878.382 pts** | 100.0% | 3.63 | 0.01360 mm | 3.85 A |
| **#9** | `MA_B9_UltraConservative` | Cohort B | Track 3 (Bayesian Optimization) | **878.382 pts** | 100.0% | 3.63 | 0.01360 mm | 3.85 A |
| **#10** | `MA_A1_AdaptiveDamp` | Cohort A | Track 3 (Bayesian Optimization) | **878.382 pts** | 100.0% | 3.63 | 0.01360 mm | 3.85 A |

---

## 🥊 Track 2 Head-to-Head Showdown: Custom Adaptive & RL Policies

Track 2 (`Track2_RLAgent`) tests each team's custom closed-loop feedback policy under non-linear cubic iron core saturation. Here is the definitive ranking of all 10 agent policies:

| Rank | Agent Name | Cohort | Strategy / Architecture | Track 2 Score | Success Rate | Mean Steps | Mean Final RMS | Latency |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **🥇 #1** | **`MA_B7_CubicCompensator`** | **Cohort B** | **Newton field inversion ($\alpha=1.00$, $\gamma=0$)** | **923.703 pts** | **100.0%** | **3.67** | **0.01100 mm** | **0.22 ms** |
| **🥈 #2** | `MA_B8_DeepTwinInversion` | Cohort B | Newton inversion ($\alpha=1.05$, $\gamma=0.018$) | **911.727 pts** | 100.0% | 3.63 | 0.01190 mm | 0.23 ms |
| **🥉 #3** | `MA_A3_MetaEpisodeTuner` | Cohort A | Cross-seed `episode_callback` tuning $\alpha \in [0.98, 1.10]$ | **883.565 pts** | 100.0% | 3.67 | 0.01340 mm | 0.22 ms |
| **#4** | `MA_B10_OptimalStaticHybrid` | Cohort B | Newton inversion ($\alpha=1.00$, $\gamma=0.018$) | **877.684 pts** | 100.0% | 3.63 | 0.01370 mm | 0.22 ms |
| **#5** | `MA_A5_EnergyAwareLimiter` | Cohort A | Current norm watchdog callback + Newton inversion | **849.111 pts** | 100.0% | 3.63 | 0.01540 mm | 0.32 ms |
| **#6** | `MA_A4_DualStageDecay` | Cohort A | Two-tier threshold gain + precision braking | **843.667 pts** | 100.0% | 3.83 | 0.01570 mm | 0.23 ms |
| **#7** | `MA_A2_MomentumBraking` | Cohort A | Step 1–2 acceleration boost + fine braking | **827.781 pts** | 100.0% | 3.80 | 0.01670 mm | 0.24 ms |
| **#8** | `MA_B6_AggressiveGain` | Cohort B | High gain ($\alpha=1.15$, $\gamma=0.015$) | **825.227 pts** | 100.0% | 3.80 | 0.01690 mm | 0.23 ms |
| **#9** | `MA_B9_UltraConservative` | Cohort B | Conservative gain ($\alpha=0.80$, $\gamma=0.010$) | **793.790 pts** | 100.0% | 4.37 | 0.01820 mm | 0.27 ms |
| **#10** | `MA_A1_AdaptiveDamp` | Cohort A | In-episode step damping below $0.028\text{ mm}$ | **604.046 pts** | 100.0% | 13.17 | 0.02340 mm | 0.85 ms |

*(Reference Baselines: Baseline 0 Classical SVD scores **635.277 pts**, Baseline 1 Supervised MLP scores **779.169 pts**, Track 3 Bayesian Optimization scores **878.382 pts**)*

---

## 🔬 In-Depth Analysis: Key Engineering Insights

### 1. The Physics of Newton Inversion on Total Current $\mathbf{I}_{\text{now}}$
In this harder 6-kick environment, the required corrector current reaches up to $2.84\text{ A}$, which lies deep inside the non-linear cubic saturation regime ($B(I) = I - 0.015 I^3$).
- **Per-Kick vs. Total Current:** Approximating the saturation kick-by-kick ($\Delta \mathbf{I} + 0.015 \Delta \mathbf{I}^3$) only achieves $\approx 767\text{ points}$ because the softening depends non-linearly on the cumulative state $\mathbf{I}$, not the delta step.
- **Tournament Winner (`MA_B7_CubicCompensator` — 923.703 pts):** By transforming into magnetic field space:
  $$\mathbf{B}_{\text{target}} = (\mathbf{I}_{\text{now}} - 0.015\,\mathbf{I}_{\text{now}}^3) - \alpha\,(\mathbf{R}^T)^\dagger \mathbf{Y}$$
  and solving $I - 0.015 I^3 = B_{\text{target}}$ via 5 Newton-Raphson iterations:
  $$I^{(m+1)} = I^{(m)} - \frac{I^{(m)} - 0.015 (I^{(m)})^3 - B_{\text{target}}}{1.0 - 0.045 (I^{(m)})^2}$$
  the agent takes 3 full-authority $0.8\text{ A}$ steps followed by an exact final landing step, converging in **3.67 steps** to **$0.01100\text{ mm}$ RMS** (virtually touching the physical sensor noise floor $\sigma = 0.010\text{ mm}$).

### 2. Deep Surrogate Optimization Boosts Baseline 1 (`MA_B8` & `MA_B10`)
- Standard Baseline 1 with a default $(128, 64, 32)$ MLP trained on 1500 samples scored **779.169 pts** (holdout RMSE $\approx 0.015\text{ mm}$).
- `MA_B8` and `MA_B10` increased dataset size to 2000–2500 samples and scaled the architecture to `(256, 128, 64)` with $L_2$ regularization $\alpha = 10^{-5}$.
- This dropped holdout prediction error near the sensor noise floor, allowing the L-BFGS-B optimizer in Baseline 1 to jump from **779.169 pts $\rightarrow$ 792.859 pts** (+13.7 points).

### 3. Cohort A Champion: Cross-Seed Meta Adaptation (`MA_A3` — 883.565 pts)
- Within Cohort A, `MA_A3_MetaEpisodeTuner` applied `episode_callback` to adapt feedback gain across seeds:
  - If a seed converged in $\le 3$ steps, it boosted gain by $+0.02$ (up to $1.10$).
  - If a seed took $\ge 5$ steps, it damped gain by $-0.02$ (down to $0.98$).
- This dynamic adjustment delivered **883.565 pts**, ranking #3 overall and surpassing the Bayesian Optimization reference baseline (878.382 pts).
- Conversely, `MA_A1_AdaptiveDamp` applied in-episode step braking whenever $\text{RMS} < 0.028\text{ mm}$, causing it to take timid micro-steps near the noise floor that inflated convergence from 3.7 steps to 13.17 steps (scoring 604.046 pts).

---

## 📈 Multi-Track Performance Summary Across All 10 Agents

| Agent Name | Baseline 0 (SVD) | Baseline 1 (MLP Inversion) | Track 2 (Custom Policy) | Track 3 (Bayesian Opt) | Best Track Score |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`MA_B7_CubicCompensator`** | 635.277 | 783.093 | **923.703** | 878.382 | **923.703** |
| **`MA_B8_DeepTwinInversion`** | 635.277 | 792.859 | **911.727** | 878.382 | **911.727** |
| **`MA_A3_MetaEpisodeTuner`** | 635.277 | 779.169 | **883.565** | 878.382 | **883.565** |
| **`MA_B10_OptimalStaticHybrid`** | 635.277 | 792.859 | 877.684 | **878.382** | **878.382** |
| **`MA_A5_EnergyAwareLimiter`** | 635.277 | 779.169 | 849.111 | **878.382** | **878.382** |
| **`MA_A4_DualStageDecay`** | 635.277 | 779.169 | 843.667 | **878.382** | **878.382** |
| **`MA_A2_MomentumBraking`** | 635.277 | 779.169 | 827.781 | **878.382** | **878.382** |
| **`MA_B6_AggressiveGain`** | 635.277 | 779.169 | 825.227 | **878.382** | **878.382** |
| **`MA_B9_UltraConservative`** | 635.277 | 779.169 | 793.790 | **878.382** | **878.382** |
| **`MA_A1_AdaptiveDamp`** | 635.277 | 779.169 | 604.046 | **878.382** | **878.382** |

---

## 📡 Live Weights & Biases Telemetry Verification

- **W&B Project:** [`ai4acc-mini-hackathon-2026/ai4acc-mini-hackathon-2026`](https://wandb.ai/ai4acc-mini-hackathon-2026/ai4acc-mini-hackathon-2026)
- **Runs Submitted:** 40 runs (4 tracks $\times$ 10 agents, all in state `finished`).
- **Telemetry Integrity:** Verified via `wandb.Api()` against local simulation logs.
- **Raw Telemetry Archive:** Fully captured in [`docs/experiments/multi_agent_benchmark_results3.json`](experiments/multi_agent_benchmark_results3.json).

---

## 💡 Key Advice for Hackathon Attendees

1. **Compensate Saturation on Total Current $\mathbf{I}_{\text{now}}$, Not on Delta Steps:**
   - Always read `info["currents"]` and invert the non-linearity in field space using Newton-Raphson. This single enhancement unlocks scores $>910\text{ pts}$.
2. **Use Feedback Gain $\alpha \approx 1.00$:**
   - Under the $0.8\text{ A}$ per-step limit, a gain of $1.00$ achieves the minimum theoretical step count (3.63–3.67 steps) across the 30 evaluation seeds.
3. **If Using Callbacks, Prefer `episode_callback` Over In-Episode Braking:**
   - Sensor noise ($\sigma = 0.010\text{ mm}$) distorts observations near the $0.030\text{ mm}$ threshold. Braking inside the episode often stalls convergence; adapting across episodes (`episode_callback`) preserves decisive control authority.

---

## 🧹 Cleanup Verification

All 10 test worktree directories (`worktrees/agent-1` through `worktrees/agent-10`) and temporary git branches (`agent-tournament3-1` through `agent-tournament3-10`) were verified destroyed post-run. Only `main` remains active in the repository.
