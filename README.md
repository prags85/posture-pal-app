# 🧍‍♀️ Posture Pal - Rule-Based Bad Posture Detection App

**Posture Pal** is a full-stack web application that detects bad posture using rule-based logic. Users can upload a **video or image** while squatting or sitting at a desk, and the app will analyze posture in real-time and flag common posture issues.

![Posture Pal Banner](https://via.placeholder.com/800x300.png?text=Posture+Pal+Demo)

---

## 🧠 Features

- 📹 Upload video or image from webcam or file
- 🎯 Rule-based logic for posture detection
- 💬 Instant feedback with visual emojis (✅ / ❌)
- 🌐 Deployed frontend and backend
- 📦 MediaPipe + OpenCV used for keypoint extraction
- 🦴 Detects issues like:
  - Knee over toe
  - Back angle < 150°
  - Neck bend > 30°

---

## 🛠 Tech Stack

| Layer       | Tech                     |
|-------------|--------------------------|
| Frontend    | React, JSX, CSS, Icons   |
| Backend     | Flask, MediaPipe, OpenCV |
| Deployment  | Vercel (Frontend), Render (Backend) |

---

## 🔗 Live Links

- 🚀 **Frontend** (Vercel): [https://posture-pal.vercel.app][(https://posture-pal.vercel.app)](https://effulgent-hummingbird-28aa9d.netlify.app/)
- 🧠 **Backend API** (Render): [[https://posture-api.onrender.com](https://posture-api.onrender.com)](https://posture-pal-app-8.onrender.com)
- 🎥 **Demo Video**: [Watch Demo](https://youtu.be/YOUR_VIDEO_LINK)

---

## 🧪 Setup Instructions (Run Locally)

### 1. Clone the repo

```bash
git clone https://github.com/prags85/posture-pal-app.git
cd posture-pal-app




## 🧪 Setup Instructions (Run Locally)

> 📌 Make sure you have **Python 3.7+** and **Node.js + npm** installed.

---

### 🖥️ 1. Backend Setup (Flask)

```bash
# Go to the backend folder
cd backend

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py





💻 3. Frontend Setup (React)
# Open a new terminal window and go to frontend
cd frontend

# Install React dependencies
npm install

# Start the React development server
npm start

