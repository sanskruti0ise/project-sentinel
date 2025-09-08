import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- Page Configuration ---
st.set_page_config(
    page_title="Sentinel Monitoring Dashboard",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Project Sentinel: Production Monitoring Dashboard")
st.markdown("This dashboard simulates real-time monitoring of the AI Risk Assessment model.")

# --- Helper Functions to Generate Fake Data ---

@st.cache_data
def get_training_data_dist():
    """Loads a sample of the training data to get baseline distributions."""
    # In a real scenario, this would be a pre-computed statistics file.
    # For this simulation, we load the actual data.
    try:
        df = pd.read_csv("data/creditcard.csv")
        return df['Amount']
    except FileNotFoundError:
        st.error("Error: `creditcard.csv` not found. Please ensure Phase 1 setup was completed.")
        return pd.Series(np.random.uniform(0, 1000, 1000))

def generate_live_data(n_points=1000):
    """Generates a stream of simulated live transaction data."""
    base_time = datetime.now()
    
    # Simulate a slight drift in transaction amounts
    amounts = np.random.lognormal(mean=4, sigma=1.5, size=n_points)
    amounts[amounts > 5000] = np.random.uniform(500, 2000, len(amounts[amounts > 5000])) # Cap outliers
    
    # Simulate fraud predictions (imbalanced)
    predictions = np.random.choice([0, 1], size=n_points, p=[0.995, 0.005]) # 0.5% fraud rate
    
    # Simulate API response times
    response_times = np.random.gamma(2, 0.05, n_points) * 1000 # in ms
    
    timestamps = [base_time - timedelta(minutes=x) for x in range(n_points)]
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'amount': amounts,
        'prediction': predictions,
        'response_time_ms': response_times
    })
    return df

# --- Main Dashboard ---

training_amount_dist = get_training_data_dist()
live_data = generate_live_data()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Transactions (24h)",
        f"{len(live_data):,}"
    )
with col2:
    fraud_rate = live_data['prediction'].mean()
    st.metric(
        "Detected Fraud Rate",
        f"{fraud_rate:.2%}",
        delta=f"{(fraud_rate - 0.0017):.2%}", # Compare to training set rate
        delta_color="inverse"
    )
with col3:
    avg_latency = live_data['response_time_ms'].mean()
    st.metric(
        "Average API Latency",
        f"{avg_latency:.2f} ms",
        delta=f"{(avg_latency - 120):.2f} ms"
    )

st.divider()

# --- Visualizations ---
chart1, chart2 = st.columns(2)

with chart1:
    st.subheader("Prediction Distribution")
    prediction_counts = live_data['prediction'].value_counts().rename({0: 'Legitimate', 1: 'Fraud'})
    fig = px.pie(
        prediction_counts,
        values=prediction_counts.values,
        names=prediction_counts.index,
        title="Live Predictions (Simulated)",
        color=prediction_counts.index,
        color_discrete_map={'Legitimate':'green', 'Fraud':'red'}
    )
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.subheader("API Response Time")
    live_data_sorted = live_data.sort_values('timestamp')
    fig = px.line(
        live_data_sorted,
        x='timestamp',
        y='response_time_ms',
        title='API Latency Over Time (Simulated)',
        labels={'timestamp': 'Time', 'response_time_ms': 'Latency (ms)'}
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Feature Drift Detection: Transaction `Amount`")
st.markdown("Comparing the distribution of transaction amounts in the training data versus live, simulated data. A significant change could indicate data drift.")

fig = go.Figure()
fig.add_trace(go.Histogram(x=training_amount_dist, name='Training Data', xbins=dict(start=0, end=500, size=10), marker_color='blue', opacity=0.6))
fig.add_trace(go.Histogram(x=live_data['amount'], name='Live Data (Simulated)', xbins=dict(start=0, end=500, size=10), marker_color='orange', opacity=0.6))

fig.update_layout(
    barmode='overlay',
    title_text='Distribution of Transaction Amount (0-$500)',
    xaxis_title_text='Amount ($)',
    yaxis_title_text='Count'
)
st.plotly_chart(fig, use_container_width=True)

