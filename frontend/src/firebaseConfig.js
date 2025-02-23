import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
const firebaseConfig = {
    apiKey: "AIzaSyBtdr-2UdkPPDoauMbB2bZUjxEYnfAJVCQ",
    authDomain: "cloud-resource-forecaster.firebaseapp.com",
    projectId: "cloud-resource-forecaster",
    storageBucket: "cloud-resource-forecaster.firebasestorage.app",
    messagingSenderId: "665502638177",
    appId: "1:665502638177:web:e9d4b66a3dfa626dacca20",
    measurementId: "G-H75GDTYNTE"
  };

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export { auth };
