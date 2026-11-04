"""
tests/test_controllers.py
Unit tests for standard baseline and hackathon competitor controllers:
- ClassicalSVDController (Baseline 0)
- SupervisedMLPController (Baseline 1)
- RLOrbitChallengeAgent (Track 2)
- BayesianOptimizationController (Track 3)
"""

import numpy as np
import pytest
from src.environment import AcceleratorOrbitGymEnv, generate_offline_dataset
from src.controllers import (
    ClassicalSVDController,
    SupervisedMLPController,
    RLOrbitChallengeAgent,
    BayesianOptimizationController,
)
from sklearn.neural_network import MLPRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel


@pytest.fixture(scope="module")
def env():
    return AcceleratorOrbitGymEnv()


@pytest.fixture(scope="module")
def trained_surrogates(env):
    X, Y = generate_offline_dataset(env, n_samples=300, random_state=42)

    # MLP
    mlp = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=200, random_state=42)
    mlp.fit(X, Y)

    # GP: Fix noise floor to the known physical sensor jitter variance (0.010 mm)^2
    gp_kernel = Matern(length_scale=1.5, nu=2.5) + WhiteKernel(
        noise_level=0.01**2, noise_level_bounds="fixed"
    )
    gp = GaussianProcessRegressor(kernel=gp_kernel, alpha=0.0, normalize_y=True, random_state=42)
    gp.fit(X[:150], Y[:150])

    return mlp, gp


class TestControllers:
    def test_classical_svd_controller(self, env):
        """Test Baseline 0 linear SVD pseudo-inverse controller."""
        controller = ClassicalSVDController(env.R, gain=0.45)
        obs, info = env.reset(seed=42)

        action = controller.act(obs, info)

        assert isinstance(action, np.ndarray)
        assert action.shape == (6,)
        assert np.all(action >= -0.8) and np.all(action <= 0.8)

        # Stepping with SVD controller should reduce orbit error
        next_obs, reward, terminated, truncated, next_info = env.step(action)
        assert next_info["rms"] < info["rms"]

    def test_supervised_mlp_controller(self, env, trained_surrogates):
        """Test Baseline 1 model-inversion optimizer controller."""
        mlp, _ = trained_surrogates
        controller = SupervisedMLPController(mlp)
        obs, info = env.reset(seed=42)

        action = controller.act(obs, info)

        assert isinstance(action, np.ndarray)
        assert action.shape == (6,)
        assert np.all(action >= -0.8) and np.all(action <= 0.8)

    def test_rl_challenge_agent(self, env):
        """Test Track 2 RL/adaptive challenge agent with physics prior and damping."""
        agent = RLOrbitChallengeAgent(env.R, gain=0.45)
        obs, info = env.reset(seed=42)

        action_step0 = agent.act(obs, {"step": 0})
        action_step5 = agent.act(obs, {"step": 5})

        assert action_step0.shape == (6,)
        assert np.all(action_step0 >= -0.8) and np.all(action_step0 <= 0.8)

        # Damping should reduce magnitude on later steps for identical observation
        norm0 = np.linalg.norm(action_step0)
        norm5 = np.linalg.norm(action_step5)
        assert norm5 < norm0

    def test_bayesian_optimization_controller(self, env, trained_surrogates):
        """Test Track 3 Bayesian Optimization Gaussian Process controller."""
        _, gp = trained_surrogates
        controller = BayesianOptimizationController(gp, kappa=0.0, l2_reg=0.0001)
        obs, info = env.reset(seed=42)

        action = controller.act(obs, info)

        assert isinstance(action, np.ndarray)
        assert action.shape == (6,)
        assert np.all(action >= -0.8) and np.all(action <= 0.8)

        next_obs, reward, terminated, truncated, next_info = env.step(action)
        assert next_info["rms"] < info["rms"]
