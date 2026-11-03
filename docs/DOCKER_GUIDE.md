# 🐳 Docker Environment Guide — AI Applications in Accelerators Mini-Hackathon

This guide explains system requirements, terminal options across operating systems, and how to use, run, and publish the containerized environment for the **AI Applications in Accelerators Tutorial & Mini-Hackathon** (KOMAC / KAERI).

---

## 📋 System Requirements & Supported Terminals

### Do participants need PowerShell?
**No, PowerShell is NOT mandatory.** Participants can use **any terminal** of their choice on Windows, macOS, or Linux. 

With **Docker Compose**, the launch command is identical across all operating systems and shells:
```bash
docker compose up
```

| Operating System | Supported Terminals | Path Syntax for `-v` (CLI only) |
| :--- | :--- | :--- |
| **Windows** | **PowerShell** | `-v "${PWD}/notebooks:/workspace/notebooks"` |
| **Windows** | **Command Prompt (`cmd.exe`)** | `-v "%cd%\notebooks:/workspace/notebooks"` |
| **Windows** | **Git Bash** | `-v "/$(pwd)/notebooks:/workspace/notebooks"` |
| **Windows** | **WSL 2 (Ubuntu)** | `-v "${PWD}/notebooks:/workspace/notebooks"` |
| **macOS** | **Terminal / iTerm2 (zsh / bash)** | `-v "${PWD}/notebooks:/workspace/notebooks"` |
| **Linux** | **Bash / Zsh / Any terminal** | `-v "${PWD}/notebooks:/workspace/notebooks"` |

> [!TIP]
> If participants run **`docker compose up`**, they don't have to worry about shell-specific path syntax (`${PWD}` vs `%cd%`) at all—Docker Compose handles path resolution natively on every OS!

---

### Prerequisites for Participants

1. **Docker Runtime:**
   - **Windows / macOS:** Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) (ensure it is running before opening the terminal).
     - *Windows note:* Docker Desktop requires **WSL 2 backend** (installed automatically by modern Docker Desktop installers).
   - **Linux:** Install `docker.io` and `docker-compose-plugin` (or Docker Engine).
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
| **Local Build** | `ai4acc-hackathon:latest` | Local host machine | Available only on the machine where it was built |
| **Docker Hub Registry** | `<username>/ai4acc-hackathon:latest` | Public / Private Cloud Registry (`hub.docker.com`) | Available worldwide via `docker pull` |

> [!NOTE]
> By default, `ai4acc-hackathon` is a **locally built image**. It is not automatically uploaded to Docker Hub. If organizers wish to distribute a pre-built image to participants without requiring them to build it locally, see [Section 4: Publishing to Docker Hub](#-4-publishing-to-docker-hub-for-organizers).

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
docker build -t ai4acc-hackathon .
```

### Step 2: Run the Container

#### Option A: Standalone Container (All files baked in)
The image already contains all source code, lecture notes, and challenge notebooks internally:
```bash
docker run -it --rm -p 8888:8888 ai4acc-hackathon
```

#### Option B: Live Volume Mounting (Saves edits to host machine)
To ensure any code or notebook edits made inside Jupyter persist directly into your local host files, mount the `notebooks` and `src` directories:

```bash
docker run -it --rm \
  -p 8888:8888 \
  -v "${PWD}/notebooks:/workspace/notebooks" \
  -v "${PWD}/src:/workspace/src" \
  ai4acc-hackathon
```

> [!IMPORTANT]
> Always execute the command from the repository root directory. If run from another folder, `${PWD}/notebooks` will point to a non-existent host path, causing Docker to mount an empty directory.

---

## 🌐 3. Connecting to Jupyter

1. Open your browser and navigate to:
   - **`http://localhost:8888`** (or `http://localhost:8889` if using port 8889)
2. Token authentication is disabled by default in the container configuration (`--ServerApp.token=''`) for a friction-free hackathon setup.
3. Open [`notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb`](file:///home/cspark/Work/projects/ai4acc-mini-hackathon/notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb) to begin the challenge.

---

## 📤 4. Publishing to Docker Hub (For Organizers)

If workshop organizers wish to distribute a pre-compiled image so attendees can skip the local build step:

### Step 1: Sign Up / Log In to Docker Hub
Ensure you have an account on [Docker Hub](https://hub.docker.com). In your terminal, authenticate:
```bash
docker login
```
*(Enter your Docker Hub username and personal access token / password)*.

### Step 2: Tag the Local Image
Tag the local `ai4acc-hackathon` image with your Docker Hub account namespace:
```bash
# Format: docker tag <local-image> <dockerhub-username>/<repo-name>:<tag>
docker tag ai4acc-hackathon <your-username>/ai4acc-hackathon:latest
```

*Example for user `kaeri-acc`:*
```bash
docker tag ai4acc-hackathon kaeri-acc/ai4acc-hackathon:latest
```

### Step 3: Push to Docker Hub
```bash
docker push <your-username>/ai4acc-hackathon:latest
```

### Step 4: Participant Usage from Docker Hub
Once pushed, participants do not need to clone the repo or build the image. They can simply run:
```bash
docker run -it --rm \
  -p 8888:8888 \
  -v "${PWD}/notebooks:/workspace/notebooks" \
  -v "${PWD}/src:/workspace/src" \
  <your-username>/ai4acc-hackathon:latest
```

---

## 🛠️ 5. Troubleshooting & Common Issues

### Issue 1: `failed to bind host port 0.0.0.0:8888/tcp: address already in use`
- **Cause:** Another process on your host machine (such as a local Jupyter server or another Docker container) is already listening on port `8888`.
- **Fix 1 (Map to another port, e.g., 8889):**
  ```bash
  docker run -it --rm -p 8889:8888 -v "${PWD}/notebooks:/workspace/notebooks" -v "${PWD}/src:/workspace/src" ai4acc-hackathon
  ```
  Then access Jupyter at **`http://localhost:8889`**.
- **Fix 2 (Stop the host process):**
  ```bash
  # Find PID using port 8888 and stop it
  kill $(lsof -t -i:8888)
  ```

---

### Issue 2: `bash: -v: command not found` or `invalid reference format`
- **Cause:** A trailing whitespace immediately after a line-continuation backslash (`\ `) in your shell command.
- **Fix:** Avoid spaces after backslashes, or run the command on a single contiguous line:
  ```bash
  docker run -it --rm -p 8888:8888 -v "${PWD}/notebooks:/workspace/notebooks" -v "${PWD}/src:/workspace/src" ai4acc-hackathon
  ```

---

### Issue 3: `notebooks` or `src` Directory Appears Empty in Jupyter
- **Cause:** The `docker run` command was executed from outside the project root directory (e.g. from `~`), causing `${PWD}/notebooks` to evaluate to an empty path on the host that shadowed the container's built-in files.
- **Fix:** Ensure you `cd` into the project root before running, or use absolute paths:
  ```bash
  cd /home/cspark/Work/projects/ai4acc-mini-hackathon
  docker compose up
  ```

---

### Issue 4: Weights & Biases (W&B) Logging Inside Docker
To pass your Weights & Biases credentials into the container:
```bash
docker run -it --rm \
  -p 8888:8888 \
  -e WANDB_API_KEY="<your-wandb-api-key>" \
  -v "${PWD}/notebooks:/workspace/notebooks" \
  ai4acc-hackathon
```
Or simply run `wandb login` in the first cell of the notebook.
