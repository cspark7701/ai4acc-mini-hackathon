"""
src/environment.py
Accelerator Orbit Alignment Gymnasium Simulation Environment.
"""
from typing import Tuple, Dict, Any, Optional
import numpy as np


class BoxSpace:
    """Gymnasium Box space fallback ensuring zero-dependency compatibility."""
    def __init__(self, low: float, high: float, shape: Tuple[int, ...], dtype=np.float32):
        self.low = np.full(shape, low, dtype=dtype)
        self.high = np.full(shape, high, dtype=dtype)
        self.shape = shape
        self.dtype = dtype

    def sample(self) -> np.ndarray:
        return np.random.uniform(self.low, self.high).astype(self.dtype)


class AcceleratorOrbitGymEnv:
    """Accelerator Orbit Hackathon: Multi-Corrector Beam Alignment Environment."""
    metadata = {"render_modes": ["human"]}

    def __init__(self, max_steps: int = 20, target_rms: float = 0.030, noise_std: float = 0.010):
        self.n_correctors = 6
        self.n_bpms = 12
        self.max_steps = max_steps
        self.target_rms = target_rms
        self.noise_std = noise_std

        self.action_space = BoxSpace(low=-0.8, high=0.8, shape=(self.n_correctors,))
        self.observation_space = BoxSpace(low=-10.0, high=10.0, shape=(self.n_bpms,))

        # Physical Transfer Response Matrix R
        s_bpm = np.linspace(1.0, 15.0, self.n_bpms)
        s_corr = np.linspace(0.2, 8.0, self.n_correctors)
        self.R = np.zeros((self.n_correctors, self.n_bpms), dtype=np.float64)
        for i, sc in enumerate(s_corr):
            for j, sb in enumerate(s_bpm):
                if sb > sc:
                    phase = 2.0 * np.pi * 0.18 * (sb - sc)
                    self.R[i, j] = 1.2 * np.sin(phase) / (1.0 + 0.05 * (sb - sc))

        self.I_corr = np.zeros(self.n_correctors, dtype=np.float32)
        self.perturbation = np.zeros(self.n_bpms, dtype=np.float32)
        self.initial_rms = 0.0
        self.current_step = 0
        self.np_random = np.random.RandomState(42)

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None) -> Tuple[np.ndarray, Dict[str, Any]]:
        if seed is not None:
            self.np_random = np.random.RandomState(seed)
        self.current_step = 0
        self.I_corr = np.zeros(self.n_correctors, dtype=np.float32)

        # Realistic upstream steering misalignment drift perturbation
        drift = self.np_random.uniform(-1.2, 1.2, size=2)
        self.perturbation = (drift[0] * self.R[0] + drift[1] * self.R[1]).astype(np.float32)

        obs = self._get_obs()
        self.initial_rms = float(np.sqrt(np.mean(obs**2)))
        return obs, {"initial_rms": self.initial_rms, "rms": self.initial_rms, "step": 0, "currents": self.I_corr.copy()}

    def _get_obs(self) -> np.ndarray:
        # Cubic iron magnetic saturation: B(I) ~ I - 0.015 * I^3
        response = (self.I_corr @ self.R) - 0.015 * (self.I_corr**3) @ self.R
        noise = self.np_random.normal(0, self.noise_std, size=self.n_bpms)
        return (self.perturbation + response + noise).astype(np.float32)

    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        action = np.clip(action, self.action_space.low, self.action_space.high).astype(np.float32)
        self.I_corr = np.clip(self.I_corr + action, -5.0, 5.0)
        self.current_step += 1

        obs = self._get_obs()
        rms = float(np.sqrt(np.mean(obs**2)))

        # Step Reward: Negative distance penalty + step action effort
        reward = -10.0 * rms - 0.01 * float(np.sum(action**2))
        terminated = bool(rms < self.target_rms)
        truncated = bool(self.current_step >= self.max_steps)

        if terminated:
            reward += 50.0  # Success completion bonus

        info = {
            "initial_rms": self.initial_rms,
            "rms": rms,
            "step": self.current_step,
            "is_success": terminated,
            "currents": self.I_corr.copy()
        }
        return obs, reward, terminated, truncated, info


def generate_offline_dataset(
    env: AcceleratorOrbitGymEnv,
    n_samples: int = 1500,
    current_range: Tuple[float, float] = (-3.0, 3.0),
    noise_std: float = 0.010,
    random_state: int = 42
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic offline dataset of corrector currents and corresponding BPM readings.
    Incorporates linear response, non-linear cubic saturation, and sensor noise.

    Parameters:
        env: AcceleratorOrbitGymEnv instance providing transfer matrix R.
        n_samples: Number of random training samples to generate.
        current_range: (min_current, max_current) in Amperes.
        noise_std: Standard deviation of Gaussian sensor jitter.
        random_state: Seed for reproducible random generation.

    Returns:
        X: Corrector current settings of shape (n_samples, 6) in Amperes.
        Y: Observed BPM displacements of shape (n_samples, 12) in mm.
    """
    rng = np.random.RandomState(random_state)
    X = rng.uniform(current_range[0], current_range[1], size=(n_samples, env.n_correctors)).astype(np.float32)
    Y_linear = X @ env.R
    Y_sat = - 0.015 * (X**3) @ env.R
    noise = rng.normal(0, noise_std, size=(n_samples, env.n_bpms)).astype(np.float32)
    Y = (Y_linear + Y_sat + noise).astype(np.float32)
    return X, Y
