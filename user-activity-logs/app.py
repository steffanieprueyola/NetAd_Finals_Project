from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import cv2
import datetime
import os

os.makedirs("logs", exist_ok=True)

app = Flask(__name__)
socketio = SocketIO(app)

def write_log(event_type, message):
    with open("logs/activity.log", "a") as f:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{time} | {event_type} | {message}\n")

        socketio.emit("log_event", {
            "type": event_type,
            "message": message,
            "time": time
        })

camera_url = "rtsp://CAMERA_IP"
cap = cv2.VideoCapture(camera_url)

def generate_frames():
    while True:
        success, frame = cap.read()

        if not success:
            continue

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/")
def index():
    write_log("VIEW", "Dashboard opened")
    return render_template("index.html")

@app.route("/video")
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
