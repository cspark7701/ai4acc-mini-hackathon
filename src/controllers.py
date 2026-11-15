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


def _current_state(info: Optional[Dict[str, Any]]) -> np.ndarray:
    """Total corrector currents applied so far (zeros when unknown)."""
    if info and "currents" in info:
        return np.asarray(info["currents"], dtype=np.float64)
    return np.zeros(6)


class SupervisedMLPController:
    """Baseline 1: Model-based batch optimizer using the MLP digital twin.

    The surrogate f(I) maps total corrector currents to the orbit response. The next orbit
    after a kick dI is predicted as  obs - f(I) + f(I + dI),  where I is the present total
    current from info["currents"]; this is exact at every step, not only the first.
    """
    def __init__(self, surrogate: Any):
        self.surrogate = surrogate

    def act(self, obs: np.ndarray, info: Optional[Dict[str, Any]] = None) -> np.ndarray:
        I_now = _current_state(info)
        f_now = self.surrogate.predict(I_now.reshape(1, -1))[0]

        def objective(delta_I: np.ndarray) -> float:
            pred = self.surrogate.predict((I_now + delta_I).reshape(1, -1))[0]
            res = obs - f_now + pred
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


class BayesianOptimizationController:
    """
    Track 3: Closed-Loop Bayesian Optimization Controller using Gaussian Processes.

    Leverages a Gaussian Process surrogate to model non-linear orbit response with epistemic
    uncertainty estimation. Solves a bounded acquisition function (Lower Confidence Bound, LCB)
    per step to balance exploitation of predicted orbit corrections against exploration:
        alpha_LCB(dI) = RMS(obs - mu(I) + mu(I + dI)) - kappa * sigma(I + dI) + lambda * ||dI||^2
    where I is the present total corrector current from info["currents"].
    """
    def __init__(
        self,
        gp_surrogate: Any,
        kappa: float = 0.0,
        l2_reg: float = 0.0001,
        delta_bound: float = 0.8
    ):
        self.gp = gp_surrogate
        self.kappa = float(kappa)
        self.l2_reg = float(l2_reg)
        self.delta_bound = float(delta_bound)

    def act(self, obs: np.ndarray, info: Optional[Dict[str, Any]] = None) -> np.ndarray:
        I_now = _current_state(info)
        mu_now = self.gp.predict(I_now.reshape(1, -1))[0]

        def acquisition_lcb(delta_I: np.ndarray) -> float:
            pred_mean, pred_std = self.gp.predict((I_now + delta_I).reshape(1, -1), return_std=True)
            res = obs - mu_now + pred_mean[0]
            rms_pred = np.sqrt(np.mean(res**2))
            unc = np.mean(pred_std)
            return float(rms_pred - self.kappa * unc + self.l2_reg * np.sum(delta_I**2))

        res = opt.minimize(
            acquisition_lcb,
            np.zeros(6),
            bounds=[(-5.0, 5.0)] * 6,
            method='L-BFGS-B'
        )
        return np.clip(res.x, -self.delta_bound, self.delta_bound)
