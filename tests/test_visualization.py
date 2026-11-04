"""
tests/test_visualization.py
Unit tests for visualization plotting functions in src/visualization.py:
- draw_beamline
- plot_benchmark_trajectories
"""

import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pytest

# Use non-interactive backend for headless test execution
matplotlib.use("Agg")

from src.environment import AcceleratorOrbitGymEnv
from src.controllers import ClassicalSVDController
from src.visualization import draw_beamline, plot_benchmark_trajectories


class TestVisualization:
    def test_draw_beamline(self, tmp_path):
        """Test lattice schematic diagram generation."""
        save_path = str(tmp_path / "beamline_test.png")
        fig = draw_beamline(save_path=save_path, show=False)

        assert isinstance(fig, plt.Figure)
        assert os.path.exists(save_path)
        assert os.path.getsize(save_path) > 1000
        plt.close(fig)

    def test_plot_benchmark_trajectories(self, tmp_path):
        """Test multi-controller trajectory comparison plot."""
        env = AcceleratorOrbitGymEnv()
        agent = ClassicalSVDController(env.R, gain=0.45)

        controllers = {"SVD_Test": agent}
        save_path = str(tmp_path / "trajectory_test.png")

        fig = plot_benchmark_trajectories(env, controllers, seed=42, save_path=save_path, show=False)

        assert isinstance(fig, plt.Figure)
        assert os.path.exists(save_path)
        assert os.path.getsize(save_path) > 1000
        plt.close(fig)
