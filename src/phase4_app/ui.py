import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="Project Sentinel",
    page_icon="🛡️",
    layout="centered"
)

# --- App Title and Description ---
st.title("🛡️ Project Sentinel: AI Risk Assessment")
st.markdown("Enter credit card transaction details below to get a real-time risk assessment from the AI workflow.")

# --- API Endpoint ---
API_URL = "http://127.0.0.1:8000/assess-transaction"

# --- Pre-filled examples ---
legit_transaction = "0.0,-1.3598071336738,-0.0727811733593648,2.53634673796914,1.37815522427443,-0.338320769942518,0.462387777762292,0.23959855406126,0.0986979012610507,0.363786969611215,0.0907941719789316,-0.551599533260813,-0.617800855762348,-0.991389847235408,-0.311169353699879,1.46817697209427,-0.470400525259478,0.207971241929242,0.0257905801985591,0.403992960255733,0.251412098239705,-0.018306777944153,0.277837575558899,-0.110473910188767,0.0669280749146731,0.128539358273528,-0.189114843888824,0.133558376740387,-0.0210530534538215,149.62"
fraud_transaction = "406.0,-2.312226542,1.951992011,-1.609850732,3.997905588,-0.522187865,-1.426545318,-2.537387306,1.391657248,-2.770089273,-2.772272145,3.202033207,-2.899907388,-0.595221881,-4.289253782,0.38972412,-1.14074718,-2.830055675,-0.016822468,0.416955705,0.126910559,0.517232371,-0.035049369,-0.465211076,-0.320401205,0.04453624,0.177839798,-0.258264956,-0.63864032,0.0"

# --- State Management ---
# Initialize session state for the input text if it doesn't exist
if 'transaction_input' not in st.session_state:
    st.session_state.transaction_input = fraud_transaction

def set_text_input(text):
    """Callback function to update the session state."""
    st.session_state.transaction_input = text

# --- User Input ---
st.subheader("Transaction Data")
# The text_area's content is now controlled by the session state
transaction_input = st.text_area(
    "Paste the 30 comma-separated transaction values here:",
    key='transaction_input', # Bind the widget to the session state key
    height=150
)

# Use columns for buttons, with on_click callbacks to update the state
col1, col2 = st.columns(2)
with col1:
    st.button(
        "Use Fraud Example",
        on_click=set_text_input,
        args=(fraud_transaction,)
    )
with col2:
    st.button(
        "Use Legitimate Example",
        on_click=set_text_input,
        args=(legit_transaction,)
    )

# --- Assessment Trigger ---
if st.button("Assess Transaction", type="primary"):
    if not transaction_input.strip():
        st.warning("Please enter transaction data.")
    else:
        with st.spinner("AI workflow is processing..."):
            try:
                payload = {"transaction_details": transaction_input}
                response = requests.post(API_URL, json=payload, timeout=60)
                response.raise_for_status()

                result = response.json()
                recommendation = result.get("recommendation")
                
                st.subheader("Assessment Result")
                if "Approved" in recommendation:
                    st.success(f"✅ **Recommendation:** {recommendation}")
                elif "Blocked" in recommendation:
                    st.error(f"🚨 **Recommendation:** {recommendation}")
                else:
                    st.warning(f"⚠️ **Recommendation:** {recommendation}")
                
                with st.expander("Show Full Workflow State"):
                    st.json(result.get("details", {}))

            except requests.exceptions.RequestException as e:
                st.error(f"API Connection Error: Could not connect to the backend. Please ensure the API server is running. Details: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")


