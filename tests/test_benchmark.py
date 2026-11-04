"""
tests/test_benchmark.py
Unit tests for evaluate_hackathon_benchmark and callback hooks.
Validates standardized evaluation protocol, score calculation, and telemetry.
"""

import numpy as np
import pytest
from src.environment import AcceleratorOrbitGymEnv
from src.benchmark import evaluate_hackathon_benchmark, print_benchmark_leaderboard
from src.controllers import ClassicalSVDController


class TestBenchmarkHarness:
    def test_evaluate_benchmark_basic(self):
        """Test benchmark evaluation across a subset of seeds."""
        env = AcceleratorOrbitGymEnv()
        agent = ClassicalSVDController(env.R, gain=0.45)

        res = evaluate_hackathon_benchmark(
            env,
            agent,
            agent_name="TestAgent",
            seeds=range(1, 4),
            use_wandb=False
        )

        assert "score" in res
        assert "success_rate" in res
        assert "mean_steps" in res
        assert "mean_rms" in res
        assert "mean_norm" in res
        assert "mean_latency" in res

        assert res["success_rate"] == 100.0
        assert res["score"] > 950.0
        assert res["mean_steps"] < 20.0
        assert res["mean_rms"] < 0.030

    def test_step_and_episode_callbacks(self):
        """Test step_callback and episode_callback hooks receive expected telemetry."""
        env = AcceleratorOrbitGymEnv()
        agent = ClassicalSVDController(env.R, gain=0.45)

        step_records = []
        episode_records = []

        def on_step(data, ag):
            step_records.append(data)
            assert "seed" in data
            assert "step" in data
            assert "obs" in data
            assert "action" in data
            assert "info" in data

        def on_episode(data, ag):
            episode_records.append(data)
            assert "seed" in data
            assert "steps" in data
            assert "initial_rms" in data
            assert "final_rms" in data
            assert "is_success" in data

        res = evaluate_hackathon_benchmark(
            env,
            agent,
            seeds=range(1, 3),
            use_wandb=False,
            step_callback=on_step,
            episode_callback=on_episode
        )

        assert len(episode_records) == 2
        assert len(step_records) > 0
        assert len(step_records) == sum(ep["steps"] for ep in episode_records)

    def test_print_benchmark_leaderboard(self, capsys):
        """Test leaderboard table formatting output."""
        sample_metrics = {
            "success_rate": 100.0,
            "mean_steps": 3.5,
            "mean_rms": 0.0210,
            "score": 1020.0
        }
        leaderboard = [("TestController", sample_metrics)]
        print_benchmark_leaderboard(leaderboard)

        captured = capsys.readouterr()
        assert "OFFICIAL HACKATHON BENCHMARK LEADERBOARD" in captured.out
        assert "TestController" in captured.out
        assert "1020.0" in captured.out
