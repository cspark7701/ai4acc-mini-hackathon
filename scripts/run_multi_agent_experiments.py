"""
Multi-Agent Parallel Experiment Runner
Executes 10 test participant agents across 10 Git worktrees.
- Cohort A (Agents 1-5): Use custom callback functions to dynamically improve all Tracks.
- Cohort B (Agents 6-10): Do not use callbacks, but tune architecture, gain, analytical kicks, and damping.
Outputs structured JSON results for each agent.
"""

import sys
import os
import json
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np

# Python path configuration for isolated execution
PYTHON_EXEC = "/home/cspark/Work/simulation_codes-working/miniforge3/envs/rl4aa26-challenge/bin/python"


def run_agent_simulation(agent_config):
    worktree_path = agent_config["worktree_path"]
    agent_id = agent_config["agent_id"]
    agent_name = agent_config["agent_name"]
    cohort = agent_config["cohort"]
    strategy = agent_config["strategy"]

    # Ensure python imports from worktree
    sys.path.insert(0, worktree_path)
    from src.environment import AcceleratorOrbitGymEnv
    from src.benchmark import evaluate_hackathon_benchmark
    from src.controllers import ClassicalSVDController, BayesianOptimizationController
    from sklearn.neural_network import MLPRegressor
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import Matern, WhiteKernel
    import scipy.optimize as opt

    env = AcceleratorOrbitGymEnv()

    # Common offline data generation for surrogate models
    np.random.seed(42 + agent_id)
    n_samples = agent_config.get("n_samples", 1500)
    X_train = np.random.uniform(-3.0, 3.0, size=(n_samples, 6))
    noise = np.random.normal(0.0, env.noise_std, size=(n_samples, 12))
    Y_train = (X_train @ env.R) - 0.015 * ((X_train**3) @ env.R) + noise

    # Surrogate training configuration
    mlp_layers = agent_config.get("mlp_layers", (128, 64, 32))
    mlp_alpha = agent_config.get("mlp_alpha", 1e-4)
    surrogate = MLPRegressor(
        hidden_layer_sizes=mlp_layers,
        activation="relu",
        alpha=mlp_alpha,
        max_iter=300,
        random_state=42 + agent_id
    )
    surrogate.fit(X_train, Y_train)

    # GP Surrogate for Track 3
    gp_kernel = Matern(length_scale=1.5, nu=2.5) + WhiteKernel(
        noise_level=env.noise_std**2, noise_level_bounds="fixed"
    )
    gp_surrogate = GaussianProcessRegressor(kernel=gp_kernel, alpha=0.0, normalize_y=True, random_state=42 + agent_id)
    gp_surrogate.fit(X_train[:250], Y_train[:250])

    # Base MLP Controller
    class SupervisedAgent:
        def __init__(self, model, l2_reg=1e-4):
            self.model = model
            self.l2_reg = l2_reg

        def act(self, obs, info=None):
            def obj(dI):
                pred = self.model.predict(dI.reshape(1, -1))[0]
                return float(np.sum((obs + pred)**2) + self.l2_reg * np.sum(dI**2))
            res = opt.minimize(obj, np.zeros(6), method="L-BFGS-B", bounds=[(-0.8, 0.8)]*6)
            return np.clip(res.x, -0.8, 0.8)

    # Track 2 RL / Adaptive Agent
    gain = agent_config.get("gain", 0.45)
    gamma = agent_config.get("gamma", 0.03)
    use_cubic_comp = agent_config.get("use_cubic_comp", False)

    class CustomRLAgent:
        def __init__(self, R_matrix, base_gain=0.45, base_gamma=0.03, cubic=False):
            self.R_pinv = np.linalg.pinv(R_matrix.T)
            self.gain = base_gain
            self.gamma = base_gamma
            self.cubic = cubic
            self.step_history = []

        def act(self, obs, info=None):
            step = info.get("step", 0) if info else 0
            dI = - self.gain * (self.R_pinv @ obs)
            if self.cubic:
                # Analytical cubic desaturation compensation
                dI = dI + 0.015 * (dI**3)
            damping = 1.0 / (1.0 + self.gamma * step)
            action = np.clip(dI * damping, -0.8, 0.8)
            return action

    b0 = ClassicalSVDController(env.R, gain=0.45)
    b1 = SupervisedAgent(surrogate, l2_reg=agent_config.get("l2_reg", 1e-4))
    b2 = CustomRLAgent(env.R, base_gain=gain, base_gamma=gamma, cubic=use_cubic_comp)
    b3 = BayesianOptimizationController(gp_surrogate, kappa=0.0, l2_reg=1e-4)

    # -------------------------------------------------------------
    # Callbacks Configuration
    # -------------------------------------------------------------
    step_cb = None
    ep_cb = None

    if cohort == "Cohort_A_Callback":
        # Custom callback strategies for Cohort A
        if agent_id == 1:
            # Agent 1: Adaptive Threshold Gain Decay Callback
            def step_cb(step_data, ag):
                rms = step_data["info"]["rms"]
                if rms < 0.040:
                    ag.gain *= 0.94  # Smooth terminal deceleration near 0.03 mm
        elif agent_id == 2:
            # Agent 2: Momentum Acceleration Callback
            def step_cb(step_data, ag):
                rms = step_data["info"]["rms"]
                # If convergence is stalled, boost gain; if rapid, brake
                if rms > 0.10:
                    ag.gain = min(ag.gain * 1.05, 0.72)
                elif rms < 0.038:
                    ag.gain *= 0.90
        elif agent_id == 3:
            # Agent 3: Episode-level Meta-Learning Gain Tuning Callback
            history = []
            def ep_cb(ep_data, ag):
                history.append(ep_data["steps"])
                if ep_data["steps"] > 6:
                    ag.gain = min(ag.gain + 0.02, 0.70)
                elif not ep_data["is_success"]:
                    ag.gamma += 0.005
        elif agent_id == 4:
            # Agent 4: Dual Threshold Multi-Stage Damping Callback
            def step_cb(step_data, ag):
                rms = step_data["info"]["rms"]
                if rms < 0.032:
                    ag.gain *= 0.85
                elif rms < 0.050:
                    ag.gain *= 0.95
        elif agent_id == 5:
            # Agent 5: Current-Energy Penalty Aware Callback
            def step_cb(step_data, ag):
                c_norm = np.linalg.norm(step_data["info"]["currents"])
                if c_norm > 2.0:
                    ag.gain *= 0.92  # Penalize heavy currents to optimize score
                elif step_data["info"]["rms"] < 0.035:
                    ag.gain *= 0.93

    # Benchmark Evaluation across official 30 seeds
    seeds = range(1, 31)

    res_b0 = evaluate_hackathon_benchmark(env, b0, agent_name="B0_SVD", team_name=agent_name, seeds=seeds, use_wandb=False)
    res_b1 = evaluate_hackathon_benchmark(env, b1, agent_name="B1_MLP", team_name=agent_name, seeds=seeds, use_wandb=False)
    res_b2 = evaluate_hackathon_benchmark(env, b2, agent_name="Track2_Custom", team_name=agent_name, seeds=seeds, use_wandb=False,
                                          step_callback=step_cb, episode_callback=ep_cb)
    res_b3 = evaluate_hackathon_benchmark(env, b3, agent_name="Track3_BO", team_name=agent_name, seeds=seeds, use_wandb=False)

    all_tracks = {
        "Baseline 0 (Linear SVD)": res_b0,
        "Baseline 1 (Supervised MLP)": res_b1,
        "Track 2 (RL/Adaptive Agent)": res_b2,
        "Track 3 (Bayesian Optimization)": res_b3,
    }

    # Best track by score
    best_track_name = max(all_tracks.keys(), key=lambda k: all_tracks[k]["score"])
    best_track_metrics = all_tracks[best_track_name]

    return {
        "agent_id": agent_id,
        "agent_name": agent_name,
        "cohort": cohort,
        "strategy": strategy,
        "best_track": best_track_name,
        "best_score": best_track_metrics["score"],
        "best_success_rate": best_track_metrics["success_rate"],
        "best_mean_steps": best_track_metrics["mean_steps"],
        "best_mean_rms": best_track_metrics["mean_rms"],
        "best_mean_norm": best_track_metrics["mean_norm"],
        "track2_score": res_b2["score"],
        "track2_steps": res_b2["mean_steps"],
        "track2_rms": res_b2["mean_rms"],
        "all_tracks": all_tracks,
    }


