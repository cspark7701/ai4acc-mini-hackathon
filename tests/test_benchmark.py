"""
tests/test_benchmark.py
Unit tests for evaluate_hackathon_benchmark and callback hooks.
Validates standardized evaluation protocol, score calculation, and telemetry.
"""


import pytest
from src.environment import AcceleratorOrbitGymEnv
from src.benchmark import evaluate_hackathon_benchmark, print_benchmark_leaderboard, score_seed
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
        assert 0.0 <= res["score"] <= 1000.0
        assert res["score"] > 600.0
        assert res["score"] == pytest.approx(res["score_success"] + res["score_speed"] + res["score_precision"])
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

        evaluate_hackathon_benchmark(
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
            "score": 705.3
        }
        leaderboard = [("TestController", sample_metrics)]
        print_benchmark_leaderboard(leaderboard)

        captured = capsys.readouterr()
        assert "OFFICIAL HACKATHON BENCHMARK LEADERBOARD" in captured.out
        assert "TestController" in captured.out
        assert "705.300" in captured.out


class TestSeedScore:
    def test_failed_episode_scores_zero(self):
        pts = score_seed(False, 20, 0.05)
        assert pts["total"] == 0.0

    def test_perfect_episode_scores_1000(self):
        pts = score_seed(True, 1, 0.010)
        assert pts["total"] == pytest.approx(1000.0)

    def test_slowest_success_at_target_scores_400(self):
        pts = score_seed(True, 20, 0.0299)
        assert pts["speed"] == pytest.approx(0.0)
        assert pts["precision"] == pytest.approx(0.0, abs=1.0)
        assert pts["total"] == pytest.approx(400.0, abs=1.0)

    def test_precision_is_log_scaled_and_capped(self):
        mid = score_seed(True, 20, 0.03 / 3 ** 0.5)
        assert mid["precision"] == pytest.approx(150.0)
        below_floor = score_seed(True, 20, 0.005)
        assert below_floor["precision"] == pytest.approx(300.0)

    def test_fewer_steps_score_higher(self):
        assert score_seed(True, 2, 0.02)["total"] > score_seed(True, 8, 0.02)["total"]

    def test_speed_scale_fixed_at_20_steps(self):
        slow = score_seed(True, 35, 0.02)
        assert slow["speed"] == pytest.approx(0.0)
        assert slow["total"] == pytest.approx(400.0 + slow["precision"])
        assert score_seed(True, 20, 0.02)["speed"] == pytest.approx(0.0)
        assert score_seed(True, 10, 0.02)["speed"] == pytest.approx(300.0 * 10 / 19)
