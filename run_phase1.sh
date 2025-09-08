#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
VENV_DIR="venv"
PYTHON="${VENV_DIR}/bin/python"
PROJECT_ROOT=$(pwd)

echo "--- Phase 1: Model Training Orchestrator ---"

# 1. Set up Virtual Environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python virtual environment in '${VENV_DIR}'..."
    python3 -m venv $VENV_DIR
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# 2. Install Dependencies
echo "Installing dependencies from requirements.txt..."
${PYTHON} -m pip install -r requirements.txt
echo "Dependencies installed."

# 3. Run the setup script to download data
echo "Running setup script to download data..."
${PYTHON} kaggle-data-download-setup.py # <-- This line has been updated
echo "Data setup complete."

# 4. Run the training script
echo "Running model training script..."
${PYTHON} src/phase1_training/train_model.py
echo "Model training complete."

echo -e "\n--- Phase 1 Execution Successful! ---"
echo "Model artifacts are saved in the 'models' directory."
echo "To view the experiment logs, run the following command in your terminal:"
echo "mlflow ui"


