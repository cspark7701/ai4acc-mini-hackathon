"""
src/benchmark.py
Standardized Evaluation Harness with Weights & Biases Logging.
"""
import time
from typing import Sequence, Optional, Dict, Any, Callable
import numpy as np

try:
    import wandb
    WANDB_AVAILABLE = True
except ImportError:
    WANDB_AVAILABLE = False


def evaluate_hackathon_benchmark(
    env_or_agent: Any,
    agent: Optional[Any] = None,
    agent_name: str = "Agent",
    team_name: str = "Team_Alpha",
    seeds: Sequence[int] = range(1, 31),
    use_wandb: bool = True,
    project: str = "accelerator-orbit-hackathon",
    entity: Optional[str] = None,
    step_callback: Optional[Callable[[Dict[str, Any], Any], None]] = None,
    episode_callback: Optional[Callable[[Dict[str, Any], Any], None]] = None,
) -> Dict[str, Any]:
    """
    Standardized benchmark evaluation across specified random seeds.
    Accepts either evaluate_hackathon_benchmark(env, agent, ...) or evaluate_hackathon_benchmark(agent, ...).

    Parameters:
        env_or_agent: Either AcceleratorOrbitGymEnv instance or the competitor agent.
        agent: Competitor agent (if env is provided as first arg).
        agent_name: Display name of the agent.
        team_name: Participant or team identifier.
        seeds: Evaluation seed sequence (strictly range(1, 31)).
        use_wandb: Enable cloud logging to Weights & Biases.
        project: W&B project namespace.
        entity: W&B team/user entity.
        step_callback: Optional callable invoked after each env.step():
            step_callback(step_data: dict, agent: Any) -> None
            step_data contains: {seed, step, obs, action, reward, next_obs, info}
        episode_callback: Optional callable invoked at the end of each seed episode:
            episode_callback(episode_data: dict, agent: Any) -> None
            episode_data contains: {seed, steps, initial_rms, final_rms, is_success, current_norm, elapsed_ms, info}
    """
    if agent is None:
        agent = env_or_agent
        from src.environment import AcceleratorOrbitGymEnv
        env = AcceleratorOrbitGymEnv()
    else:
        env = env_or_agent

    n_seeds = len(seeds)
    successes = 0
    total_steps = 0
    final_rms_list = []
    current_norms = []
    latencies = []
    table_rows = []

    for seed in seeds:
        obs, info = env.reset(seed=seed)
        initial_rms = info["initial_rms"]
        terminated = False
        truncated = False
        step = 0
        t0 = time.time()

        while not (terminated or truncated):
            action = agent.act(obs, info)
            next_obs, reward, terminated, truncated, next_info = env.step(action)
            step += 1

            if step_callback is not None:
                step_callback({
                    "seed": seed,
                    "step": step,
                    "obs": obs,
                    "action": action,
                    "reward": reward,
                    "next_obs": next_obs,
                    "terminated": terminated,
                    "truncated": truncated,
                    "info": next_info,
                }, agent)

            obs = next_obs
            info = next_info

        elapsed_ms = (time.time() - t0) * 1000.0
        latencies.append(elapsed_ms)

        is_succ = info.get("is_success", False)
        if is_succ:
            successes += 1
        total_steps += step
        final_rms_list.append(info["rms"])
        norm_I = float(np.linalg.norm(info["currents"]))
        current_norms.append(norm_I)

        if episode_callback is not None:
            episode_callback({
                "seed": seed,
                "steps": step,
                "initial_rms": initial_rms,
                "final_rms": info["rms"],
                "is_success": is_succ,
                "current_norm": norm_I,
                "elapsed_ms": elapsed_ms,
                "info": info,
            }, agent)

        table_rows.append([seed, initial_rms, info["rms"], step, is_succ, norm_I, elapsed_ms])

    success_rate = (successes / n_seeds) * 100.0
    mean_steps = total_steps / n_seeds
    mean_rms = float(np.mean(final_rms_list))
    mean_norm = float(np.mean(current_norms))
    mean_latency = float(np.mean(latencies))

    # Official Orbit Alignment Hackathon Scoring Formula
    score = success_rate * 10.0 - 2.0 * mean_steps + (0.03 / max(mean_rms, 0.005)) * 20.0 - 2.0 * mean_norm

    if use_wandb and WANDB_AVAILABLE:
        try:
            run_name = f"{team_name}_{agent_name}"
            run = wandb.init(
                project=project,
                entity=entity,
                name=run_name,
                tags=["orbit-hackathon", agent_name, team_name],
                config={
                    "team": team_name,
                    "agent": agent_name,
                    "n_seeds": n_seeds,
                    "target_rms_mm": env.target_rms,
                    "max_steps": env.max_steps,
                    "noise_std_mm": env.noise_std
                },
                reinit="finish_previous"
            )
            run.summary["challenge_score"] = float(round(score, 1))
            run.summary["success_rate_pct"] = float(round(success_rate, 1))
            run.summary["mean_steps"] = float(round(mean_steps, 2))
            run.summary["mean_final_rms_mm"] = float(round(mean_rms, 4))
            run.summary["mean_current_norm_A"] = float(round(mean_norm, 2))
            run.summary["mean_latency_ms"] = float(round(mean_latency, 2))

            wandb_cols = ["Seed", "Initial_RMS_mm", "Final_RMS_mm", "Steps", "Success", "Current_Norm_A", "Latency_ms"]
            wandb_table = wandb.Table(columns=wandb_cols, data=table_rows)
            wandb.log({"seed_breakdown_table": wandb_table})

            print(f"[W&B] Logged '{run_name}' to {run.url} (Score: {score:.1f} pts)")
            run.finish()
        except Exception as e:
            print(f"[W&B Warning] Logging skipped: {e}")

    return {
        "success_rate": success_rate,
        "mean_steps": mean_steps,
        "mean_rms": mean_rms,
        "mean_norm": mean_norm,
        "mean_latency": mean_latency,
        "score": score
    }


def print_benchmark_leaderboard(leaderboard: Sequence[Any]) -> None:
    """
    Format and display official hackathon benchmark leaderboard table.

    Parameters:
        leaderboard: List of (name, metrics_dict) tuples.
    """
    sorted_board = sorted(leaderboard, key=lambda x: x[1].get("score", 0.0), reverse=True)
    print("=" * 85)
    print("                        OFFICIAL HACKATHON BENCHMARK LEADERBOARD")
    print("=" * 85)
    print(f"{'Rank':<5} | {'Agent / Controller Name':<28} | {'Success':<8} | {'Steps':<6} | {'Final RMS':<10} | {'Score':<8}")
    print("-" * 85)
    for rank, (name, metrics) in enumerate(sorted_board, 1):
        print(f"#{rank:<4} | {name:<28} | {metrics['success_rate']:>6.1f}% | {metrics['mean_steps']:>5.1f} | {metrics['mean_rms']:>8.4f}mm | {metrics['score']:>7.1f}")
    print("=" * 85)
