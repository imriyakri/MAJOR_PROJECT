import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load your dataset
@st.cache_data
def load_data():
    df = pd.read_csv("")  # Replace with your actual dataset path
    return df

df = load_data()

st.title("Cloud Resource Monitoring Dashboard")

# Sidebar Filters
vm_id = st.sidebar.selectbox("Select VM ID", df["vm_id"].unique())
filtered_data = df[df["vm_id"] == vm_id]

# Display Metrics
st.write("### CPU & Memory Usage Over Time")
fig, ax = plt.subplots()
ax.plot(filtered_data["timestamp"], filtered_data["cpu_usage"], label="CPU Usage")
ax.plot(filtered_data["timestamp"], filtered_data["memory_usage"], label="Memory Usage")
ax.set_xlabel("Time")
ax.set_ylabel("Usage (%)")
ax.legend()
st.pyplot(fig)

# Alert System
def send_email_alert(subject, body):
    sender_email = "your_email@gmail.com"
    receiver_email = "receiver_email@gmail.com"
    password = "your_app_password"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        st.success("Email alert sent successfully!")
    except Exception as e:
        st.error(f"Error sending email: {e}")

# Trigger email alert if CPU usage exceeds 90%
if filtered_data["cpu_usage"].max() > 90:
    send_email_alert(
        "High CPU Usage Alert",
        f"Warning! High CPU usage detected for VM {vm_id}."
    )

