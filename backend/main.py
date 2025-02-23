from fastapi import FastAPI, HTTPException, Depends
from firebase_admin import credentials, auth, firestore, initialize_app
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np
import tensorflow as tf
from fastapi.middleware.cors import CORSMiddleware
# Initialize Firebase
cred = credentials.Certificate("firebase_credentials.json")
initialize_app(cred)
db = firestore.client()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------- USER AUTHENTICATION -------- #
class UserAuth(BaseModel):
    email: str
    password: str

@app.post("/signup")
def signup(user: UserAuth):
    try:
        user_record = auth.create_user(email=user.email, password=user.password)
        return {"message": "User created successfully", "uid": user_record.uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login")
def login(user: UserAuth):
    return {"message": "Login handled on frontend with Firebase auth"}

# -------- FIRESTORE OPERATIONS -------- #
def add_to_firestore(collection: str, data: dict):
    try:
        doc_ref = db.collection(collection).add(data)
        return {"message": "Data added successfully", "doc_id": doc_ref[1].id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add_usage_data")
def add_usage_data(data: dict):
    return add_to_firestore("usage_data", data)

@app.get("/get_usage_data")
def get_usage_data():
    docs = db.collection("usage_data").stream()
    return {"data": [doc.to_dict() for doc in docs]}

@app.get("/get_alerts")
def get_alerts():
    docs = db.collection("alerts").stream()
    return {"alerts": [doc.to_dict() for doc in docs]}

# -------- FORECASTING MODEL API -------- #
# Load models and scaler
ml_model = joblib.load("forecast_model.pkl")
lstm_model = tf.keras.models.load_model("lstm_forecast_model.keras")
scaler = joblib.load("scaler.pkl")

@app.post("/predict")
def predict(usage_history: dict):
    try:
        usage_series = np.array(usage_history["cpu_usage"]).reshape(-1, 1)
        prediction = ml_model.predict(usage_series[-5:].reshape(1, -1))
        return {"predicted_cpu_usage": prediction.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/{vm_id}")
def predict_cpu(vm_id: str, data: dict):
    try:
        input_data = np.array([data["cpu_usage"], data["memory_usage"], data["network_traffic"]]).reshape(1, -1)
        input_scaled = scaler.transform(input_data)
        input_scaled = np.expand_dims(input_scaled, axis=0)
        
        predicted_cpu = lstm_model.predict(input_scaled)
        predicted_cpu = scaler.inverse_transform([[predicted_cpu[0][0]]])[0][0]
        predicted_cpu = max(predicted_cpu, 0)  # Ensure no negative predictions

        prediction_data = {"vm_id": vm_id, "predicted_cpu_usage": predicted_cpu}
        add_to_firestore("cpu_predictions", prediction_data)
        
        return prediction_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/predictions/{vm_id}")
def get_predictions(vm_id: str):
    docs = db.collection("cpu_predictions").where("vm_id", "==", vm_id).stream()
    return [{"vm_id": doc.get("vm_id"), "predicted_cpu_usage": doc.get("predicted_cpu_usage")} for doc in docs]

import psutil

def get_system_metrics():
    return {
        "cpu_usage": psutil.cpu_percent(),
        "ram_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "network": psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    }
