# ==============================================================================
# Dockerfile — AI Applications in Accelerators Tutorial & Mini-Hackathon
# KOMAC / KAERI
# ==============================================================================

FROM python:3.12-slim

# Set environment variables for non-interactive installs and clean Python logging
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install essential build and runtime utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set workspace directory
WORKDIR /workspace

# Copy dependency configuration and source package first for Docker layer caching
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Upgrade pip and install package in editable mode with development tools (JupyterLab, Notebook, Pytest, Black)
RUN pip install --upgrade pip setuptools wheel && \
    pip install -e ".[dev]" && \
    python -m ipykernel install --name=ai4acc --display-name="Python (ai4acc)"

# Copy all remaining project files (notebooks, lecture notes, docs, img, setup script)
COPY . .

# Ensure solution notebooks are excluded from participant container image
RUN rm -f /workspace/notebooks/*Solution*.ipynb

# Expose default Jupyter port
EXPOSE 8888

# Default command: Launch Jupyter Lab accessible from any host browser
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--ServerApp.token=", "--ServerApp.password="]
