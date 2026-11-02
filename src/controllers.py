"""
src/controllers.py
Benchmark Controllers for the Accelerator Orbit Alignment Challenge.
"""
from typing import Optional, Dict, Any
import numpy as np
import scipy.optimize as opt


class ClassicalSVDController:
    """Baseline 0: Classical linear Orbit Response Matrix pseudo-inverse feedback."""
    def __init__(self, R_matrix: np.ndarray, gain: float = 0.45):
        self.gain = gain
        self.R_pinv = np.linalg.pinv(R_matrix.T)

    def act(self, obs: np.ndarray, info: Optional[Dict[str, Any]] = None) -> np.ndarray:
        return np.clip(- self.gain * (self.R_pinv @ obs), -0.8, 0.8)


class SupervisedMLPController:
    """Baseline 1: Model-based batch optimizer using the MLP digital twin."""
    def __init__(self, surrogate: Any):
        self.surrogate = surrogate

    def act(self, obs: np.ndarray, info: Optional[Dict[str, Any]] = None) -> np.ndarray:
        def objective(delta_I: np.ndarray) -> float:
            pred = self.surrogate.predict(delta_I.reshape(1, -1))[0]
            res = obs + pred
            return float(np.sum(res**2) + 0.0001 * np.sum(delta_I**2))

        res = opt.minimize(objective, np.zeros(6), bounds=[(-5.0, 5.0)] * 6, method='L-BFGS-B')
        return np.clip(res.x, -0.8, 0.8)


class RLOrbitChallengeAgent:
    """Track 2: Closed-loop policy agent with physics-informed prior and adaptive damping."""
    def __init__(self, R_matrix: np.ndarray, gain: float = 0.45):
        self.base_R_pinv = np.linalg.pinv(R_matrix.T)
        self.gain = gain
        self.W_tune = np.zeros((6, 12), dtype=np.float64)
        self.bias = np.zeros(6, dtype=np.float64)

    def act(self, obs: np.ndarray, info: Optional[Dict[str, Any]] = None) -> np.ndarray:
        step_idx = info.get("step", 0) if info else 0
        action_phys = - self.gain * (self.base_R_pinv @ obs)
        action_learned = self.W_tune @ obs + self.bias
        action = action_phys + 0.05 * np.tanh(action_learned)
        damping = 1.0 / (1.0 + 0.03 * step_idx)
        return np.clip(action * damping, -0.8, 0.8)
