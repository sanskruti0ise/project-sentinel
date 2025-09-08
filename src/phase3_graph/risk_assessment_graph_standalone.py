import joblib
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph, END

# --- 1. Load Environment Variables and Models ---
# Note: We are reusing the same model and tool from Phase 2
load_dotenv()

MODEL_PATH = "models/xgb_fraud_detector.joblib"
SCALER_PATH = "models/scaler.joblib"

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("✅ Model and scaler loaded successfully for the graph.")
except FileNotFoundError:
    print("❌ Error: Model or scaler not found. Please run Phase 1 first.")
    exit()

# --- 2. Define the Fraud Detection Tool (reused from Phase 2) ---
def fraud_detection_tool(transaction_details: str) -> str:
    """
    Analyzes a credit card transaction to determine if it is fraudulent.
    Input should be a comma-separated string of 30 numerical values.
    Returns 'FRAUD' or 'NOT FRAUD'.
    """
    try:
        features = np.array([float(val) for val in transaction_details.split(',')])
        if len(features) != 30:
            return "Error: Input must contain exactly 30 numerical values."
        
        col_names = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
        features_df = pd.DataFrame([features], columns=col_names)
        
        scaled_features = scaler.transform(features_df)
        prediction = model.predict(scaled_features)
        
        result = "FRAUD" if prediction[0] == 1 else "NOT FRAUD"
        print(f"Tool raw prediction: {prediction[0]}, result: {result}")
        return result
    except Exception as e:
        return f"An error occurred: {str(e)}"

# --- 3. Define the Graph's State ---
# This is the "memory" of our graph. It holds the data that gets passed between nodes.
class GraphState(TypedDict):
    transaction_details: str
    triage_result: str
    final_recommendation: str

# --- 4. Define the Graph's Nodes ---
# Each node is a function that performs an action and updates the state.

def triage_node(state: GraphState):
    """
    First step: Use the fraud detection tool to assess the transaction.
    """
    print("--- Executing Triage Node ---")
    transaction = state['transaction_details']
    result = fraud_detection_tool(transaction)
    
    # Update the state with the result
    return {"triage_result": result}

def legitimate_node(state: GraphState):
    """
    This node is reached if the transaction is not fraudulent.
    """
    print("--- Executing Legitimate Node ---")
    recommendation = "Transaction Approved. No further action required."
    return {"final_recommendation": recommendation}

def fraudulent_node(state: GraphState):
    """
    This node is reached if the transaction is flagged as fraudulent.
    """
    print("--- Executing Fraudulent Node ---")
    recommendation = "Transaction Blocked. Escalated to Human Review Team."
    return {"final_recommendation": recommendation}

# --- 5. Define the Graph's Edges (The Routing Logic) ---

def decide_next_node(state: GraphState) -> str:
    """
    This is the conditional edge. It decides which node to go to next
    based on the result of the triage node.
    """
    print("--- Making routing decision ---")
    if "Error" in state['triage_result']:
        print("Routing to: END (due to tool error)")
        return END # Or a dedicated error handling node
    elif state['triage_result'] == "FRAUD":
        print("Routing to: fraudulent_node")
        return "fraudulent_node"
    else:
        print("Routing to: legitimate_node")
        return "legitimate_node"

# --- 6. Construct the Graph ---

workflow = StateGraph(GraphState)

# Add the nodes
workflow.add_node("triage_node", triage_node)
workflow.add_node("legitimate_node", legitimate_node)
workflow.add_node("fraudulent_node", fraudulent_node)

# Set the entry point
workflow.set_entry_point("triage_node")

# Add the conditional edge
workflow.add_conditional_edges(
    "triage_node",
    decide_next_node,
    {
        "fraudulent_node": "fraudulent_node",
        "legitimate_node": "legitimate_node",
    }
)

# Add edges that lead to the end of the graph
workflow.add_edge("legitimate_node", END)
workflow.add_edge("fraudulent_node", END)

# Compile the graph into a runnable object
app = workflow.compile()
print("\n✅ LangGraph workflow compiled successfully.")

# --- 7. Main Execution Block ---

if __name__ == "__main__":
    # The same test cases from Phase 2
    legit_transaction = "0.0,-1.3598071336738,-0.0727811733593648,2.53634673796914,1.37815522427443,-0.338320769942518,0.462387777762292,0.23959855406126,0.0986979012610507,0.363786969611215,0.0907941719789316,-0.551599533260813,-0.617800855762348,-0.991389847235408,-0.311169353699879,1.46817697209427,-0.470400525259478,0.207971241929242,0.0257905801985591,0.403992960255733,0.251412098239705,-0.018306777944153,0.277837575558899,-0.110473910188767,0.0669280749146731,0.128539358273528,-0.189114843888824,0.133558376740387,-0.0210530534538215,149.62"
    fraud_transaction = "406.0,-2.312226542,1.951992011,-1.609850732,3.997905588,-0.522187865,-1.426545318,-2.537387306,1.391657248,-2.770089273,-2.772272145,3.202033207,-2.899907388,-0.595221881,-4.289253782,0.38972412,-1.14074718,-2.830055675,-0.016822468,0.416955705,0.126910559,0.517232371,-0.035049369,-0.465211076,-0.320401205,0.04453624,0.177839798,-0.258264956,-0.63864032,0.0"

    print("\n\n--- Running Graph with Legitimate Transaction ---")
    inputs = {"transaction_details": legit_transaction}
    result = app.invoke(inputs)
    print("\n--- Final Graph State (Legitimate) ---")
    print(result)

    print("\n\n--- Running Graph with Fraudulent Transaction ---")
    inputs = {"transaction_details": fraud_transaction}
    result = app.invoke(inputs)
    print("\n--- Final Graph State (Fraudulent) ---")
    print(result)

