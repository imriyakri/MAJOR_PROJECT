import React, { useState, useEffect } from "react";
import { signOut } from "firebase/auth";
import { getAuth } from "firebase/auth";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Line } from "react-chartjs-2";
import "chart.js/auto";
import "./dashboard.css"; // Import styles

const Dashboard = ({ user }) => {
  const auth = getAuth();
  const navigate = useNavigate();
  const [cpuData, setCpuData] = useState([]);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/get_usage_data")
      .then((res) => setCpuData(res.data.data))
      .catch((err) => console.error("Error fetching data:", err));

    axios.get("http://127.0.0.1:8000/get_alerts")
      .then((res) => setAlerts(res.data.alerts))
      .catch((err) => console.error("Error fetching alerts:", err));
  }, []);

  const handleLogout = async () => {
    await signOut(auth);
    navigate("/login"); // Redirect to login after logout
  };

  const chartData = {
    labels: cpuData.map((_, index) => `Time ${index + 1}`),
    datasets: [
      {
        label: "CPU Usage (%)",
        data: cpuData.map((data) => data.cpu_usage),
        borderColor: "rgb(75, 192, 192)",
        tension: 0.4,
      },
    ],
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-card">
        <h1 className="dashboard-title">Cloud Resource Monitoring</h1>
        <button className="logout-btn" onClick={handleLogout}>Logout</button>
        
        <div className="chart-section">
          <h2>CPU Usage Forecast</h2>
          <div className="chart-box">
            <Line data={chartData} />
          </div>
        </div>

        <div className="alerts-section">
          <h2>Alerts</h2>
          <ul>
            {alerts.length > 0 ? alerts.map((alert, index) => (
              <li key={index} className="alert-text">{alert.message}</li>
            )) : <p>No alerts</p>}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
