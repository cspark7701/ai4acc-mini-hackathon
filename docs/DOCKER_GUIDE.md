# 🐳 Docker Environment Guide — AI Applications in Accelerators Mini-Hackathon

This guide explains system requirements, terminal options across operating systems, and how to use, run, and publish the containerized environment for the **AI Applications in Accelerators Tutorial & Mini-Hackathon** (KOMAC / KAERI).

---

## 📋 System Requirements & Supported Terminals

### Do participants need PowerShell?
**No, PowerShell is NOT mandatory.** Participants can use **any terminal** of their choice on Windows, macOS, or Linux. 

Because all required libraries, simulation models, and the participant challenge notebook are baked into the pre-compiled image, the launch command is identical and universal across all operating systems and shells:
```bash
docker run -it --rm -p 8888:8888 cspark7701/ai4acc-hackathon-2026:latest
```

| Operating System | Supported Terminals | Launch Command |
| :--- | :--- | :--- |
| **Windows** | **Command Prompt (`cmd.exe`)** | `docker run -it --rm -p 8888:8888 cspark7701/ai4acc-hackathon-2026:latest` |
| **Windows** | **PowerShell** | `docker run -it --rm -p 8888:8888 cspark7701/ai4acc-hackathon-2026:latest` |
| **Windows** | **Git Bash / WSL 2** | `docker run -it --rm -p 8888:8888 cspark7701/ai4acc-hackathon-2026:latest` |
| **macOS** | **Terminal / iTerm2 (zsh / bash)** | `docker run -it --rm -p 8888:8888 cspark7701/ai4acc-hackathon-2026:latest` |
| **Linux** | **Bash / Zsh / Any terminal** | `docker run -it --rm -p 8888:8888 cspark7701/ai4acc-hackathon-2026:latest` |

> [!TIP]
> **Zero Setup Required:** Attendees do not need to clone the git repository, configure local Python virtual environments, or worry about shell-specific volume mount path syntax. Once the container is running, open **`http://localhost:8888`** in your browser.

---

### Prerequisites for Participants

1. **Docker Runtime:**
   - **Windows / macOS:** Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) (ensure it is running before opening the terminal).
     - *Windows note:* Docker Desktop requires **WSL 2 backend** (installed automatically by modern Docker Desktop installers).
   - **Linux:** Install Docker Engine and the Docker Compose plugin (Ubuntu/Debian: `sudo apt install docker.io docker-compose-plugin`; CentOS/RHEL: `sudo dnf install docker-ce docker-compose-plugin`). Ensure service is running via `sudo systemctl enable --now docker`.
2. **Web Browser:**
   - Any modern browser (Google Chrome, Microsoft Edge, Mozilla Firefox, Safari) to interact with JupyterLab at `http://localhost:8888`.
3. **Hardware Specifications:**
   - **RAM:** Minimum 4 GB (8 GB or more recommended).
   - **Storage:** ~2.5 GB free disk space (base image + dependencies).
   - **Architecture:** Works on both x86_64 (Intel/AMD) and ARM64 (Apple Silicon M1/M2/M3/M4).
