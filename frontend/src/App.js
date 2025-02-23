import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import { initializeApp } from "firebase/app";
import { getAuth, onAuthStateChanged } from "firebase/auth";
import LoginPage from "./LoginPage"; // Ensure correct path
import Dashboard from "./Dashboard"; // Import Dashboard
import "./style.css"; // Import styles

const firebaseConfig = {
  apiKey: "AIzaSyBtdr-2UdkPPDoauMbB2bZUjxEYnfAJVCQ",
  authDomain: "cloud-resource-forecaster.firebaseapp.com",
  projectId: "cloud-resource-forecaster",
  storageBucket: "cloud-resource-forecaster.firebasestorage.app",
  messagingSenderId: "665502638177",
  appId: "1:665502638177:web:e9d4b66a3dfa626dacca20",
  measurementId: "G-H75GDTYNTE",
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
    });
    return () => unsubscribe();
  }, []);

  return (
    <Router>
      <Routes>
        {/* If user is logged in, go to Dashboard, else go to Login */}
        <Route path="/" element={<LoginPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<Dashboard/> } />
      </Routes>
    </Router>
  );
}

export default App;
