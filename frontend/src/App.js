import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import { FaCloudUploadAlt, FaVideo } from 'react-icons/fa';

function App() {
  const [video, setVideo] = useState(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = (e) => {
    setVideo(e.target.files[0]);
    setResult("");
  };

  const handleSubmit = async () => {
    if (!video) {
      alert("📁 Please upload a video or image first!");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('video', video);

    try {
      const res = await axios.post(
        'https://posture-pal-app-8.onrender.com/analyze',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      setResult(res.data.feedback);
    } catch (err) {
      console.error(err);
      setResult(err?.response?.data?.feedback || "❌ Something went wrong. Try again.");
    }
    setLoading(false);
  };

  const getResultIcon = () => {
    if (result.includes("Bad") || result.includes("wrong") || result.includes("Unsupported")) {
      return "❌";
    } else {
      return "✅";
    }
  };

  const getResultClass = () => {
    if (result.includes("Bad") || result.includes("wrong") || result.includes("Unsupported")) {
      return "bad";
    } else {
      return "good";
    }
  };

  return (
    <div className="app">
      <header className="header">
        <FaVideo className="header-icon" />
        <h1>Posture Pal 🧍‍♀️</h1>
      </header>

      <div className="card">
        <label htmlFor="upload" className="upload-label">
          <FaCloudUploadAlt /> Upload posture video/image
        </label>
        <input
          id="upload"
          type="file"
          accept="video/*,image/*"
          onChange={handleUpload}
          hidden
        />

        <button onClick={handleSubmit}>🔍 Check Posture</button>

        {loading && <p className="loading">⏳ Analyzing posture...</p>}

        {!loading && result && (
          <p className={getResultClass()}>
            {getResultIcon()} {result}
          </p>
        )}
      </div>

      <footer className="footer">
        <p>Made with 💙 by Pragya | 2025</p>
      </footer>
    </div>
  );
}

export default App;
