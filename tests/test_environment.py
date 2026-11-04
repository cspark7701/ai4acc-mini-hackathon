"""
tests/test_environment.py
Unit and functional tests for AcceleratorOrbitGymEnv.
Validates environment contract, reset/step physics, hardware limits, and terminations.
"""

import numpy as np
import pytest
from src.environment import AcceleratorOrbitGymEnv, generate_offline_dataset


class TestAcceleratorOrbitGymEnv:
    def test_initialization(self):
        """Test default environment initialization and attributes."""
        env = AcceleratorOrbitGymEnv()
        assert env.n_bpms == 12
        assert env.n_correctors == 6
        assert env.target_rms == 0.030
        assert env.noise_std == 0.010
        assert env.max_steps == 20
        assert env.R.shape == (6, 12)
        assert env.action_space.shape == (6,)
        assert env.observation_space.shape == (12,)

    def test_reset_reproducibility(self):
        """Test that reset produces deterministic initial state given a fixed seed."""
        env = AcceleratorOrbitGymEnv()
        obs1, info1 = env.reset(seed=42)
        obs2, info2 = env.reset(seed=42)

        np.testing.assert_allclose(obs1, obs2, atol=1e-6)
        assert info1["rms"] == pytest.approx(info2["rms"], abs=1e-6)
        assert info1["step"] == 0
        np.testing.assert_allclose(info1["currents"], np.zeros(6))

    def test_reset_different_seeds(self):
        """Test that different seeds draw different initial orbit misalignments."""
        env = AcceleratorOrbitGymEnv()
        obs1, _ = env.reset(seed=42)
        obs2, _ = env.reset(seed=99)

        assert not np.allclose(obs1, obs2)

    def test_action_bounds_and_current_clipping(self):
        """Test per-step delta action clipping [-0.8, 0.8] and total current bounds [-5.0, 5.0]."""
        env = AcceleratorOrbitGymEnv()
        env.reset(seed=42)

        # Action exceeding delta limit [0.8]
        large_action = np.ones(6) * 5.0
        obs, reward, terminated, truncated, info = env.step(large_action)

        # Delta current should be clipped to +0.8 per steerer
        np.testing.assert_allclose(info["currents"], np.ones(6) * 0.8, atol=1e-5)

        # Accumulate over 10 steps to verify hard saturation clip at +/- 5.0 A
        for _ in range(10):
            obs, reward, terminated, truncated, info = env.step(np.ones(6) * 0.8)

        np.testing.assert_allclose(info["currents"], np.ones(6) * 5.0, atol=1e-5)

    def test_step_contract_and_shapes(self):
        """Test step return tuple conforms to standard Gymnasium contract."""
        env = AcceleratorOrbitGymEnv()
        obs, info = env.reset(seed=42)

        action = np.zeros(6, dtype=np.float32)
        next_obs, reward, terminated, truncated, next_info = env.step(action)

        assert isinstance(next_obs, np.ndarray)
        assert next_obs.shape == (12,)
        assert isinstance(reward, float)
        assert isinstance(terminated, bool)
        assert isinstance(truncated, bool)
        assert isinstance(next_info, dict)
        assert "rms" in next_info
        assert "currents" in next_info
        assert next_info["step"] == 1

    def test_truncation_at_max_steps(self):
        """Test environment truncates when step count reaches max_steps (20)."""
        env = AcceleratorOrbitGymEnv()
        env.reset(seed=42)

        for step in range(1, 20):
            obs, reward, terminated, truncated, info = env.step(np.zeros(6))
            assert not truncated
            assert info["step"] == step

        obs, reward, terminated, truncated, info = env.step(np.zeros(6))
        assert truncated
        assert info["step"] == 20

    def test_custom_reward_function(self):
        """Test custom reward callback function hook."""
        called = []

        def custom_reward(rms, action, terminated, truncated, step):
            called.append(step)
            return 100.0 - rms

        env = AcceleratorOrbitGymEnv(reward_fn=custom_reward)
        env.reset(seed=42)
        obs, reward, terminated, truncated, info = env.step(np.zeros(6))

        assert len(called) == 1
        assert called[0] == 1
        assert reward == pytest.approx(100.0 - info["rms"], rel=1e-4)


class TestOfflineDatasetGenerator:
    def test_generate_offline_dataset(self):
        """Test synthetic dataset generator shapes and properties."""
        env = AcceleratorOrbitGymEnv()
        X, Y = generate_offline_dataset(env, n_samples=200, random_state=42)

        assert X.shape == (200, 6)
        assert Y.shape == (200, 12)
        assert np.all(X >= -3.0) and np.all(X <= 3.0)
