from flask import Flask
from flask_socketio import SocketIO
import cv2
import datetime
import time

# AUTH
from auth.routes import auth_bp

# DASHBOARD
from dashboard.routes import dashboard_bp

# CREATE APP
app = Flask(__name__)

# SECRET KEY
app.config["SECRET_KEY"] = "change-this-secret-key"

# SOCKETIO
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading",
    logger=True,
    engineio_logger=True
)

# REGISTER BLUEPRINTS
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

# CAMERA STORAGE
cameras = {
    0: 0
}

# FIND CAMERA
def find_camera(id):
    try:
        return cameras.get(int(id))
    except:
        return None

# GENERATE FRAMES
def gen_frames(camera_id):

    cam = find_camera(camera_id)

    if cam is None:
        raise Exception("Camera not found.")

    cap = cv2.VideoCapture(cam)

    while True:

        success, frame = cap.read()

        if not success:
            break

        _, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            frame +
            b"\r\n"
        )

    cap.release()

# REAL-TIME LOGS
def generate_logs():

    sample_logs = [
        {
            "message": "Motion detected at Camera 1",
            "type": "warning"
        },
        {
            "message": "Unauthorized access attempt",
            "type": "danger"
        },
        {
            "message": "Camera connection stable",
            "type": "success"
        },
        {
            "message": "Face recognition triggered",
            "type": "info"
        }
    ]

    while True:

        current_log = sample_logs[
            int(time.time()) % len(sample_logs)
        ]

        socketio.emit("new_log", {
            "message": current_log["message"],
            "type": current_log["type"],
            "time": datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        })

        time.sleep(3)

# RUN APP
if __name__ == "__main__":

    # START BACKGROUND TASK HERE
    socketio.start_background_task(generate_logs)

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        allow_unsafe_werkzeug=True
    )
