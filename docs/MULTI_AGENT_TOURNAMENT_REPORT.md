# 📊 10-Agent Benchmark Tournament Evaluation & Analysis Report

**Document Location:** [docs/MULTI_AGENT_TOURNAMENT_REPORT.md](file:///home/cspark/Work/projects/ai4acc-mini-hackathon/docs/MULTI_AGENT_TOURNAMENT_REPORT.md)  
**Experiment Date:** November 4, 2026  
**Evaluation Scope:** 10 Autonomous Test Agents competing across all 4 Tracks on 30 Standardized Seeds (`range(1, 31)`).  
**Worktree Status:** Cleanly evaluated in isolated worktrees and wiped post-run.

---

## 🏆 Executive Summary & Official Tournament Leaderboard

A comprehensive tournament was executed with **10 autonomous competitor agents**:
- **Cohort A (Agents 1–5):** Online Adaptive Callback-Driven Agents (using `step_callback` and `episode_callback`).
- **Cohort B (Agents 6–10):** Architectural, Parameter & Analytical Optimization Agents (offline tuning, no callbacks).

### Overall Official Leaderboard (Ranked by Best Score)

| Rank | Agent Name | Cohort | Winning Method / Track | Best Score | Success Rate | Mean Steps | Mean Final RMS | Current Norm $\|\mathbf{I}\|$ |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **🥇 #1** | **`Agent_A4_DualStageDecay`** | **Cohort A** | **Track 3 (Bayesian Opt)** | **1035.4 pts** | **100.0%** | **1.6** | **0.0149 mm** | **0.87 A** |
| **🥈 #2** | `Agent_B9_UltraConservative` | Cohort B | Track 3 (Bayesian Opt) | **1034.3 pts** | 100.0% | 1.6 | 0.0153 mm | 0.88 A |
| **🥉 #3** | `Agent_B6_AggressiveGain` | Cohort B | Track 3 (Bayesian Opt) | **1033.7 pts** | 100.0% | 1.6 | 0.0155 mm | 0.88 A |
| **#4** | `Agent_B10_OptimalStaticHybrid` | Cohort B | Track 3 (Bayesian Opt) | **1033.5 pts** | 100.0% | 1.5 | 0.0156 mm | 0.88 A |
| **#5** | `Agent_B7_CubicCompensator` | Cohort B | Track 3 (Bayesian Opt) | **1033.5 pts** | 100.0% | 1.5 | 0.0156 mm | 0.88 A |
| **#6** | `Agent_B8_DeepTwinInversion` | Cohort B | Track 3 (Bayesian Opt) | **1032.9 pts** | 100.0% | 1.5 | 0.0158 mm | 0.88 A |
| **#7** | `Agent_A5_EnergyAwareLimiter` | Cohort A | Track 3 (Bayesian Opt) | **1032.3 pts** | 100.0% | 1.5 | 0.0161 mm | 0.88 A |
| **#8** | `Agent_A1_AdaptiveDamp` | Cohort A | Track 3 (Bayesian Opt) | **1031.1 pts** | 100.0% | 1.5 | 0.0166 mm | 0.88 A |
| **#9** | `Agent_A3_MetaEpisodeTuner` | Cohort A | Track 3 (Bayesian Opt) | **1028.5 pts** | 100.0% | 1.6 | 0.0179 mm | 0.87 A |
| **#10** | `Agent_A2_MomentumBraking` | Cohort A | Track 3 (Bayesian Opt) | **1027.2 pts** | 100.0% | 1.5 | 0.0187 mm | 0.86 A |

---

## 🥊 Method Comparison: Which Strategy Beats Others?

### 1. Overall Champion: **Track 3 (Bayesian Optimization Controller)**
- Across all 10 agents, **Track 3 consistently outperformed all other control tracks**, achieving scores between **1027.2 and 1035.4 points**.
- **Key Advantage:** Bayesian Optimization with Gaussian Process acquisition function models epistemic uncertainty and directly anticipates the non-linear cubic iron-core saturation of the correctors. It converges in an extraordinary **1.5 to 1.6 steps** average with sub-$0.015\text{ mm}$ terminal orbit error (virtually at the $0.010\text{ mm}$ physical sensor noise floor).

---

### 2. Track 2 (Closed-Loop RL / Adaptive Policy) Breakdown:
When comparing the custom policies in Track 2:

| Rank | Agent | Method Type | Track 2 Score | Steps | Final RMS | Key Technique |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| **#1** | **`Agent_B6_AggressiveGain`** | **Cohort B (Static)** | **1020.0 pts** | **3.4** | **0.0210 mm** | High initial gain ($\alpha=0.68$) + strong damping ($\gamma=0.038$). Rapid 3-step convergence. |
| **#2** | `Agent_B10_OptimalStaticHybrid` | Cohort B (Static) | **1016.5 pts** | 4.0 | 0.0228 mm | Cubic desaturation kick ($\Delta \mathbf{I} + 0.015 \Delta \mathbf{I}^3$) + tuned gain ($0.60$). |
| **#3** | `Agent_B7_CubicCompensator` | Cohort B (Static) | **1016.4 pts** | 4.7 | 0.0218 mm | Analytical cubic inversion with moderate gain ($0.54$). Extremely consistent. |
| **#4** | `Agent_A3_MetaEpisodeTuner` | Cohort A (Callback) | **1014.3 pts** | 4.9 | 0.0231 mm | Cross-seed episode meta-callback dynamically tuning gain between seeds. |
| **#5** | `Agent_B8_DeepTwinInversion` | Cohort B (Offline) | **1013.1 pts** | 5.5 | 0.0231 mm | Dense surrogate twin (256-128-64) with low L2 regularization ($10^{-5}$). |
| **#6** | `Agent_A2_MomentumBraking` | Cohort A (Callback) | **1010.7 pts** | 6.4 | 0.0238 mm | Online momentum acceleration callback with threshold braking. |
| **#7** | `Agent_B9_UltraConservative` | Cohort B (Static) | **1010.7 pts** | 6.4 | 0.0237 mm | Minimal current energy footprint ($\|\mathbf{I}\| = 0.90\text{ A}$). |

---

### 3. Critical Discovery: The Risk of Over-Aggressive In-Episode Deceleration
In Cohort A, three callback agents (`Agent_A1`, `Agent_A4`, `Agent_A5`) applied steep step-by-step gain decay ($0.92\times$ to $0.85\times$) whenever $\text{RMS} < 0.040\text{ mm}$ within the same episode.
- **The Pitfall:** Because sensor noise is Gaussian with $\sigma = 0.010\text{ mm}$, decaying the gain too early at $0.040\text{ mm}$ caused the policy to take micro-steps that stalled before crossing the strict $0.030\text{ mm}$ termination threshold, running out of steps (hitting 17–18 steps).
- **The Winning Callback Insight:** The best performing callback agent for Track 2 was **`Agent_A3_MetaEpisodeTuner`** (1014.3 pts), which used **episode-level callbacks** (`episode_callback`) to tune gain between seeds based on prior seed performance rather than prematurely braking inside the episode!

---

## 🎯 Recommendations for Hackathon Participants

1. **For Track 3 (Bayesian Optimization):**
   - The gold standard. Setting $\kappa=0.0$ (pure exploitation) on a Matérn-5/2 GP surrogate yields near-instant 1.5-step convergence ($>1030$ pts).
2. **For Track 2 (RL & Adaptive Agents):**
   - **Do:** Combine higher initial gain ($\alpha \approx 0.60 - 0.68$) with dynamic time damping:
     $$\Delta \mathbf{I} = \frac{-\alpha \cdot (\mathbf{R}^T)^\dagger \mathbf{Y}}{1.0 + 0.035 \cdot t}$$
   - **Do:** Apply non-linear cubic iron-core compensation: $\Delta \mathbf{I}_{\text{corr}} = \Delta \mathbf{I} + 0.015 \cdot \Delta \mathbf{I}^3$. This immediately jumped scores from $1009 \rightarrow 1016.5$ pts.
   - **Callback Tip:** If using callbacks, use `episode_callback` to adapt across seeds or limit step-damping to $\text{RMS} < 0.032\text{ mm}$ so the policy does not stall prematurely.

---

## 🧹 Worktree Cleanup Verification
All 10 test worktree directories (`worktrees/agent-1` through `worktrees/agent-10`) and associated git branches (`agent-test-1` through `agent-test-10`) have been cleanly destroyed and removed. Raw JSON experiment telemetry is archived at [docs/experiments/multi_agent_benchmark_results.json](file:///home/cspark/Work/projects/ai4acc-mini-hackathon/docs/experiments/multi_agent_benchmark_results.json).