def main():
    agent_configs = [
        # --- Cohort A: 5 Callback-Driven Agents ---
        {
            "agent_id": 1,
            "agent_name": "Agent_A1_AdaptiveDamp",
            "cohort": "Cohort_A_Callback",
            "strategy": "Step callback: Terminal gain decay when RMS < 0.040 mm to stop limit-cycle overshoot",
            "gain": 0.58, "gamma": 0.025, "use_cubic_comp": True,
            "worktree_path": "/home/cspark/Work/projects/ai4acc-mini-hackathon/worktrees/agent-1"
        },
        {
            "agent_id": 2,
            "agent_name": "Agent_A2_MomentumBraking",
            "cohort": "Cohort_A_Callback",
            "strategy": "Step callback: High-speed distant kick (boost gain) + hard braking near boundary",
            "gain": 0.65, "gamma": 0.020, "use_cubic_comp": True,
            "worktree_path": "/home/cspark/Work/projects/ai4acc-mini-hackathon/worktrees/agent-2"
        },
        {
            "agent_id": 3,
            "agent_name": "Agent_A3_MetaEpisodeTuner",
            "cohort": "Cohort_A_Callback",
            "strategy": "Episode callback: Cross-seed dynamic meta-tuning of gain and damping based on prior seed latency",
            "gain": 0.52, "gamma": 0.030, "use_cubic_comp": False,
            "worktree_path": "/home/cspark/Work/projects/ai4acc-mini-hackathon/worktrees/agent-3"
        },
        {
            "agent_id": 4,
            "agent_name": "Agent_A4_DualStageDecay",
            "cohort": "Cohort_A_Callback",
            "strategy": "Step callback: Dual-stage precision braking (fine control < 0.050 mm and sub-0.032 mm)",
            "gain": 0.62, "gamma": 0.022, "use_cubic_comp": True,
            "worktree_path": "/home/cspark/Work/projects/ai4acc-mini-hackathon/worktrees/agent-4"
        },
        {
            "agent_id": 5,
            "agent_name": "Agent_A5_EnergyAwareLimiter",
            "cohort": "Cohort_A_Callback",
            "strategy": "Step callback: Energy-aware current limiting callback suppressing opposing kick oscillations",
            "gain": 0.55, "gamma": 0.028, "use_cubic_comp": True,
            "worktree_path": "/home/cspark/Work/projects/ai4acc-mini-hackathon/worktrees/agent-5"
        },

        # --- Cohort B: 5 Non-Callback Parameter & Architectural Agents ---
        {
            "agent_id": 6,
            "agent_name": "Agent_B6_AggressiveGain",
            "cohort": "Cohort_B_NoCallback",
            "strategy": "No callback: Fixed aggressive feedback gain (alpha=0.68) with strong damping (gamma=0.038)",
            "gain": 0.68, "gamma": 0.038, "use_cubic_comp": False,
            "worktree_path": "/home/cspark/Work/projects/ai4acc-mini-hackathon/worktrees/agent-6"
        },
        {
            "agent_id": 7,
            "agent_name": "Agent_B7_CubicCompensator",
            "cohort": "Cohort_B_NoCallback",
            "strategy": "No callback: Analytical cubic inverse series desaturation kick (dI + 0.015*dI^3) with moderate gain (0.54)",
            "gain": 0.54, "gamma": 0.026, "use_cubic_comp": True,
            "worktree_path": "/home/cspark/Work/projects/ai4acc-mini-hackathon/worktrees/agent-7"
        },
        {
            "agent_id": 8,
            "agent_name": "Agent_B8_DeepTwinInversion",
            "cohort": "Cohort_B_NoCallback",
            "strategy": "No callback: Deep MLP digital twin (256-128-64) with dense sampling (3000 pts) and low L2 regularizer",
            "n_samples": 3000, "mlp_layers": (256, 128, 64), "l2_reg": 1e-5, "gain": 0.48, "gamma": 0.030,
            "worktree_path": "/home/cspark/Work/projects/ai4acc-mini-hackathon/worktrees/agent-8"
        },
        {
            "agent_id": 9,
            "agent_name": "Agent_B9_UltraConservative",
            "cohort": "Cohort_B_NoCallback",
            "strategy": "No callback: Low gain (0.42) with minimal damping for maximum current norm efficiency",
            "gain": 0.42, "gamma": 0.015, "use_cubic_comp": False,
            "worktree_path": "/home/cspark/Work/projects/ai4acc-mini-hackathon/worktrees/agent-9"
        },
        {
            "agent_id": 10,
            "agent_name": "Agent_B10_OptimalStaticHybrid",
            "cohort": "Cohort_B_NoCallback",
            "strategy": "No callback: Analytical cubic kick + tuned static gain (0.60) + tuned static damping (0.030)",
            "gain": 0.60, "gamma": 0.030, "use_cubic_comp": True,
            "worktree_path": "/home/cspark/Work/projects/ai4acc-mini-hackathon/worktrees/agent-10"
        },
    ]

    print("====================================================================")
    print("   AI4ACC 10-Agent Autonomous Benchmark Tournament Launch")
    print("====================================================================")
    print("Cohort A: 5 Callback-Driven Agents (Adaptive online feedback)")
    print("Cohort B: 5 Architectural/Parameter Agents (Offline tuning)")
    print("Evaluation: Strictly 30 Standardized Seeds (range 1 to 31)")
    print("--------------------------------------------------------------------")

    results = []
    # Execute in parallel with ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(run_agent_simulation, cfg): cfg["agent_name"] for cfg in agent_configs}
        for future in as_completed(futures):
            name = futures[future]
            try:
                res = future.result()
                results.append(res)
                print(f"[FINISHED] {res['agent_name']} ({res['cohort']}) -> Best Score: {res['best_score']:.1f} pts ({res['best_track']}), Track 2 Score: {res['track2_score']:.1f} pts")
            except Exception as e:
                print(f"[ERROR] Agent {name} encountered an error: {e}")

    # Sort results by score descending
    results.sort(key=lambda x: x["best_score"], reverse=True)

    # Save to JSON
    os.makedirs("docs/experiments", exist_ok=True)
    out_path = "docs/experiments/multi_agent_benchmark_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\n====================================================================")
    print(f"Results successfully saved to: {out_path}")
    print("====================================================================")

    # Print summary leaderboard
    print(f"\n{'Rank':<5} | {'Agent Name':<28} | {'Cohort':<20} | {'Best Score':<10} | {'Track 2 Score':<14} | {'Best Track':<25}")
    print("-" * 115)
    for rank, r in enumerate(results, 1):
        print(f"#{rank:<4} | {r['agent_name']:<28} | {r['cohort']:<20} | {r['best_score']:>8.1f}  | {r['track2_score']:>12.1f}  | {r['best_track']:<25}")
    print("=" * 115)


if __name__ == "__main__":
    main()
