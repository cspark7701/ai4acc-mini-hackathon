"""
scripts/update_notebooks.py
Updates Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb and
Single_Notebook_Beam_Orbit_Predictor_Solution.ipynb to include Track 3 (Bayesian Optimization)
and reflect the updated Lecture 1 title.
"""
import json

def update_participant_notebook():
    path = "notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb"
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # 1. Update Cell 0 (Title & Tracks)
    nb["cells"][0]["source"] = [
        "# Accelerator Orbit Alignment Hackathon: Beam Orbit Benchmark\n",
        "## Participant Edition (with Weights & Biases / W&B Leaderboard Integration)\n",
        "\n",
        "**Workshop & Challenge Context:**\n",
        "* **Author:** Chong Shik Park, Ph.D.\n",
        "* **Date:** November 19, 2026\n",
        "* **Target Audience:** Graduate Students & Early-Career Accelerator Researchers\n",
        "* **Curricular Alignment:** \n",
        "  * **Lecture 1:** Chong Shik Park — AI/ML Foundations and Closed-Loop Control for Particle Accelerators\n",
        "  * **Lecture 2:** Thorsten Hellert — Agentic AI, Autonomous Operations & Scientific Workflows\n",
        "\n",
        "---\n",
        "\n",
        "### 🎯 Challenge Mission\n",
        "In modern particle accelerators and beam transport lines, beam alignment is critical to ensure high transmission efficiency and prevent beam loss. \n",
        "In this hackathon, you will develop closed-loop control algorithms to steer the beam through a **15-meter transport line** with:\n",
        "* **6 Dipole Steering Magnets:** $X = [\\mathrm{HCM1}, \\mathrm{VCM1}, \\mathrm{HCM2}, \\mathrm{VCM2}, \\mathrm{HCM3}, \\mathrm{VCM3}]^T \\in [-5.0\\text{ A}, +5.0\\text{ A}]$\n",
        "* **12 Beam Position Monitors (BPMs):** $Y \\in \\mathbb{R}^{12}$, measuring transverse beam offsets in millimeters (mm).\n",
        "* **Non-Linear Iron Saturation:** $B(I) \\approx I - 0.015 \\cdot I^3$, causing progressive softening at higher corrector currents.\n",
        "* **Objective:** Align the beam so that the Root-Mean-Square (RMS) displacement is below **$0.030\\text{ mm}$** within a budget of **20 control steps**:\n",
        "  $$\\text{RMS} = \\sqrt{\\frac{1}{12}\\sum_{i=1}^{12} Y_i^2} < 0.030\\text{ mm}$$\n",
        "\n",
        "---\n",
        "\n",
        "### 🏆 Three Parallel Competition Tracks:\n",
        "1. **Track 1 (Supervised Digital Twin Inversion):** Train a non-linear neural surrogate model (MLP) on offline tracking data, and use an optimization solver to invert the surrogate for optimal corrective kicks.\n",
        "2. **Track 2 (Closed-Loop Reinforcement Learning / Adaptive Policy):** Design an interactive feedback policy agent that continuously senses BPM offsets and outputs delta current kicks $\\Delta I_c$ with physics-informed priors and adaptive damping.\n",
        "3. **Track 3 (Bayesian Optimization Controller):** Build a sample-efficient Gaussian Process controller with Lower Confidence Bound (LCB) acquisition to actively align the beam under non-linear saturation.\n"
    ]

    # 2. Update Cell 1 (Imports)
    nb["cells"][1]["source"] = [
        "# Step 0: Imports, Environment Setup, and Weights & Biases (W&B) Configuration\n",
        "import os\n",
        "import time\n",
        "import numpy as np\n",
        "import matplotlib.pyplot as plt\n",
        "from sklearn.model_selection import train_test_split\n",
        "from sklearn.metrics import root_mean_squared_error\n",
        "from sklearn.linear_model import Ridge\n",
        "from sklearn.neural_network import MLPRegressor\n",
        "from sklearn.gaussian_process import GaussianProcessRegressor\n",
        "from sklearn.gaussian_process.kernels import Matern, WhiteKernel\n",
        "\n",
        "# Import standardized simulation, controllers, benchmark & visualization from src/\n",
        "from src import (\n",
        "    AcceleratorOrbitGymEnv,\n",
        "    ClassicalSVDController,\n",
        "    SupervisedMLPController,\n",
        "    RLOrbitChallengeAgent,\n",
        "    BayesianOptimizationController,\n",
        "    generate_offline_dataset,\n",
        "    evaluate_hackathon_benchmark,\n",
        "    print_benchmark_leaderboard,\n",
        "    draw_beamline,\n",
        "    plot_benchmark_trajectories\n",
        ")\n",
        "\n",
        "# ------------------------------------------------------------------------------\n",
        "# Hackathon Configuration (Customize for Your Team!)\n",
        "# ------------------------------------------------------------------------------\n",
        "# >>> [PARTICIPANT MODIFY HERE]: Change to your registered team name!\n",
        "TEAM_NAME = \"Team_Alpha\"\n",
        "\n",
        "# >>> [DO NOT MODIFY]: Official workshop competition settings\n",
        "WANDB_PROJECT = \"accelerator-orbit-hackathon\" # [DO NOT CHANGE] Official project name for live leaderboard\n",
        "WANDB_ENTITY = None                          # [DO NOT CHANGE] Preset workshop entity\n",
        "USE_WANDB = True                             # [DO NOT CHANGE] Keep True to submit scores to the live leaderboard\n",
        "\n",
        "print(f\"Setup complete! Ready to compete as: {TEAM_NAME}\")\n"
    ]

    # 3. Update Cell 8 (Section 4 Markdown: 4 controllers)
    nb["cells"][8]["source"] = [
        "---\n",
        "## 4. Benchmark Controllers: Classical, Supervised, RL, and Bayesian Optimization Agents\n",
        "\n",
        "Every competitor controller must implement the standardized agent interface:\n",
        "```python\n",
        "def act(self, obs: np.ndarray, info: Optional[dict] = None) -> np.ndarray\n",
        "```\n",
        "where `obs` has shape `(12,)` and the returned action is an array of shape `(6,)` in $[-0.8\\text{ A}, +0.8\\text{ A}]$.\n",
        "\n",
        "1. **Baseline 0 (Classical SVD Controller):** Inverts the linear Orbit Response Matrix via Moore-Penrose pseudo-inverse: $\\Delta \\mathbf{I} = - \\alpha (\\mathbf{R}^T)^{\\dagger} \\mathbf{Y}$.\n",
        "2. **Baseline 1 / Track 1 (Supervised Neural Inversion):** Solves an optimization problem per step using the trained neural surrogate digital twin:\n",
        "   $$\\min_{\\Delta \\mathbf{I}} \\|\\mathbf{Y} + f_{\\theta}(\\Delta \\mathbf{I})\\|^2 + \\lambda \\|\\Delta \\mathbf{I}\\|^2$$\n",
        "3. **Challenge Track 2 (Closed-Loop RL / Adaptive Agent):** Combines physics prior feedback with adaptive step damping:\n",
        "   $$\\Delta \\mathbf{I}_t = \\text{damping}(t) \\cdot \\left[ - \\alpha (\\mathbf{R}^T)^{\\dagger} \\mathbf{Y} + \\mathbf{W}_{\\text{tune}} \\mathbf{Y} + \\mathbf{b} \\right]$$\n",
        "   RL agents learn or optimize policy parameters by interacting with `AcceleratorOrbitGymEnv`. By tuning reward and penalty weights (`step_penalty`, `action_weight`, `rms_weight`, `success_bonus`), you can directly incentivize the agent to converge in fewer steps and use minimal corrector current!\n",
        "4. **Challenge Track 3 (Bayesian Optimization Controller):** Uses a Gaussian Process surrogate with epistemic uncertainty estimation to evaluate an acquisition function (Lower Confidence Bound, LCB) balancing exploitation of predicted orbit corrections with exploration:\n",
        "   $$\\alpha_{\\text{LCB}}(\\Delta \\mathbf{I}) = \\text{RMS}(\\mathbf{Y}_{\\text{obs}} + \\mu_{\\text{GP}}(\\Delta \\mathbf{I})) - \\kappa \\cdot \\sigma_{\\text{GP}}(\\Delta \\mathbf{I}) + \\lambda \\|\\Delta \\mathbf{I}\\|^2$$\n"
    ]

    # 4. Update Cell 9 (Code: add TODO 3 for Bayesian Optimization)
    cell9_code = nb["cells"][9]["source"]
    todo3_text = [
        "\n",
        "# ==============================================================================\n",
        "# TODO 3 (Challenge Track 3): Design & Tune Bayesian Optimization Controller\n",
        "# ==============================================================================\n",
        "# INSTRUCTIONS FOR PARTICIPANTS:\n",
        "# Implement a Bayesian Optimization controller using GaussianProcessRegressor.\n",
        "# 1. Train a Gaussian Process surrogate on calibration data (or a 300-shot subset).\n",
        "# 2. Configure the GP kernel (e.g. Matern, RBF, WhiteKernel for 10 um sensor noise).\n",
        "# 3. Implement the Lower Confidence Bound (LCB) acquisition function:\n",
        "#      alpha_LCB = rms_pred - kappa * uncertainty + lambda * ||action||^2\n",
        "# 4. Tune exploration weight kappa (e.g. 0.0 for pure exploitation, 0.5-1.5 for exploration).\n",
        "#\n",
        "# ------------------------------------------------------------------------------\n",
        "# EXAMPLES FOR NEWBIE PARTICIPANTS:\n",
        "#\n",
        "# Example: Fit Gaussian Process Regressor on Calibration Shots\n",
        "#   gp_kernel = Matern(length_scale=1.5, nu=2.5) + WhiteKernel(noise_level=1e-4, noise_level_bounds='fixed')\n",
        "#   gp_model = GaussianProcessRegressor(kernel=gp_kernel, alpha=0.0, normalize_y=True, random_state=42)\n",
        "#   gp_model.fit(X_train[:300], Y_train[:300]) # 300 samples provides sub-second fitting!\n",
        "#\n",
        "# ------------------------------------------------------------------------------\n",
        "# 💡 STRATEGIC TUNING HINTS: WHICH VALUES TO MODIFY TO GET HIGHER SCORES!\n",
        "#\n",
        "# 1. Exploration vs. Exploitation Parameter (kappa):\n",
        "#    • kappa = 0.0: Pure exploitation of the GP posterior mean (fastest convergence!).\n",
        "#    • kappa = 0.5 - 1.5: Actively balances uncertainty in high-current non-linear saturation zones.\n",
        "#\n",
        "# 2. Kernel Selection:\n",
        "#    • Matern(nu=2.5) provides physically realistic smoothness for magnetic field response.\n",
        "#    • WhiteKernel(noise_level=1e-4, noise_level_bounds='fixed') fixes the 0.010 mm BPM sensor jitter prior.\n",
        "#\n",
        "# 3. Regularization (l2_reg):\n",
        "#    • Adding small L2 penalty (e.g. 1e-4) suppresses excessive corrector current norms.\n",
        "# ==============================================================================\n",
        "\n",
        "# >>> [PARTICIPANT MODIFY HERE - TODO 3 (CHALLENGE TRACK 3)] <<<\n",
        "class MyBayesianOptAgent:\n",
        "    \"\"\"Track 3: Participant Custom Bayesian Optimization Controller.\"\"\"\n",
        "    def __init__(self, gp_model, kappa=0.0, l2_reg=0.0001):\n",
        "        # [CAN MODIFY]: Gaussian Process surrogate model\n",
        "        self.gp = gp_model\n",
        "        # [CAN MODIFY]: Exploration weight kappa (Try 0.0 for pure exploitation, or 0.5 for active exploration)\n",
        "        self.kappa = float(kappa)\n",
        "        # [CAN MODIFY]: Action penalty regularization weight\n",
        "        self.l2_reg = float(l2_reg)\n",
        "\n",
        "    def act(self, obs, info=None):\n",
        "        \"\"\"\n",
        "        [PARTICIPANT TODO]: Minimize acquisition function to select optimal delta current kick.\n",
        "        \"\"\"\n",
        "        import scipy.optimize as opt\n",
        "        def acquisition_lcb(delta_I):\n",
        "            pred_mean, pred_std = self.gp.predict(delta_I.reshape(1, -1), return_std=True)\n",
        "            res = obs + pred_mean[0]\n",
        "            rms_pred = np.sqrt(np.mean(res**2))\n",
        "            unc = np.mean(pred_std)\n",
        "            # Lower Confidence Bound (LCB) acquisition\n",
        "            return float(rms_pred - self.kappa * unc + self.l2_reg * np.sum(delta_I**2))\n",
        "\n",
        "        res = opt.minimize(\n",
        "            acquisition_lcb,\n",
        "            np.zeros(6),\n",
        "            bounds=[(-5.0, 5.0)] * 6,\n",
        "            method='L-BFGS-B'\n",
        "        )\n",
        "        return np.clip(res.x, -0.8, 0.8)\n",
        "\n",
        "# >>> [CAN MODIFY]: Fit Gaussian Process surrogate on calibration data (e.g. 300 shots):\n",
        "gp_kernel = Matern(length_scale=1.5, nu=2.5) + WhiteKernel(noise_level=1e-4, noise_level_bounds='fixed')\n",
        "gp_surrogate = GaussianProcessRegressor(kernel=gp_kernel, alpha=0.0, normalize_y=True, random_state=42)\n",
        "gp_surrogate.fit(X_train[:300], Y_train[:300])\n",
        "\n",
        "# >>> [CAN MODIFY]: Instantiate your Track 3 Bayesian Optimization Controller:\n",
        "b3 = MyBayesianOptAgent(gp_surrogate, kappa=0.0, l2_reg=0.0001)\n",
        "print(\"All four competitor controllers (Baseline 0, Track 1, Track 2, Track 3) initialized successfully.\")\n"
    ]

    new_cell9 = []
    for line in cell9_code:
        if 'print("All three competitor controllers' in line:
            new_cell9.extend(todo3_text)
        else:
            new_cell9.append(line)
    nb["cells"][9]["source"] = new_cell9

    # 5. Update Cell 11 (Evaluation & Leaderboard)
    nb["cells"][11]["source"] = [
        "# Step 5: Standardized Evaluation Harness with Weights & Biases Logging\n",
        "# ==============================================================================\n",
        "# [DO NOT MODIFY - Standardized 30-Seed Evaluation Protocol]\n",
        "# ==============================================================================\n",
        "# Evaluates each competitor controller across 30 standardized seeds (range 1 to 31).\n",
        "# Telemetry, seed breakdowns, and scores are automatically uploaded to W&B.\n",
        "print(\"Running Official Hackathon Benchmark across 30 Test Seeds...\")\n",
        "\n",
        "res_b0 = evaluate_hackathon_benchmark(env, b0, agent_name=\"Baseline0_LinearSVD\", team_name=TEAM_NAME, use_wandb=USE_WANDB, project=WANDB_PROJECT, entity=WANDB_ENTITY)\n",
        "res_b1 = evaluate_hackathon_benchmark(env, b1, agent_name=\"Baseline1_SupervisedMLP\", team_name=TEAM_NAME, use_wandb=USE_WANDB, project=WANDB_PROJECT, entity=WANDB_ENTITY)\n",
        "res_b2 = evaluate_hackathon_benchmark(env, b2, agent_name=\"Track2_RLAgent\", team_name=TEAM_NAME, use_wandb=USE_WANDB, project=WANDB_PROJECT, entity=WANDB_ENTITY)\n",
        "res_b3 = evaluate_hackathon_benchmark(env, b3, agent_name=\"Track3_BayesianOpt\", team_name=TEAM_NAME, use_wandb=USE_WANDB, project=WANDB_PROJECT, entity=WANDB_ENTITY)\n",
        "\n",
        "# Display Official Leaderboard Table\n",
        "print_benchmark_leaderboard([\n",
        "    (\"Track 3 (Bayesian Optimization Controller)\", res_b3),\n",
        "    (\"Baseline 1 (Supervised MLP Inversion)\", res_b1),\n",
        "    (\"Baseline 0 (Linear ORM SVD Controller)\", res_b0),\n",
        "    (\"Track 2 (RL Closed-Loop Agent)\", res_b2),\n",
        "])\n"
    ]

    # 6. Update Cell 13 (Trajectory Visualization)
    nb["cells"][13]["source"] = [
        "# Step 6: Generate Dual Trajectory Overlay & Dynamic Convergence Curves\n",
        "# ==============================================================================\n",
        "# [DO NOT MODIFY - Canonical Diagnostic Visualization]\n",
        "# ==============================================================================\n",
        "fig = plot_benchmark_trajectories(\n",
        "    env,\n",
        "    controllers={\n",
        "        \"Linear SVD\": b0,\n",
        "        \"Supervised MLP\": b1,\n",
        "        \"RL Agent\": b2,\n",
        "        \"Bayesian Opt\": b3\n",
        "    },\n",
        "    seed=42,\n",
        "    save_path=\"img/benchmark_trajectories.png\",\n",
        "    show=True\n",
        ")\n"
    ]

    # 7. Update Cell 15 (Final Team Showcase)
    nb["cells"][15]["source"] = [
        "# Step 7: Final Team Showcase Presentation Summary\n",
        "# ==============================================================================\n",
        "# [DO NOT MODIFY - Automated Showcase Scorecard for Presentation]\n",
        "# ==============================================================================\n",
        "best_agent_name, best_metrics = max(\n",
        "    [(\"Track 3 (Bayesian Optimization)\", res_b3),\n",
        "     (\"Track 2 (RL Closed-Loop Agent)\", res_b2),\n",
        "     (\"Baseline 1 (Supervised MLP)\", res_b1),\n",
        "     (\"Baseline 0 (Linear SVD)\", res_b0)],\n",
        "    key=lambda item: item[1][\"score\"]\n",
        ")\n",
        "\n",
        "print(\"=\" * 68)\n",
        "print(f\"   TEAM: {TEAM_NAME} — OFFICIAL HACKATHON BENCHMARK SUBMISSION\")\n",
        "print(\"=\" * 68)\n",
        "print(f\"  • Best Performing Agent  : {best_agent_name}\")\n",
        "print(f\"  • Official Total Score   : {best_metrics['score']:.1f} points\")\n",
        "print(f\"  • Alignment Success Rate : {best_metrics['success_rate']:.1f}%\")\n",
        "print(f\"  • Mean Steps to Target   : {best_metrics['mean_steps']:.1f} steps\")\n",
        "print(f\"  • Mean Residual Orbit RMS: {best_metrics['mean_rms']:.4f} mm\")\n",
        "print(f\"  • Mean Corrector Norm    : {best_metrics['mean_norm']:.2f} A\")\n",
        "print(f\"  • Mean Policy Latency    : {best_metrics['mean_latency']:.2f} ms\")\n",
        "print(\"=\" * 68)\n"
    ]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    print("Updated Participant notebook successfully!")


