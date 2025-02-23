import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firestore
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Load your dataset
@st.cache_data
def load_data():
    df = pd.read_csv("your_dataset.csv")  # Replace with your actual dataset path
    return df

df = load_data()

st.title("🚀 Cloud Resource Monitoring Dashboard")

# Sidebar Filters
vm_id = st.sidebar.selectbox("Select VM ID", df["vm_id"].unique())
filtered_data = df[df["vm_id"] == vm_id]

# Display Metrics
st.write("### 📊 CPU & Memory Usage Over Time")
fig, ax = plt.subplots()
ax.plot(filtered_data["timestamp"], filtered_data["cpu_usage"], label="CPU Usage")
ax.plot(filtered_data["timestamp"], filtered_data["memory_usage"], label="Memory Usage")
ax.set_xlabel("Time")
ax.set_ylabel("Usage (%)")
ax.legend()
st.pyplot(fig)

# Store Alert in Firestore if CPU usage exceeds 90%
if filtered_data["cpu_usage"].max() > 90:
    alert_message = f"⚠️ High CPU Usage detected for VM {vm_id}!"
    db.collection("alerts").add({
        "vm_id": vm_id,
        "message": alert_message,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    st.warning(alert_message)

# Fetch and Display Alerts from Firestore
st.write("### 🔔 Active Alerts")
alerts_ref = db.collection("alerts").order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
for alert in alerts_ref:
    data = alert.to_dict()
    st.warning(f"**VM {data['vm_id']}**: {data['message']} (⏳ {data['timestamp']})")
