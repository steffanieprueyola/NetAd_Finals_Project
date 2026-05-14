from flask import Flask, Response
from flask_socketio import SocketIO
import cv2
import datetime
import time

from auth.routes import auth_bp
from dashboard.routes import dashboard_bp

app = Flask(__name__)

# REQUIRED for login session
app.config["SECRET_KEY"] = "change-this-secret-key"

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading",
    logger=True,
    engineio_logger=True
)

# REGISTER BLUEPRINTS (AUTH + DASHBOARD)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

# Camera storage
cameras = {0: 0}

def find_camera(id):
    try:
        return cameras.get(int(id))
    except:
        return None

def gen_frames(camera_id):
    cam = find_camera(camera_id)

    if cam is None:
        raise Exception("Camera not found.")

    cap = cv2.VideoCapture(cam)

    while True:
        success, frame = cap.read()

        if not success:
            continue

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# BACKGROUND LOGS
def generate_logs():

    sample_logs = [
        {"message": "Motion detected at Camera 1", "type": "warning"},
        {"message": "Unauthorized access attempt", "type": "danger"},
        {"message": "Camera connection stable", "type": "success"},
        {"message": "Face recognition triggered", "type": "info"}
    ]

    while True:
        log = sample_logs[int(time.time()) % len(sample_logs)]

        socketio.emit("new_log", {
            "message": log["message"],
            "type": log["type"],
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        time.sleep(3)

socketio.start_background_task(generate_logs)

if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        allow_unsafe_werkzeug=True
    )