def update_solution_notebook():
    path = "notebooks/Single_Notebook_Beam_Orbit_Predictor_Solution.ipynb"
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # 1. Update Cell 0 (Title & Tracks)
    nb["cells"][0]["source"] = [
        "# Accelerator Orbit Alignment Hackathon: Beam Orbit Benchmark\n",
        "## Solution & Reference Benchmark Edition (with Weights & Biases / W&B Leaderboard Integration)\n",
        "\n",
        "**Workshop & Challenge Context:**\n",
        "* **Author:** Chong Shik Park, Ph.D.\n",
        "* **Date:** November 19, 2026\n",
        "* **Target Audience:** Graduate Students & Early-Career Accelerator Researchers\n",
        "* **Curricular Alignment:** \n",
        "  * **Lecture 1:** Chong Shik Park — AI/ML Foundations and Closed-Loop Control for Particle Accelerators\n",
        "  * **Lecture 2:** Thorsten Hellert — Agentic AI, Autonomous Operations & Scientific Workflows\n",
        "\n",
        "---\n",
        "\n",
        "### 🎯 Challenge Mission\n",
        "In modern particle accelerators and beam transport lines, beam alignment is critical to ensure high transmission efficiency and prevent beam loss. \n",
        "In this hackathon, you will develop closed-loop control algorithms to steer the beam through a **15-meter transport line** with:\n",
        "* **6 Dipole Steering Magnets:** $X = [\\mathrm{HCM1}, \\mathrm{VCM1}, \\mathrm{HCM2}, \\mathrm{VCM2}, \\mathrm{HCM3}, \\mathrm{VCM3}]^T \\in [-5.0\\text{ A}, +5.0\\text{ A}]$\n",
        "* **12 Beam Position Monitors (BPMs):** $Y \\in \\mathbb{R}^{12}$, measuring transverse beam offsets in millimeters (mm).\n",
        "* **Non-Linear Iron Saturation:** $B(I) \\approx I - 0.015 \\cdot I^3$, causing progressive softening at higher corrector currents.\n",
        "* **Objective:** Align the beam so that the Root-Mean-Square (RMS) displacement is below **$0.030\\text{ mm}$** within a budget of **20 control steps**:\n",
        "  $$\\text{RMS} = \\sqrt{\\frac{1}{12}\\sum_{i=1}^{12} Y_i^2} < 0.030\\text{ mm}$$\n",
        "\n",
        "---\n",
        "\n",
        "### 🏆 Three Parallel Competition Tracks:\n",
        "1. **Track 1 (Supervised Digital Twin Inversion):** Train a non-linear neural surrogate model (MLP) on offline tracking data, and use an optimization solver to invert the surrogate for optimal corrective kicks.\n",
        "2. **Track 2 (Closed-Loop Reinforcement Learning / Adaptive Policy):** Design an interactive feedback policy agent that continuously senses BPM offsets and outputs delta current kicks $\\Delta I_c$ with physics-informed priors and adaptive damping.\n",
        "3. **Track 3 (Bayesian Optimization Controller):** Build a sample-efficient Gaussian Process controller with Lower Confidence Bound (LCB) acquisition to actively align the beam under non-linear saturation.\n"
    ]

    # 2. Update Cell 1 (Imports)
    nb["cells"][1]["source"] = [
        "# Step 0: Imports, Environment Setup, and Weights & Biases (W&B) Configuration\n",
        "import os\n",
        "import time\n",
        "import numpy as np\n",
        "import matplotlib.pyplot as plt\n",
        "from sklearn.model_selection import train_test_split\n",
        "from sklearn.metrics import root_mean_squared_error\n",
        "from sklearn.linear_model import Ridge\n",
        "from sklearn.neural_network import MLPRegressor\n",
        "from sklearn.gaussian_process import GaussianProcessRegressor\n",
        "from sklearn.gaussian_process.kernels import Matern, WhiteKernel\n",
        "\n",
        "# Import standardized simulation, controllers, benchmark & visualization from src/\n",
        "from src import (\n",
        "    AcceleratorOrbitGymEnv,\n",
        "    ClassicalSVDController,\n",
        "    SupervisedMLPController,\n",
        "    RLOrbitChallengeAgent,\n",
        "    BayesianOptimizationController,\n",
        "    generate_offline_dataset,\n",
        "    evaluate_hackathon_benchmark,\n",
        "    print_benchmark_leaderboard,\n",
        "    draw_beamline,\n",
        "    plot_benchmark_trajectories\n",
        ")\n",
        "\n",
        "# ------------------------------------------------------------------------------\n",
        "# Hackathon Configuration (Customize for Your Team!)\n",
        "# ------------------------------------------------------------------------------\n",
        "# >>> [PARTICIPANT MODIFY HERE]: Change to your registered team name!\n",
        "TEAM_NAME = \"Team_ReferenceSolution\"\n",
        "\n",
        "# >>> [DO NOT MODIFY]: Official workshop competition settings\n",
        "WANDB_PROJECT = \"accelerator-orbit-hackathon\" # [DO NOT CHANGE] Official project name for live leaderboard\n",
        "WANDB_ENTITY = None                          # [DO NOT CHANGE] Preset workshop entity\n",
        "USE_WANDB = False                            # Offline local evaluation mode for solution notebook\n",
        "\n",
        "print(f\"Setup complete! Ready to compete as: {TEAM_NAME}\")\n"
    ]

    # 3. Update Cell 8 (Section 4 Markdown: 4 controllers)
    nb["cells"][8]["source"] = [
        "---\n",
        "## 4. Benchmark Controllers: Classical, Supervised, RL, and Bayesian Optimization Agents\n",
        "\n",
        "Every competitor controller must implement the standardized agent interface:\n",
        "```python\n",
        "def act(self, obs: np.ndarray, info: Optional[dict] = None) -> np.ndarray\n",
        "```\n",
        "where `obs` has shape `(12,)` and the returned action is an array of shape `(6,)` in $[-0.8\\text{ A}, +0.8\\text{ A}]$.\n",
        "\n",
        "1. **Baseline 0 (Classical SVD Controller):** Inverts the linear Orbit Response Matrix via Moore-Penrose pseudo-inverse: $\\Delta \\mathbf{I} = - \\alpha (\\mathbf{R}^T)^{\\dagger} \\mathbf{Y}$.\n",
        "2. **Baseline 1 / Track 1 (Supervised Neural Inversion):** Solves an optimization problem per step using the trained neural surrogate digital twin:\n",
        "   $$\\min_{\\Delta \\mathbf{I}} \\|\\mathbf{Y} + f_{\\theta}(\\Delta \\mathbf{I})\\|^2 + \\lambda \\|\\Delta \\mathbf{I}\\|^2$$\n",
        "3. **Challenge Track 2 (Closed-Loop RL / Adaptive Agent):** Combines physics prior feedback with adaptive step damping:\n",
        "   $$\\Delta \\mathbf{I}_t = \\text{damping}(t) \\cdot \\left[ - \\alpha (\\mathbf{R}^T)^{\\dagger} \\mathbf{Y} + \\mathbf{W}_{\\text{tune}} \\mathbf{Y} + \\mathbf{b} \\right]$$\n",
        "4. **Challenge Track 3 (Bayesian Optimization Controller):** Uses a Gaussian Process surrogate with epistemic uncertainty estimation to evaluate an acquisition function (Lower Confidence Bound, LCB) balancing exploitation of predicted orbit corrections with exploration:\n",
        "   $$\\alpha_{\\text{LCB}}(\\Delta \\mathbf{I}) = \\text{RMS}(\\mathbf{Y}_{\\text{obs}} + \\mu_{\\text{GP}}(\\Delta \\mathbf{I})) - \\kappa \\cdot \\sigma_{\\text{GP}}(\\Delta \\mathbf{I}) + \\lambda \\|\\Delta \\mathbf{I}\\|^2$$\n"
    ]

    # 4. Update Cell 9 (Code: add Track 3 reference controller)
    nb["cells"][9]["source"] = [
        "# Step 4: Define Benchmark Controllers\n",
        "\n",
        "# ------------------------------------------------------------------------------\n",
        "# 1. Baseline 0: Classical Linear ORM Pseudo-Inverse Controller (from src)\n",
        "# ------------------------------------------------------------------------------\n",
        "# [Reference Baseline 0]:\n",
        "b0 = ClassicalSVDController(env.R, gain=0.45)\n",
        "\n",
        "# ------------------------------------------------------------------------------\n",
        "# 2. Baseline 1: Supervised Forward Surrogate + SciPy Inversion Optimizer (from src)\n",
        "# ------------------------------------------------------------------------------\n",
        "# [Reference Baseline 1]:\n",
        "b1 = SupervisedMLPController(surrogate_model)\n",
        "\n",
        "# ------------------------------------------------------------------------------\n",
        "# 3. Track 2: Reference Closed-Loop RL / Adaptive Agent (from src)\n",
        "# ------------------------------------------------------------------------------\n",
        "# [Reference Solution Agent]:\n",
        "b2 = RLOrbitChallengeAgent(env.R, gain=0.45)\n",
        "\n",
        "# ------------------------------------------------------------------------------\n",
        "# 4. Track 3: Reference Bayesian Optimization Controller (from src)\n",
        "# ------------------------------------------------------------------------------\n",
        "# Fit Gaussian Process surrogate on calibration data (300 samples for sub-second fitting)\n",
        "gp_kernel = Matern(length_scale=1.5, nu=2.5) + WhiteKernel(noise_level=1e-4, noise_level_bounds='fixed')\n",
        "gp_surrogate = GaussianProcessRegressor(kernel=gp_kernel, alpha=0.0, normalize_y=True, random_state=42)\n",
        "gp_surrogate.fit(X_train[:300], Y_train[:300])\n",
        "\n",
        "# [Reference Solution Agent]:\n",
        "b3 = BayesianOptimizationController(gp_surrogate, kappa=0.0, l2_reg=0.0001)\n",
        "\n",
        "print(\"All four competitor controllers (Baseline 0, Track 1, Track 2, Track 3) initialized successfully.\")\n"
    ]

    # 5. Update Cell 11 (Evaluation & Leaderboard)
    nb["cells"][11]["source"] = [
        "# Step 5: Standardized Evaluation Harness with Weights & Biases Logging\n",
        "# ==============================================================================\n",
        "# [DO NOT MODIFY - Standardized 30-Seed Evaluation Protocol]\n",
        "# ==============================================================================\n",
        "# Evaluates each competitor controller across 30 standardized seeds (range 1 to 31).\n",
        "# Telemetry, seed breakdowns, and scores are automatically uploaded to W&B.\n",
        "print(\"Running Official Hackathon Benchmark across 30 Test Seeds...\")\n",
        "\n",
        "res_b0 = evaluate_hackathon_benchmark(env, b0, agent_name=\"Baseline0_LinearSVD\", team_name=TEAM_NAME, use_wandb=USE_WANDB, project=WANDB_PROJECT, entity=WANDB_ENTITY)\n",
        "res_b1 = evaluate_hackathon_benchmark(env, b1, agent_name=\"Baseline1_SupervisedMLP\", team_name=TEAM_NAME, use_wandb=USE_WANDB, project=WANDB_PROJECT, entity=WANDB_ENTITY)\n",
        "res_b2 = evaluate_hackathon_benchmark(env, b2, agent_name=\"Track2_RLAgent\", team_name=TEAM_NAME, use_wandb=USE_WANDB, project=WANDB_PROJECT, entity=WANDB_ENTITY)\n",
        "res_b3 = evaluate_hackathon_benchmark(env, b3, agent_name=\"Track3_BayesianOpt\", team_name=TEAM_NAME, use_wandb=USE_WANDB, project=WANDB_PROJECT, entity=WANDB_ENTITY)\n",
        "\n",
        "# Display Official Leaderboard Table\n",
        "print_benchmark_leaderboard([\n",
        "    (\"Track 3 (Bayesian Optimization Controller)\", res_b3),\n",
        "    (\"Baseline 1 (Supervised MLP Inversion)\", res_b1),\n",
        "    (\"Baseline 0 (Linear ORM SVD Controller)\", res_b0),\n",
        "    (\"Track 2 (RL Closed-Loop Agent)\", res_b2),\n",
        "])\n"
    ]

    # 6. Update Cell 13 (Trajectory Visualization)
    nb["cells"][13]["source"] = [
        "# Step 6: Generate Dual Trajectory Overlay & Dynamic Convergence Curves\n",
        "# ==============================================================================\n",
        "# [DO NOT MODIFY - Canonical Diagnostic Visualization]\n",
        "# ==============================================================================\n",
        "fig = plot_benchmark_trajectories(\n",
        "    env,\n",
        "    controllers={\n",
        "        \"Linear SVD\": b0,\n",
        "        \"Supervised MLP\": b1,\n",
        "        \"RL Agent\": b2,\n",
        "        \"Bayesian Opt\": b3\n",
        "    },\n",
        "    seed=42,\n",
        "    save_path=\"img/benchmark_trajectories.png\",\n",
        "    show=True\n",
        ")\n"
    ]

    # 7. Update Cell 15 (Final Team Showcase)
    nb["cells"][15]["source"] = [
        "# Step 7: Final Team Showcase Presentation Summary\n",
        "# ==============================================================================\n",
        "# [DO NOT MODIFY - Automated Showcase Scorecard for Presentation]\n",
        "# ==============================================================================\n",
        "best_agent_name, best_metrics = max(\n",
        "    [(\"Track 3 (Bayesian Optimization)\", res_b3),\n",
        "     (\"Track 2 (RL Closed-Loop Agent)\", res_b2),\n",
        "     (\"Baseline 1 (Supervised MLP)\", res_b1),\n",
        "     (\"Baseline 0 (Linear SVD)\", res_b0)],\n",
        "    key=lambda item: item[1][\"score\"]\n",
        ")\n",
        "\n",
        "print(\"=\" * 68)\n",
        "print(f\"   TEAM: {TEAM_NAME} — OFFICIAL HACKATHON BENCHMARK SUBMISSION\")\n",
        "print(\"=\" * 68)\n",
        "print(f\"  • Best Performing Agent  : {best_agent_name}\")\n",
        "print(f\"  • Official Total Score   : {best_metrics['score']:.1f} points\")\n",
        "print(f\"  • Alignment Success Rate : {best_metrics['success_rate']:.1f}%\")\n",
        "print(f\"  • Mean Steps to Target   : {best_metrics['mean_steps']:.1f} steps\")\n",
        "print(f\"  • Mean Residual Orbit RMS: {best_metrics['mean_rms']:.4f} mm\")\n",
        "print(f\"  • Mean Corrector Norm    : {best_metrics['mean_norm']:.2f} A\")\n",
        "print(f\"  • Mean Policy Latency    : {best_metrics['mean_latency']:.2f} ms\")\n",
        "print(\"=\" * 68)\n"
    ]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    print("Updated Solution notebook successfully!")

if __name__ == "__main__":
    update_participant_notebook()
    update_solution_notebook()
