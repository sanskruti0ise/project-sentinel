import streamlit as st
import requests

# --- Page Configuration ---
st.set_page_config(
    page_title="Project Sentinel",
    page_icon="🛡️",
    layout="centered"
)

# --- App Title and Description ---
st.title("🛡️ Project Sentinel: AI Risk Assessment")
st.markdown("Enter transaction details below. You can use the examples and then modify the `Time` and `Amount` to see how the AI responds.")

# --- API Endpoint ---
API_URL = "http://127.0.0.1:8000/assess-transaction"

# --- Pre-filled examples ---
legit_transaction_str = "0.0,-1.3598071336738,-0.0727811733593648,2.53634673796914,1.37815522427443,-0.338320769942518,0.462387777762292,0.23959855406126,0.0986979012610507,0.363786969611215,0.0907941719789316,-0.551599533260813,-0.617800855762348,-0.991389847235408,-0.311169353699879,1.46817697209427,-0.470400525259478,0.207971241929242,0.0257905801985591,0.403992260255733,0.251412098239705,-0.018306777944153,0.277837575558899,-0.110473910188767,0.0669280749146731,0.128539358273528,-0.189114843888824,0.133558376740387,-0.0210530534538215,149.62"
fraud_transaction_str = "406.0,-2.312226542,1.951992011,-1.609850732,3.997905588,-0.522187865,-1.426545318,-2.537387306,1.391657248,-2.770089273,-2.772272145,3.202033207,-2.899907388,-0.595221881,-4.289253782,0.38972412,-1.14074718,-2.830055675,-0.016822468,0.416955705,0.126910559,0.517232371,-0.035049369,-0.465211076,-0.320401205,0.04453624,0.177839798,-0.258264956,-0.63864032,0.0"

def parse_transaction(tx_str):
    """Helper to parse the transaction string into components."""
    vals = [float(v) for v in tx_str.split(',')]
    return {
        "time": vals[0],
        "v_features": ",".join(map(str, vals[1:-1])),
        "amount": vals[-1]
    }

# --- State Management ---
if 'time' not in st.session_state:
    initial_state = parse_transaction(fraud_transaction_str)
    st.session_state.time = initial_state['time']
    st.session_state.v_features = initial_state['v_features']
    st.session_state.amount = initial_state['amount']

def set_example_transaction(tx_str):
    """Callback to update state with a full transaction example."""
    state = parse_transaction(tx_str)
    st.session_state.time = state['time']
    st.session_state.v_features = state['v_features']
    st.session_state.amount = state['amount']

# --- User Input ---
st.subheader("Transaction Data")
st.markdown("You can edit the `Time` and `Amount` fields below.")

col1, col2 = st.columns(2)
with col1:
    st.number_input("Time (seconds since first transaction)", key="time", step=1.0)
with col2:
    st.number_input("Transaction Amount ($)", key="amount", min_value=0.0, step=10.0, format="%.2f")

st.info("ℹ️ The 28 anonymized 'V' features are loaded from the examples below.")


# Use columns for buttons to load examples
col1, col2 = st.columns(2)
with col1:
    st.button(
        "Load Fraud Example",
        on_click=set_example_transaction,
        args=(fraud_transaction_str,)
    )
with col2:
    st.button(
        "Load Legitimate Example",
        on_click=set_example_transaction,
        args=(legit_transaction_str,)
    )


# --- Assessment Trigger ---
if st.button("Assess Transaction", type="primary"):
    # Reconstruct the full transaction string from the state
    full_transaction_str = f"{st.session_state.time},{st.session_state.v_features},{st.session_state.amount}"
    
    with st.spinner("AI workflow is processing..."):
        try:
            payload = {"transaction_details": full_transaction_str}
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


