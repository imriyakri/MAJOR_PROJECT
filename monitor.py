import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def store_alert(vm_id, message):
    """Store alerts in Firebase Firestore instead of sending emails."""
    alert_ref = db.collection("alerts").add({
        "vm_id": vm_id,
        "message": message,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    print(f"🔥 Alert Stored for {vm_id}: {message}")

# Example: Trigger an alert when CPU usage is high
def check_resource_usage(vm_id, cpu_usage):
    if cpu_usage > 80:  # Set threshold
        store_alert(vm_id, f"High CPU Usage Alert: {cpu_usage}%")

# Example test
check_resource_usage("VM-101", 85)

