"""
src Package
Core simulation environment, baseline controllers, and evaluation harness.
"""
from src.environment import AcceleratorOrbitGymEnv, BoxSpace, generate_offline_dataset
from src.controllers import (
    ClassicalSVDController,
    SupervisedMLPController,
    RLOrbitChallengeAgent
)
from src.benchmark import evaluate_hackathon_benchmark, print_benchmark_leaderboard
from src.visualization import draw_beamline, plot_benchmark_trajectories

__all__ = [
    "AcceleratorOrbitGymEnv",
    "BoxSpace",
    "generate_offline_dataset",
    "ClassicalSVDController",
    "SupervisedMLPController",
    "RLOrbitChallengeAgent",
    "evaluate_hackathon_benchmark",
    "print_benchmark_leaderboard",
    "draw_beamline",
    "plot_benchmark_trajectories"
]
