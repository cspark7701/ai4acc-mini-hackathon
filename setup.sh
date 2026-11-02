#!/usr/bin/env bash
# ==============================================================================
# setup.sh — Dynamic Python Virtual Environment Setup & Activation Script
# AI Applications in Accelerators Tutorial & Mini-Hackathon (KOMAC / KAERI)
# ==============================================================================

# 1. Dynamically resolve the absolute repository root directory without hardcoding
if [ -n "${BASH_SOURCE[0]}" ]; then
    _SCRIPT_PATH="${BASH_SOURCE[0]}"
elif [ -n "${ZSH_VERSION}" ]; then
    _SCRIPT_PATH="${(%):-%x}"
else
    _SCRIPT_PATH="$0"
fi

REPO_ROOT="$(cd "$(dirname "${_SCRIPT_PATH}")" >/dev/null 2>&1 && pwd)"

# 2. Check whether the script is being sourced or executed directly
(return 0 2>/dev/null) && _IS_SOURCED=1 || _IS_SOURCED=0

# 3. Locate or select virtual environment directory dynamically
VENV_NAME="${VENV_NAME:-ai4acc}"
VENV_DIR="${REPO_ROOT}/${VENV_NAME}"

# 4. Automatically create virtual environment if not already present
if [ ! -f "${VENV_DIR}/bin/activate" ]; then
    echo "[setup.sh] Virtual environment not found at: ${VENV_DIR}"
    
    # Locate available python interpreter dynamically
    PYTHON_CMD=""
    for cand in python3 python python3.12 python3.11 python3.10 python3.13; do
        if command -v "${cand}" >/dev/null 2>&1; then
            PYTHON_CMD="$(command -v "${cand}")"
            break
        fi
    done

    if [ -z "${PYTHON_CMD}" ]; then
        echo "[setup.sh Error] No suitable Python interpreter found on PATH. Please install Python 3.9+."
        return 1 2>/dev/null || exit 1
    fi

    echo "[setup.sh] Initializing virtual environment using ${PYTHON_CMD}..."
    "${PYTHON_CMD}" -m venv "${VENV_DIR}"
    if [ $? -ne 0 ]; then
        echo "[setup.sh Error] Failed to create virtual environment."
        return 1 2>/dev/null || exit 1
    fi

    echo "[setup.sh] Upgrading pip and installing project dependencies in editable mode..."
    "${VENV_DIR}/bin/pip" install --upgrade pip
    "${VENV_DIR}/bin/pip" install -e "${REPO_ROOT}[dev]"
fi

# 5. Activate virtual environment
if [ -f "${VENV_DIR}/bin/activate" ]; then
    if [ ${_IS_SOURCED} -eq 1 ]; then
        # If another or previous virtual environment is currently active, deactivate it cleanly first
        if [ -n "${VIRTUAL_ENV:-}" ] && [ "${VIRTUAL_ENV}" != "${VENV_DIR}" ]; then
            if type deactivate >/dev/null 2>&1; then
                deactivate
            fi
        fi

        # shellcheck disable=SC1090
        source "${VENV_DIR}/bin/activate"

        # Ensure any leftover (.venv) in prompt is cleanly stripped
        if [[ "${PS1:-}" == *"(.venv)"* ]]; then
            PS1="${PS1//\(\.venv\) /}"
            PS1="${PS1//\(\.venv\)/}"
        fi

        # Set dynamic PYTHONPATH ensuring 'src' imports work from anywhere
        if [[ ":${PYTHONPATH:-}:" != *":${REPO_ROOT}:"* ]]; then
            export PYTHONPATH="${REPO_ROOT}${PYTHONPATH:+:${PYTHONPATH}}"
        fi

        echo "=================================================================="
        echo "   AI Applications in Accelerators Tutorial & Mini-Hackathon      "
        echo "=================================================================="
        echo " [✓] Environment Activated : $(which python)"
        echo " [✓] Python Version         : $(python --version 2>&1)"
        echo " [✓] Workspace Root         : ${REPO_ROOT}"
        echo " [✓] PYTHONPATH Added       : ${REPO_ROOT}"
        echo "------------------------------------------------------------------"
        echo " Quickstart Commands:"
        echo "   • Start Jupyter Lab      : jupyter lab"
        echo "   • Run Participant Edition: jupyter lab notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb"
        echo "   • Headless Benchmark Test: python -c 'import src; print(\"src loaded successfully!\")'"
        echo "   • Deactivate Environment : deactivate"
        echo "=================================================================="
    else
        echo "[setup.sh] Virtual environment verified at: ${VENV_DIR}"
        echo ""
        echo "NOTICE: To activate this environment in your current shell, please RUN:"
        echo ""
        echo "    source setup.sh"
        echo "    # or"
        echo "    . setup.sh"
        echo ""
    fi
else
    echo "[setup.sh Error] Activation script missing at ${VENV_DIR}/bin/activate"
    return 1 2>/dev/null || exit 1
fi