4. **Weights & Biases Account (Optional but recommended):**
   - Free account at [wandb.ai](https://wandb.ai) to submit scores to the live leaderboard.

---

## 🧭 Overview: Local Image vs. Docker Hub

When you build the container using the provided [`Dockerfile`](file:///home/cspark/Work/projects/ai4acc-mini-hackathon/Dockerfile):

| Environment | Image Name | Storage Location | Accessibility |
| :--- | :--- | :--- | :--- |
| **Local Build** | `ai4acc-hackathon-2026:latest` | Local host machine | Available only on the machine where it was built |
| **Docker Hub Registry** | `<username>/ai4acc-hackathon-2026:latest` | Public / Private Cloud Registry (`hub.docker.com`) | Available worldwide via `docker pull` |

> [!NOTE]
> By default, `ai4acc-hackathon-2026` is a **locally built image**. It is not automatically uploaded to Docker Hub. If organizers wish to distribute a pre-built image to participants without requiring them to build it locally, see [Section 4: Publishing to Docker Hub](#-4-publishing-to-docker-hub-for-organizers).

---

## 🚀 1. Quickstart with Docker Compose (Recommended)

Docker Compose is the simplest and least error-prone method because [`docker-compose.yml`](file:///home/cspark/Work/projects/ai4acc-mini-hackathon/docker-compose.yml) automatically anchors all paths to the repository directory.

From the project root directory:

```bash
cd /home/cspark/Work/projects/ai4acc-mini-hackathon

# Build image and start Jupyter Lab
docker compose up
```

- To run in the background as a daemon:
  ```bash
  docker compose up -d
  ```
- To stop the container:
  ```bash
  docker compose down
  ```

Once started, open your web browser to **`http://localhost:8888`**.

---

## 💻 2. Running with the Docker CLI

### Step 1: Build the Image Locally
```bash
cd /home/cspark/Work/projects/ai4acc-mini-hackathon
docker build -t ai4acc-hackathon-2026 .
```

### Step 2: Run the Official Challenge Container

Run the official container directly in your terminal:
```bash
docker run -it --rm -p 8888:8888 cspark7701/ai4acc-hackathon-2026:latest
```

> [!NOTE]
> The pre-compiled image contains all dependencies, simulation models, and the participant challenge notebook (`Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb`). The reference solution notebook is completely excluded to protect competition integrity.
>
> *(Participants can save their notebook inside JupyterLab and download a local copy at any time via **File → Download**).*

---

## 🌐 3. Connecting to Jupyter

1. Open your browser and navigate to:
   - **`http://localhost:8888`** (or `http://localhost:8889` if using port 8889)
2. Token authentication is disabled by default in the container configuration (`--ServerApp.token=''`) for a friction-free hackathon setup.
3. Open [`notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb`](file:///home/cspark/Work/projects/ai4acc-mini-hackathon/notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb) to begin the challenge.

---

## 📤 4. Publishing to Docker Hub (For Organizers)

If workshop organizers wish to distribute a pre-compiled image so attendees can skip the local build step:

> [!TIP]
> **One-Command Automated Publishing Script:**
> An automated publishing script is provided at [`scripts/docker_publish.sh`](file:///home/cspark/Work/projects/ai4acc-mini-hackathon/scripts/docker_publish.sh). It handles pre-flight Docker checks, solution privacy verification, multi-arch builds (`linux/amd64` + `linux/arm64` by default), authentication, and publishing:
> ```bash
> # Interactive mode (prompts for username, uses 'latest' tag and multi-arch by default):
> ./scripts/docker_publish.sh
> 
> # Or specify parameters:
> ./scripts/docker_publish.sh <your-username> latest [--single-arch]
> ```

### Step 1: Build the Image Locally
From the repository root directory, build the challenge image (the reference solution notebook is automatically excluded via `.dockerignore`):
```bash
docker build -t ai4acc-hackathon-2026 .
```
*(Alternatively, you can build directly with your target Docker Hub namespace:)*
```bash
docker build -t <your-username>/ai4acc-hackathon-2026:latest .
```

> [!TIP]
> **Multi-Architecture Support (Intel/AMD + Apple Silicon):**
> Workshop participants may use either x86_64 (Windows/Linux/Intel Mac) or ARM64 (Apple Silicon M1/M2/M3/M4). To build and push a unified multi-platform manifest directly to Docker Hub:
> ```bash
> docker buildx build --platform linux/amd64,linux/arm64 -t <your-username>/ai4acc-hackathon-2026:latest --push .
> ```

### Step 2: Sign Up / Log In to Docker Hub
Ensure you have an account on [Docker Hub](https://hub.docker.com). In your terminal, authenticate:
```bash
docker login
```
*(Enter your Docker Hub username and personal access token / password)*.

### Step 3: Tag the Local Image
If you built the image locally as `ai4acc-hackathon-2026`, tag it with your Docker Hub account namespace:
```bash
# Format: docker tag <local-image> <dockerhub-username>/<repo-name>:<tag>
docker tag ai4acc-hackathon-2026 <your-username>/ai4acc-hackathon-2026:latest
```

### Step 4: Push to Docker Hub
```bash
docker push <your-username>/ai4acc-hackathon-2026:latest
```

### Step 5: Participant Usage from Docker Hub
Once pushed, participants do not need to clone the repo or build the image. They can simply run:
```bash
docker run -it --rm -p 8888:8888 cspark7701/ai4acc-hackathon-2026:latest
```

---

## 🛠️ 5. Troubleshooting & Common Issues

### Issue 1: `failed to bind host port 0.0.0.0:8888/tcp: address already in use`
- **Cause:** Another process on your host machine (such as a local Jupyter server or another Docker container) is already listening on port `8888`.
- **Fix 1 (Map to another port, e.g., 8889):**
  ```bash
  docker run -it --rm -p 8889:8888 cspark7701/ai4acc-hackathon-2026:latest
  ```
  Then access Jupyter at **`http://localhost:8889`**.
- **Fix 2 (Stop the host process):**
  ```bash
  # Find PID using port 8888 and stop it
  kill $(lsof -t -i:8888)
  ```

---

### Issue 2: Saving Your Work from the Container
- **Download from Browser:** In the JupyterLab file browser, simply right-click `Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb` and select **Download** (or use **File → Download**).
- **Weights & Biases (W&B):** When you run the evaluation benchmark cells, your challenge scores, telemetry, and figures are automatically and permanently logged to your W&B cloud dashboard.

---

### Issue 3: Weights & Biases (W&B) Logging Inside Docker
To pass your Weights & Biases credentials into the container at launch:
```bash
docker run -it --rm \
  -p 8888:8888 \
  -e WANDB_API_KEY="<your-wandb-api-key>" \
  cspark7701/ai4acc-hackathon-2026:latest
```
Or simply run `wandb.login()` in the first cell of the notebook.
