from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import os
from pathlib import Path

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": [
    "http://localhost:3000",
    "https://posturepal-app.netlify.app",
    "https://effulgent-hummingbird-28aa9d.netlify.app"  # ✅ Add your Netlify domain
]}})


# ✅ Root route
@app.route('/', methods=['GET'])
def home():
    return "✅ Posture Pal API is running!"

# MediaPipe setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def get_angle(p1, p2, p3):
    a = np.array(p1)
    b = np.array(p2)
    c = np.array(p3)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
    return angle

def analyze_frame(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        shoulder = [landmarks[11].x, landmarks[11].y]
        hip = [landmarks[23].x, landmarks[23].y]
        knee = [landmarks[25].x, landmarks[25].y]
        ankle = [landmarks[27].x, landmarks[27].y]
        ear = [landmarks[7].x, landmarks[7].y]

        # Rule 1: Knee over toe
        if knee[0] > ankle[0] + 0.05:
            return "Bad posture: Knee is over the toe"

        # Rule 2: Back angle
        back_angle = get_angle(shoulder, hip, knee)
        if back_angle < 150:
            return f"Bad posture: Back angle is {int(back_angle)}°, should be ≥ 150°"

        # Rule 3: Neck bend
        neck_angle = get_angle(ear, shoulder, hip)
        if neck_angle < 150:
            return f"Bad posture: Neck angle is {int(neck_angle)}°, should be ≥ 150°"

        return "Good posture"

    return "No person detected"

@app.route('/analyze', methods=['POST'])
def analyze():
    print("📥 /analyze endpoint hit")
    print("📎 Uploaded files:", request.files)

    uploaded_file = request.files.get('video')
    if not uploaded_file:
        return jsonify({'feedback': 'No file received'}), 400

    filename = uploaded_file.filename
    file_ext = Path(filename).suffix.lower()
    print(f"📁 Received file: {filename}, extension: {file_ext}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    feedback_list = []

    try:
        # ✅ Video processing
        if file_ext in ['.mp4', '.avi', '.mov', '.webm', '.mkv']:
            cap = cv2.VideoCapture(tmp_path)
            if not cap.isOpened():
                print("❌ Failed to open video:", tmp_path)
                os.remove(tmp_path)
                return jsonify({'feedback': 'Could not open video. Try a different format or smaller size.'}), 400

            print("🎥 Opened video:", tmp_path)
            print("🎞 Frame size:", cap.get(cv2.CAP_PROP_FRAME_WIDTH), "x", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print("⏱ FPS:", cap.get(cv2.CAP_PROP_FPS))

            frame_count = 0
            max_frames = 30

            while cap.isOpened() and frame_count < max_frames:
                ret, frame = cap.read()
                print(f"📸 Frame {frame_count}: Read successful? {ret}")
                if not ret:
                    break

                if frame is None:
                    print("⚠️ Frame is None")
                    continue

                feedback = analyze_frame(frame)
                print(f"🔍 Feedback from frame {frame_count}: {feedback}")
                feedback_list.append(feedback)
                frame_count += 1
            cap.release()

        # ✅ Image processing
        elif file_ext in ['.jpg', '.jpeg', '.png', '.webp', '.jfif']:
            frame = cv2.imread(tmp_path)
            if frame is None:
                return jsonify({'feedback': 'Image could not be read. Please try a different one.'}), 400
            feedback = analyze_frame(frame)
            feedback_list.append(feedback)

        else:
            return jsonify({'feedback': 'Unsupported file type'}), 400

    finally:
        os.remove(tmp_path)

    print("📤 Final feedback list:", feedback_list)

    for fb in feedback_list:
        if "Bad posture" in fb:
            return jsonify({'feedback': fb})
    return jsonify({'feedback': feedback_list[0] if feedback_list else "No feedback"})

# ⚠️ Do NOT use Flask dev server in production
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
