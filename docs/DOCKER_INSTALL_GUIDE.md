# Docker Installation Guide 🐳

This guide installs Docker on your laptop for the **AI Applications in Accelerators
Tutorial & Mini-Hackathon**. The challenge runs inside Docker, so this is the only
software you need to install.

Follow the section for your operating system, then continue with
[`DOCKER_SETUP_GUIDE.md`](DOCKER_SETUP_GUIDE.md) to download the challenge image and test it.

| You need | Details |
| --- | --- |
| Free disk space | About 3 GB (Docker itself plus the ~1.2 GB challenge image) |
| Memory | 4 GB minimum, 8 GB recommended |
| Processor | 64-bit Intel/AMD or ARM64 (Apple Silicon) |
| Docker account | **Not needed** |

---

## Linux

In your terminal, install Docker (Ubuntu / Debian):

```bash
sudo apt install docker.io docker-compose-v2
```

Allow your user to run Docker without `sudo`, then log out and back in:

```bash
sudo usermod -aG docker $USER
```

Verify your installation:

```bash
docker --version
docker compose version
```

## macOS

**Option A — Docker Desktop (simplest):** download and install Docker Desktop from
[https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/),
then start the app from your Applications folder.

**Option B — Docker with Colima (no Docker Desktop):** install both with `brew`:

```bash
brew install docker colima
```

The virtual machine created by Colima gets 2 CPUs and 2 GB of RAM by default. Give it
4 GB so the notebook does not run out of memory:

```bash
colima start --cpu 2 --memory 4
```

> **Note:** With Colima, `colima start` must be run before any Docker command works. It
> provides the container engine that Docker Desktop would otherwise supply.

Verify your installation (both options):

```bash
docker --version
docker compose version
```

## Windows

Docker on Windows requires WSL 2 (Windows Subsystem for Linux). Check whether you already
have it by opening PowerShell and running:

```powershell
wsl --version
```

If this prints version information, continue with the options below. If you get an error,
install WSL 2 and restart your computer when prompted:

```powershell
wsl --install
```

More information on WSL 2 is available
[here](https://learn.microsoft.com/en-us/windows/wsl/install).

Then choose one of the two options:

**Option A — Docker Desktop via `winget` (fastest):** open PowerShell as Administrator and run:

```powershell
winget install Docker.DockerDesktop
```

**Option B — Docker Desktop installer:**

1. Download and install Docker Desktop from
   [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/).
2. During installation, make sure **"Use WSL 2 instead of Hyper-V"** is selected.

Verify your installation (both options):

```powershell
docker --version
docker compose version
```

**Start the Docker Desktop app.** Docker Desktop must be running for Docker commands to
work. Look for the whale icon in your system tray; if it is not there, launch Docker
Desktop from the Start menu and wait until it shows "Engine running".

You **do not** need a Docker account. Skip any sign-in prompt.

---

## Check that Docker works

With Docker running, type this in any terminal:

```bash
docker run --rm hello-world
```

A message starting with `Hello from Docker!` means the installation is complete. 🎉

## Troubleshooting

- **`docker: command not found`:** Docker is not installed, or the terminal was opened
  before the installation finished. Open a new terminal, or restart your computer.
- **`Cannot connect to the Docker daemon`:** the Docker engine is not running. Start
  Docker Desktop, run `colima start`, or run `sudo systemctl start docker`.
- **`permission denied` on Linux:** your user is not in the `docker` group. Run
  `sudo usermod -aG docker $USER`, then log out and back in.
- **`wsl --install` fails on Windows:** make sure virtualization is enabled in the
  BIOS/UEFI settings and that Windows is up to date, then try again.
