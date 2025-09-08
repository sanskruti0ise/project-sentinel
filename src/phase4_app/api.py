import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# Add the project root to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Now we can import from src
from src.phase3_graph.risk_assessment_graph import get_graph_app

# --- 1. Initialize FastAPI app and LangGraph ---
app = FastAPI(
    title="Project Sentinel API",
    description="API for the AI Risk Assessment Workflow",
    version="1.0.0"
)

# Compile the LangGraph app when the API starts
langgraph_app = get_graph_app()
print("✅ LangGraph workflow compiled and ready.")

# --- 2. Define Request and Response Models ---
class TransactionRequest(BaseModel):
    transaction_details: str

class AssessmentResponse(BaseModel):
    recommendation: str
    details: dict

# --- 3. Define the API Endpoint ---
@app.post("/assess-transaction", response_model=AssessmentResponse)
async def assess_transaction(request: TransactionRequest):
    """
    Receives transaction details and returns the final risk assessment
    from the LangGraph workflow.
    """
    print(f"Received request for transaction...")
    inputs = {"transaction_details": request.transaction_details}
    
    # Invoke the LangGraph workflow
    result = langgraph_app.invoke(inputs)
    
    print(f"Workflow finished with result: {result.get('final_recommendation')}")
    
    return {
        "recommendation": result.get('final_recommendation', 'Error: Could not determine recommendation.'),
        "details": result
    }

# --- 4. Run the API Server ---
if __name__ == "__main__":
    print("Starting FastAPI server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)

