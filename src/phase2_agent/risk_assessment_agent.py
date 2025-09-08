import joblib
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import tool, AgentExecutor, create_react_agent
from langchain import hub

# --- 1. Load Environment Variables and Models ---
load_dotenv()

MODEL_PATH = "models/xgb_fraud_detector.joblib"
SCALER_PATH = "models/scaler.joblib"

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("✅ Model and scaler loaded successfully.")
except FileNotFoundError:
    print("❌ Error: Model or scaler not found. Please run Phase 1 first.")
    exit()

# --- 2. Create the Fraud Detection Tool ---
@tool
def fraud_detection_tool(transaction_details: str) -> str:
    """
    Analyzes a credit card transaction to determine if it is fraudulent.
    Input should be a comma-separated string of 30 numerical values
    representing the transaction features in the order: Time, V1-V28, Amount.
    Returns 'FRAUD' if the transaction is likely fraudulent,
    'NOT FRAUD' if it is likely legitimate.
    """
    try:
        features = np.array([float(val) for val in transaction_details.split(',')])
        
        if len(features) != 30:
            return "Error: Input must contain exactly 30 numerical values."

        # --- FIX: Create a DataFrame with the correct feature names ---
        # This matches the format the StandardScaler was trained on.
        col_names = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
        features_df = pd.DataFrame([features], columns=col_names)

        # Use the DataFrame for scaling and prediction
        scaled_features = scaler.transform(features_df)
        prediction = model.predict(scaled_features)
        
        result = "FRAUD" if prediction[0] == 1 else "NOT FRAUD"
        print(f"Tool raw prediction: {prediction[0]}, result: {result}")
        return result

    except Exception as e:
        return f"An error occurred: {str(e)}"

# --- 3. Define the Agent and Prompt ---
def create_risk_assessment_agent():
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    tools = [fraud_detection_tool]

    prompt = hub.pull("hwchase17/react")
    prompt.template = prompt.template.replace(
        "{agent_scratchpad}",
        """
You are a Senior Risk Analyst AI for a fintech company. Your task is to provide a clear and concise risk assessment for a given credit card transaction.

You have access to a highly accurate fraud detection model. Your job is not just to run the model, but to interpret its output and provide a structured, professional recommendation.

TOOLS:
------
You have access to the following tools:

{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: The action to take, should be one of [{tool_names}]
Action Input: The input to the action
Observation: The result of the action
```

When you have a final answer, you MUST use the format below.

```
Thought: Do I need to use a tool? No
Final Answer:
**Risk Assessment:** [FRAUD DETECTED or NO FRAUD DETECTED]
**Confidence:** [High]
**Recommendation:** [Block Transaction and Flag for Review or Approve Transaction]
**Justification:** [A brief, one-sentence explanation of why you made the recommendation, based on the model's output.]
```

Begin!

New Transaction Details: {input}
{agent_scratchpad}
"""
    )

    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    
    return agent_executor

# --- 4. Main Execution Block ---
if __name__ == "__main__":
    risk_agent = create_risk_assessment_agent()

    print("\n--- Analyzing a Potentially Legitimate Transaction ---")
    # A clear, legitimate transaction from the dataset
    legit_transaction = "0.0,-1.3598071336738,-0.0727811733593648,2.53634673796914,1.37815522427443,-0.338320769942518,0.462387777762292,0.23959855406126,0.0986979012610507,0.363786969611215,0.0907941719789316,-0.551599533260813,-0.617800855762348,-0.991389847235408,-0.311169353699879,1.46817697209427,-0.470400525259478,0.207971241929242,0.0257905801985591,0.403992960255733,0.251412098239705,-0.018306777944153,0.277837575558899,-0.110473910188767,0.0669280749146731,0.128539358273528,-0.189114843888824,0.133558376740387,-0.0210530534538215,149.62"
    result_legit = risk_agent.invoke({"input": legit_transaction})
    print("\n--- Final Assessment ---")
    print(result_legit['output'])

    print("\n\n--- Analyzing a Known Fraudulent Transaction ---")
    # A clear, fraudulent transaction from the dataset
    fraud_transaction = "406.0,-2.312226542,1.951992011,-1.609850732,3.997905588,-0.522187865,-1.426545318,-2.537387306,1.391657248,-2.770089273,-2.772272145,3.202033207,-2.899907388,-0.595221881,-4.289253782,0.38972412,-1.14074718,-2.830055675,-0.016822468,0.416955705,0.126910559,0.517232371,-0.035049369,-0.465211076,-0.320401205,0.04453624,0.177839798,-0.258264956,-0.63864032,0.0"
    result_fraud = risk_agent.invoke({"input": fraud_transaction})
    print("\n--- Final Assessment ---")
    print(result_fraud['output'])


