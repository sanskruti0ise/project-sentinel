#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
VENV_DIR="venv"
PYTHON="${VENV_DIR}/bin/python"
ENV_FILE=".env"

echo "--- Phase 2: AI Risk Assessment Agent ---"

# 1. Check for .env file
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Error: The '.env' file is missing."
    echo "Please create it and add your OPENAI_API_KEY."
    exit 1
fi

echo "✅ '.env' file found."

# 2. Ensure dependencies are installed
echo "Updating dependencies for Phase 2..."
${PYTHON} -m pip install -r requirements.txt --quiet
echo "Dependencies are up to date."

# 3. Run the agent script
echo "Running the risk assessment agent..."
${PYTHON} src/phase2_agent/risk_assessment_agent.py
echo "Agent execution finished."

echo -e "\n--- Phase 2 Execution Successful! ---"

