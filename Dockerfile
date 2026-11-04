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

# Upgrade pip and install package permanently into system site-packages with development tools
RUN pip install --upgrade pip setuptools wheel && \
    pip install ".[dev]" && \
    python -m ipykernel install --name=ai4acc --display-name="Python (ai4acc)"

# Copy all repository materials
COPY . .

# Clean workspace so participants ONLY see:
# 1. Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb
# 2. Lecture_1_AI_ML_Techniques_for_Accelerators.pdf
# 3. Lecture_1_AI_ML_Foundations_and_Control.pdf
# Plus internal img/ needed by the notebook's draw_beamline / save_path.
RUN mv /workspace/notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb /workspace/ && \
    mv /workspace/lecture_notes/Lecture_1_AI_ML_Techniques_for_Accelerators.pdf /workspace/ && \
    mv /workspace/presentations/Lecture_1_AI_ML_Foundations_and_Control.pdf /workspace/ && \
    rm -rf /workspace/notebooks \
           /workspace/lecture_notes \
           /workspace/presentations \
           /workspace/docs \
           /workspace/dist \
           /workspace/scripts \
           /workspace/src \
           /workspace/build \
           /workspace/ai4acc_mini_hackathon.egg-info \
           /workspace/README.md \
           /workspace/AGENTS.md \
           /workspace/Dockerfile \
           /workspace/docker-compose.yml \
           /workspace/setup.sh \
           /workspace/pyproject.toml \
           /workspace/.dockerignore \
           /workspace/.git* \
           /workspace/img/ku_logo.png

# Expose default Jupyter port
EXPOSE 8888

# Default command: Launch Jupyter Lab directly in /workspace
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--ServerApp.token=", "--ServerApp.password="]
