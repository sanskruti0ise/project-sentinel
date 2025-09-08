#!/bin/bash

# --- Phase 3: LangGraph Multi-Agent Workflow ---

echo "--- Phase 3: LangGraph Multi-Agent Workflow ---"

# Check for .env file
if [ ! -f .env ]; then
    echo "❌ Error: '.env' file not found. Please create it and add your GOOGLE_API_KEY."
    exit 1
else
    echo "✅ '.env' file found."
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating Python virtual environment..."
    source venv/bin/activate
else
    echo "❗️Warning: Virtual environment not found. Running with system Python."
fi

echo "Updating dependencies for Phase 3..."
# Install requirements, -q for quiet
pip install -r requirements.txt -q
echo "Dependencies are up to date."

echo "Running the risk assessment graph..."
# Execute the main graph script
python src/phase3_graph/risk_assessment_graph.py

echo -e "\n--- Phase 3 Execution Successful! ---"

