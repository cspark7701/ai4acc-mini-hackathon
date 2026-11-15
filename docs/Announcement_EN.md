# 📢 AI Tutorial Session for Accelerators & Mini-Hackathon

---

## 🌟 Workshop Overview

We cordially invite researchers, engineers, postdoctoral scholars, and graduate students to the **AI Tutorial Session for Accelerators & Mini-Hackathon**!

This intensive, full-day educational session and competition bridges cutting-edge Artificial Intelligence (AI) and Machine Learning (ML) techniques with physical beam dynamics, closed-loop accelerator orbit correction, and agentic autonomous operational workflows.

- **Date & Time:** Thursday, November 19, 2026 | 09:00 – 17:00 KST
- **Location:** KOMAC / KAERI (Korea Multi-purpose Accelerator Complex / Korea Atomic Energy Research Institute)
- **Registration (Indico):** [https://indico.korea.ac.kr/event/114/](https://indico.korea.ac.kr/event/114/)
- **Target Audience:** Undergraduate and graduate students, postdocs in accelerator physics and technologies
- **Distinguished Instructors:**
  - **Chong Shik Park, Ph.D.** — Korea University, Sejong
  - **Thorsten Hellert, Ph.D.** — Lawrence Berkeley National Laboratory (LBNL) / Osprey Project Team

---

## 🕒 Master Program Schedule

| Time (KST)        | Session Type          | Details & Lecturers                                                                                                                                                                                                                                           |
|:-----------------:|:---------------------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **09:00 – 09:10** | Welcome & Orientation | Opening remarks, workshop objectives, setup verification & W&B intro                                                                                                                                                                                          |
| **09:10 – 10:30** | **Lecture 1**         | **AI/ML Foundations and Closed-Loop Control for Particle Accelerators**<br>Lecturer: Chong Shik Park, Ph.D. (Korea University, Sejong)                                                                                                                        |
| **10:30 – 10:40** | Break & Discussion    | Intermission and Q&A                                                                                                                                                                                                                                          |
| **10:40 – 12:00** | **Lecture 2**         | **Agentic AI for Accelerator Research: Osprey Applications**<br>Lecturer: Thorsten Hellert, Ph.D.                                                                                                                                                             |
| **12:00 – 13:30** | Lunch & Networking    | Complimentary lunch and attendee collaboration                                                                                                                                                                                                                |
| **13:30 – 16:30** | **Mini-Hackathon**    | **Beam Orbit Alignment Benchmark Challenge**<br>• Track 1: Supervised Neural Surrogate (MLP) Inverse Optimization<br>• Track 2: Physics-Informed Closed-Loop Reinforcement Learning (RL)<br>• Track 3: Gaussian Process Bayesian Optimization (BO) Controller |
| **16:30 – 17:00** | Leaderboard Awards    | W&B Live Leaderboard review, awards presentation & closing remarks                                                                                                                                                                                            |

---

## 💻 Participant Preparation & Hardware Requirements

To guarantee a seamless and productive hands-on experience, please review the following requirements prior to attending:

### 1. Bring Your Own Laptop (BYOD)

- All participants are requested to **bring their personal laptop and power adapter** for the morning tutorials and the afternoon hackathon.
- High-speed venue Wi-Fi connectivity will be provided.

### 2. Operating Systems & Docker Desktop Setup Instructions (Windows, macOS, Linux)

- You are welcome to use **any operating system: Windows, macOS, or Linux**.
- Hands-on exercises and challenge environments are packaged using Docker for consistent and reproducible execution. Please prepare your system before attending:

#### 🪟 Windows Users (Docker Desktop + WSL 2):

1. Download and install Docker Desktop from the [official website](https://www.docker.com/products/docker-desktop/).
2. **Enable WSL 2 (Windows Subsystem for Linux):**
   - Open PowerShell or Command Prompt as Administrator and run:
     
     ```powershell
     wsl --install
     ```
     
     *(If WSL is already installed, execute `wsl --update`)*
   - In Docker Desktop Settings $\rightarrow$ General, verify that **"Use the WSL 2 based engine"** is checked.
3. Restart your computer if prompted, and ensure Docker Desktop is running before the workshop.

#### 🍎 Mac (macOS) Users:

1. Download and install Docker Desktop from the [official website](https://www.docker.com/products/docker-desktop/) selecting the installer matching your hardware (Apple Silicon for M1/M2/M3/M4 or Intel chip).
2. Launch Docker Desktop and complete initial system permission grants.

#### 🐧 Linux Users (Ubuntu/Debian & CentOS/RHEL):

- No GUI app is required. Install Docker Engine and the Docker Compose plugin via your distribution's package manager:
  - **Ubuntu / Debian:**
    
    ```bash
    sudo apt update && sudo apt install -y docker.io docker-compose-plugin
    sudo systemctl enable --now docker
    sudo usermod -aG docker $USER
    ```
  - **CentOS / RHEL (Red Hat Enterprise Linux) / Rocky Linux:**
    
    ```bash
    sudo dnf install -y yum-utils
    sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    sudo systemctl enable --now docker
    sudo usermod -aG docker $USER
    ```
    
    *(Note: Log out and log back in after adding your user to the docker group for changes to take effect).*

- **Official Hackathon Docker Container Launch:**
  - **Windows (Double-Click):** Simply **double-click** `run_hackathon_windows.bat`. It will automatically check your Docker Desktop engine and launch the environment.
  - **macOS / Linux:** Run `./run_hackathon_mac_linux.sh` in your terminal.
  - **Direct Terminal Command:**
    ```bash
    docker run -it --rm -p 127.0.0.1:8888:8888 cspark7701/ai4acc-hackathon-2026:latest
    ```
  *(After launching via the script or command, open your web browser and browse to `http://localhost:8888` to begin).*

### 3. Weights & Biases (W&B) Live Leaderboard (No Account Needed)

- The hackathon utilizes **Weights & Biases (W&B)** for real-time experiment tracking, telemetry visualization, and the live competition leaderboard.
- **You do not need a W&B account or API key.** The launchers handed out on the day (`run_hackathon_windows.bat` / `run_hackathon_mac_linux.sh`) pass the workshop's shared key file (`wandb.apikey`) to the container automatically, so your benchmark results go straight to the leaderboard.
- Keep `wandb.apikey` in the **same folder** as the launcher, and please do not share it outside the workshop.
- Each team chooses a **unique team name** on the day and enters it as `TEAM_NAME` in the notebook. The leaderboard is shown live on the room display. *(Without network access you can still run the benchmark and see your score locally.)*

---

## ✅ Pre-Workshop Readiness Checklist

- [ ] Workshop registration completed on Indico ([https://indico.korea.ac.kr/event/114/](https://indico.korea.ac.kr/event/114/))
- [ ] Personal laptop and power adapter ready
- [ ] Docker Desktop installed and verified running (Windows: WSL 2 enabled, macOS: app launched) or Linux Docker Engine ready
- [ ] A hackathon team name in mind (no W&B account is needed)
