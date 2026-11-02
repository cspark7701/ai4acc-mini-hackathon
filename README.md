# AI Applications in Accelerators: Tutorial & Mini-Hackathon

Welcome to the **AI Applications in Accelerators Tutorial & Mini-Hackathon** repository. This project hosts the computational challenge, simulation environment, benchmark notebooks, and documentation for the hands-on mini-hackathon held at the **Korea Multi-purpose Accelerator Complex (KOMAC) / Korea Atomic Energy Research Institute (KAERI)**.

---

## 📋 Table of Contents

- [Overview](#overview)
- [The Challenge: Beam Orbit Alignment Benchmark](#the-challenge-beam-orbit-alignment-benchmark)
- [Master Schedule & Program](#master-schedule--program)
- [Repository Structure](#repository-structure)
- [Getting Started & Environment Setup](#getting-started--environment-setup)
  - [Option A: Local Python / Conda](#option-a-local-python--conda)
  - [Option B: Google Colab](#option-b-google-colab)
  - [Option C: Docker Container (Offline Contingency)](#option-c-docker-container-offline-contingency)
- [Weights & Biases (W&B) Leaderboard](#weights--biases-wb-leaderboard)
- [Benchmark Results & Scoring](#benchmark-results--scoring)
- [Participant Workflow & Instructions](#participant-workflow--instructions)
- [Documentation Index](#documentation-index)

---

## 🎯 Overview

Modern particle accelerators rely increasingly on machine learning and autonomous agentic workflows to handle high-dimensional, non-linear, and time-critical beam control tasks. This tutorial bridges theoretical foundations with real-time operational applications:

- **Morning Lectures:**
  - **Lecture 1:** *AI/ML Fundamentals, Neural Networks & Surrogate Modeling for Accelerators* — **Chong Shik Park**
  - **Lecture 2:** *Agentic AI, LLM Tools & Osprey Applications in Accelerator Research* — **Thorsten Hellert**
- **Afternoon Mini-Hackathon:**
  - Hands-on closed-loop control challenge in a standardized [Gymnasium](https://gymnasium.farama.org/) environment.
  - Multi-track benchmarking: Classical Linear ORM, Supervised Neural Surrogate Inversion, and Closed-Loop Reinforcement Learning / Adaptive Policies.
  - Live real-time scoring streamed to a unified [Weights & Biases (W&B)](https://wandb.ai) leaderboard.

---

## 🔬 The Challenge: Beam Orbit Alignment Benchmark

Participants design, optimize, and benchmark closed-loop accelerator controllers to steer an off-axis particle beam back to nominal alignment within an optical transport lattice.

```
       +-----------------------------------------------------------------+
       |               ACCELERATOR BEAM TRANSPORT SECTION                |
Beam ->| [BPM1]--[HCM1]--[QF1]--[BPM2]--...--[VCM3]--[QD3]--[BPM12]       |-> Target
       +-----------------------------------------------------------------+
          Diagnostics: 12 BPMs            Actuators: 6 Correctors (3H/3V)
```

### Physical Lattice & Hardware Specification
- **Actuators ($X$):** 6 dipole steering magnets (3 Horizontal `HCM1-3`, 3 Vertical `VCM1-3`).
  - Total Current Range: $[-5.0\text{ A}, +5.0\text{ A}]$
  - Step Action Range ($\Delta I$): $[-0.8\text{ A}, +0.8\text{ A}]$
- **Diagnostics ($Y$):** 12 Beam Position Monitors (BPMs) positioned along a 15-meter transport line measuring beam offset in millimeters (mm).
- **Optics & Non-linearities:**
  - Alternating quadrupole focusing/defocusing magnets (`QF`, `QD`).
  - Core linear Orbit Response Matrix (ORM) derived from standard accelerator transfer matrices:
    $$R_{ij} = \frac{\sqrt{\beta_i \beta_j}}{2 \sin(\pi \nu)} \cos(|\psi_i - \psi_j| - \pi \nu)$$
  - Non-linear magnetic core saturation: $-0.015 \cdot X^3 \cdot R$
  - Realistic Gaussian diagnostic noise: $\epsilon \sim \mathcal{N}(0, 0.010\text{ mm})$
- **Goal Condition:** Bring Root-Mean-Square (RMS) beam orbit error below threshold:
  $$\text{RMS} = \sqrt{\frac{1}{12}\sum_{i=1}^{12} Y_i^2} < 0.030\text{ mm}$$
  within a budget of **20 control steps**.

---

## ⏱️ Master Schedule & Program

| Time | Session Phase | Speaker / Facilitator | Core Focus |
| :--- | :--- | :--- | :--- |
| **09:00 – 09:10** | Opening Remarks | Workshop Organizers | Welcome & learning goals |
| **09:10 – 10:30** | **Lecture 1** (Extended) | **Chong Shik Park** | AI/ML fundamentals, neural networks & surrogate modeling |
| **10:30 – 10:40** | Coffee & Networking | Attendees | Mid-morning recess |
| **10:40 – 12:00** | **Lecture 2** (Extended) | **Thorsten Hellert** | Agentic AI, LLM tools & Osprey in accelerator control |
| **12:00 – 13:30** | Lunch Break | Attendees | Lunch & informal discussion |
| **13:30 – 13:45** | Hackathon Kickoff | Technical Mentors | Environment verification & W&B login |
| **13:45 – 14:45** | Supervised Track | Participants | Train Ridge & MLP surrogate models; optimizer inversion |
| **14:45 – 15:45** | RL & Adaptive Track | Participants | Continuous feedback policy, gain & damping tuning |
| **15:45 – 16:30** | Live W&B Benchmarking | Participants | 30-seed benchmark evaluation, sync to live screen |
| **16:30 – 17:00** | Team Presentations & Showcase | All Teams | 3-minute lightning presentations & awards |

---

## 📂 Repository Structure

```
.
├── README.md                                         # Main workshop & challenge guide (this file)
├── AGENTS.md                                         # Operational instructions for AI assistants & agents
├── Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb  # Primary challenge notebook for participants (with TODOs)
├── Single_Notebook_Beam_Orbit_Predictor_Solution.ipynb     # Reference solutions and benchmark code
├── Single_Notebook_Beam_Orbit_Predictor.ipynb              # Master reference notebook
│
├── Technical Preparation.docx                        # Comprehensive tutorial readiness and curriculum guide
├── Hackathon Project Guide.docx                      # Full challenge rules, physics spec, and scoring breakdown
├── Mini-Hackathon Participant Instructions.docx       # Quick-reference participant milestone checklist
├── W&B Workspace Setup Guide.docx                    # Step-by-step W&B team and leaderboard setup guide
└── Docker Desktop Setup Guide.docx                   # Offline and container contingency deployment guide
```

---

## 🚀 Getting Started & Environment Setup

You can run the challenge notebooks using any of the following environments:

### Option A: Local Python / Conda

1. Create and activate a clean Python virtual environment (Python 3.10+ recommended):
   ```bash
   conda create -n ai4acc python=3.10 -y
   conda activate ai4acc
   ```

2. Install the necessary packages:
   ```bash
   pip install numpy scipy matplotlib scikit-learn gymnasium wandb jupyterlab
   ```

3. Launch Jupyter Lab and open the participant notebook:
   ```bash
   jupyter lab Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb
   ```

### Option B: Google Colab

1. Upload `Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb` to [Google Colab](https://colab.research.google.com/).
2. Run the first cell to install dependencies:
   ```python
   !pip install -q wandb gymnasium scikit-learn
   ```
3. Authenticate with your Weights & Biases account:
   ```python
   import wandb
   wandb.login()
   ```

### Option C: Docker Container (Offline Contingency)

If local Wi-Fi or software installation is restricted:
```bash
docker run -it --rm \
  -p 8888:8888 \
  -v "${PWD}:/home/jovyan/work" \
  -e JUPYTER_ENABLE_LAB=yes \
  quay.io/jupyter/scipy-notebook:latest
```
Access the Jupyter Lab interface in your browser at `http://localhost:8888`.

---

## 📊 Weights & Biases (W&B) Leaderboard

All evaluations automatically push telemetry and scoring to the live workshop leaderboard.

1. **Sign Up / Log In:** Create an account at [wandb.ai](https://wandb.ai).
2. **Retrieve API Key:** Obtain your personal API key from [wandb.ai/authorize](https://wandb.ai/authorize).
3. **Configure in Notebook:**
   ```python
   WANDB_PROJECT = "accelerator-orbit-hackathon"
   WANDB_ENTITY = "komac-ai-tutorial"  # Assigned workshop team entity (or leave None for personal)
   TEAM_NAME = "Team_01"               # Assigned team name
   ```
4. **Logged Telemetry:**
   - Summary scalar metrics: `challenge_score`, `success_rate_pct`, `mean_steps`, `mean_final_rms_mm`, `mean_current_norm_A`, `mean_latency_ms`.
   - Artifact table: `seed_breakdown_table` tracking individual seed outcomes across 30 standardized seeds.
   - Live dynamic convergence plots and dual orbit trajectory diagrams.

---

## 🏆 Benchmark Results & Scoring

### Official Scoring Formula

Controller performance is evaluated across **30 standardized test seeds** (`seeds=range(1, 31)`) using the official benchmark equation:

$$\text{Score} = (\text{Success Rate} \times 10.0) - (2.0 \times \overline{\text{Steps}}) + \left(\frac{0.03}{\max(\overline{\text{RMS}}, 0.005)} \times 20.0\right) - (2.0 \times \overline{\|\mathbf{I}\|})$$

- **$\text{Success Rate}$**: Percentage of seeds converging to $\text{RMS} < 0.03\text{ mm}$ (0 to 100%).
- **$\overline{\text{Steps}}$**: Mean iterations needed to converge (penalizes slow control).
- **$\overline{\text{RMS}}$**: Final alignment quality (rewards sub-micron accuracy).
- **$\overline{\|\mathbf{I}\|}$**: Euclidean norm of final corrector currents (penalizes magnet strain and saturation).

### Reference Benchmark Performance

| Rank | Controller / Agent Architecture | Success Rate | Mean Steps | Final RMS | Current Norm | Official Score |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 🥇 | **Baseline 1: Supervised MLP Surrogate Inversion** | 100.0% | **2.3 steps** | 0.0257 mm | 1.21 A | **1,016.8 pts** |
| 🥈 | **Baseline 0: Classical Linear SVD Controller** | 100.0% | 5.6 steps | **0.0230 mm** | **1.16 A** | **1,013.1 pts** |
| 🥉 | **Track 2: Closed-Loop RL / Adaptive Policy** | 100.0% | 6.1 steps | 0.0239 mm | 1.18 A | **1,011.1 pts** |

---

## 🛠️ Participant Workflow & Instructions

Follow these steps in [Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb](file:///home/cspark/Work/projects/ai4acc-mini-hackathon/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb):

1. **Step 0 & 1:** Run environment setup and visualize the accelerator lattice schematic.
2. **Step 2:** Instantiate the `AcceleratorOrbitGymEnv` simulation environment.
3. **Step 3 (TODO 1):** Train the forward surrogate models (Linear Ridge and Multi-Layer Perceptron) on offline beam data and inspect holdout RMSE.
4. **Step 4 (Baseline 0 & 1):** Test the classical SVD controller and the SciPy `L-BFGS-B` surrogate inversion controller.
5. **Step 4 (TODO 2 / Track 2):** Implement and tune your custom closed-loop policy agent:
   - Tune feedback gain $\alpha$, damping schedules, or neural residual offsets.
   - Adhere to the standard `act(obs, info) -> action` interface.
6. **Step 5:** Run `evaluate_hackathon_benchmark(...)` across all 30 evaluation seeds and inspect the live W&B run URL.
7. **Step 6 & 7:** Generate trajectory alignment plots and prepare your team's 3-minute showcase presentation.

---

## 📚 Documentation Index

For detailed guidelines, refer to the included guides:
- [Hackathon Project Guide (Word Document)](file:///home/cspark/Work/projects/ai4acc-mini-hackathon/Hackathon%20Project%20Guide.docx) — Complete rules, physics derivations, and scoring breakdown.
- [Technical Preparation Guide (Word Document)](file:///home/cspark/Work/projects/ai4acc-mini-hackathon/Technical%20Preparation.docx) — Detailed lecture syllabus, setup recommendations, and schedule.
- [Mini-Hackathon Participant Instructions (Word Document)](file:///home/cspark/Work/projects/ai4acc-mini-hackathon/Mini-Hackathon%20Participant%20Instructions.docx) — Quick participant checklist.
- [W&B Workspace Setup Guide (Word Document)](file:///home/cspark/Work/projects/ai4acc-mini-hackathon/W&B%20Workspace%20Setup%20Guide.docx) — Live dashboard and team administration guide.
- [Docker Desktop Setup Guide (Word Document)](file:///home/cspark/Work/projects/ai4acc-mini-hackathon/Docker%20Desktop%20Setup%20Guide.docx) — Containerized deployment instructions.
- [AGENTS.md](file:///home/cspark/Work/projects/ai4acc-mini-hackathon/AGENTS.md) — Operational instructions for AI coding assistants and autonomous agents.
