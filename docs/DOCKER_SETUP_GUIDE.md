# To Do Before the Workshop 📋 — Docker Setup Guide

This guide prepares your laptop for the **AI Applications in Accelerators Tutorial &
Mini-Hackathon**. The whole challenge runs inside Docker, so you do not have to install
Python or any library yourself.

Please finish steps 1 to 3 **before the workshop**. They need a good network connection
and take 15 to 30 minutes.

| You need | Details |
| --- | --- |
| Free disk space | About 3 GB (Docker itself plus the ~1.2 GB challenge image) |
| Memory | 4 GB minimum, 8 GB recommended |
| Processor | 64-bit Intel/AMD or ARM64 (Apple Silicon) |
| Web browser | Chrome, Edge, Firefox or Safari |
| W&B account | **Not needed.** Scores are submitted with a shared key handed out on the day |

---

## 1. Install Docker 🐳

Follow **[`DOCKER_INSTALL_GUIDE.md`](DOCKER_INSTALL_GUIDE.md)** for your operating system
(Linux, macOS or Windows). Come back here once `docker --version` prints a version number
and Docker is running.

---

## 2. Download the challenge image

Downloading the image in advance saves time and venue Wi-Fi on the day. With Docker
running, type this in any terminal (PowerShell, Command Prompt, Terminal, Bash):

```bash
docker pull cspark7701/ai4acc-hackathon-2026:latest
```

The image contains Python 3.12, JupyterLab, the beamline simulation, all required
libraries, the participant notebook and the lecture PDFs. You do not need to clone the
git repository.

If you cannot download it beforehand, the organizer's bundle includes an offline copy
(`ai4acc-image.tar.gz`) that the launcher loads automatically.

---

## 3. Test that everything runs

### Start the container

With Docker running (Linux: `sudo systemctl start docker`; macOS with Colima:
`colima start`; Windows and macOS with Docker Desktop: open the app), run:

```bash
docker run -it --rm -p 8888:8888 cspark7701/ai4acc-hackathon-2026:latest
```

The command is the same on every operating system and in every terminal.

### Open the notebook

1. Open **[http://localhost:8888/lab](http://localhost:8888/lab)** in your web browser.
   No password or token is required.
2. In the file browser on the left, open
   `Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb`.
3. Run the first cell with the library imports. If it finishes without an error, your
   laptop is ready. 🎉

Scores are not sent to the leaderboard during this test, because the shared key is only
handed out at the workshop. The notebook reports them locally instead.

### Stop the container

Press `Ctrl+C` in the terminal where the container is running. Then, if you like, stop
the Docker engine:

| System | Command |
| --- | --- |
| Linux | `sudo systemctl stop docker` |
| macOS with Colima | `colima stop` |
| Windows / macOS with Docker Desktop | Quit the Docker Desktop app |

### Monitor memory use

To watch the container's memory and CPU use in real time, type this in a second terminal:

```bash
docker stats
```

---

## 4. On the day of the workshop

You will receive a folder from the organizer containing:

| File | Purpose |
| --- | --- |
| `run_hackathon_windows.bat` | Launcher for Windows (double-click) |
| `run_hackathon_mac_linux.sh` | Launcher for macOS and Linux |
| `wandb.apikey` | Shared key that submits your scores to the live leaderboard |
| `ai4acc-image.tar.gz` | Offline copy of the challenge image |

Keep all files **together in the same folder**. Do not open, edit or share `wandb.apikey`.

Start the environment with the launcher, not with the `docker run` command from step 3:

- **Windows:** double-click `run_hackathon_windows.bat`.
- **macOS / Linux:** open a terminal in the folder and run `./run_hackathon_mac_linux.sh`.

The launcher checks that Docker is running, loads the offline image if needed, passes the
leaderboard key to the container, and opens JupyterLab in your browser. It prints
`[OK] W&B leaderboard key loaded.` when it finds the key.

In the notebook's configuration cell, change only `TEAM_NAME` to your registered team
name. See [`WANDB_LEADERBOARD_GUIDE.md`](WANDB_LEADERBOARD_GUIDE.md) for details.

**Save your work:** files inside the container are deleted when it stops. Before you
stop it, download your notebook from JupyterLab with **File → Download**.

---

## Troubleshooting

- **`docker: command not found`:** Docker is not installed, or the terminal was opened
  before the installation finished. Open a new terminal, or restart your computer.
- **`Cannot connect to the Docker daemon`:** the Docker engine is not running. Start
  Docker Desktop, run `colima start`, or run `sudo systemctl start docker`.
- **`permission denied` on Linux:** your user is not in the `docker` group. Run
  `sudo usermod -aG docker $USER`, then log out and back in.
- **`address already in use` for port 8888:** another program, often a local Jupyter
  server, is using the port. Use port 8889 instead and open `http://localhost:8889/lab`:

  ```bash
  docker run -it --rm -p 8889:8888 cspark7701/ai4acc-hackathon-2026:latest
  ```

- **`[!] No W&B key found` from the launcher:** `wandb.apikey` is not in the same folder
  as the launcher. Copy it there and start the launcher again.
- **The browser does not open by itself:** open `http://localhost:8888/lab` manually.

For Docker Compose, building the image yourself and publishing it, see
[`DOCKER_GUIDE.md`](DOCKER_GUIDE.md).

---

## Alternative installation for experienced practitioners 👩🏾‍💻

If you regularly code in Python and are used to virtual environments, you can run
everything locally instead. **You need Python 3.9 or higher** and should be ready to debug
your own installation.

```bash
git clone https://github.com/cspark7701/ai4acc-mini-hackathon.git
cd ai4acc-mini-hackathon
source setup.sh
jupyter lab
```

`setup.sh` creates a virtual environment named `ai4acc`, installs the package with its
development tools, and activates it. On Windows, run it from Git Bash or WSL.

A local installation does not receive the shared leaderboard key from the launcher. To
submit scores, set it yourself before starting Jupyter, using the `wandb.apikey` file you
receive at the workshop:

```bash
export WANDB_API_KEY="$(cat /path/to/wandb.apikey)"
```
