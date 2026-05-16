from flask import Flask, Response
from flask_socketio import SocketIO
import cv2
import datetime
import time

from auth.routes import auth_bp
from dashboard.routes import dashboard_bp

app = Flask(__name__)

# SECRET KEY
app.config["SECRET_KEY"] = "change-this-secret-key"

# SOCKET IO
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading"
)

# REGISTER BLUEPRINTS
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

# =========================================
# CAMERA SOURCE
# =========================================

# LOCAL WEBCAM TEST
# cameras = {
#     0: 0
# }

# RTSP CAMERA TEST
cameras = {
    0: "rtsp://username:password@192.168.1.100:554/stream"
}

# Example IP Webcam
# cameras = {
#     0: "http://192.168.1.5:8080/video"
# }

# =========================================
# CAMERA FUNCTIONS
# =========================================

def find_camera(camera_id):
    try:
        return cameras.get(int(camera_id))
    except:
        return None

def gen_frames(camera_id):

    cam = find_camera(camera_id)

    if cam is None:
        print("Camera not found")
        return

    print(f"Opening camera stream: {cam}")

    cap = cv2.VideoCapture(cam)

    if not cap.isOpened():
        print("FAILED TO OPEN CAMERA")
        return

    while True:

        success, frame = cap.read()

        if not success:
            print("FAILED TO READ FRAME")
            break

        _, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            frame +
            b"\r\n"
        )

# =========================================
# VIDEO FEED ROUTE
# =========================================

@app.route("/video_feed/<int:id>/")
def video_feed(id):

    return Response(
        gen_frames(id),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

# =========================================
# REAL-TIME LOGS
# =========================================

def generate_logs():

    sample_logs = [
        {"message": "Motion detected at Camera 1", "type": "warning"},
        {"message": "Unauthorized access attempt", "type": "danger"},
        {"message": "Camera connection stable", "type": "success"},
        {"message": "Face recognition triggered", "type": "info"},
        {"message": "Low light detected", "type": "warning"},
        {"message": "Object movement detected", "type": "info"}
    ]

    while True:

        current_log = sample_logs[int(time.time()) % len(sample_logs)]

        log = {
            "message": current_log["message"],
            "type": current_log["type"],
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        socketio.emit("new_log", log)

        time.sleep(3)

# START LOG THREAD
socketio.start_background_task(generate_logs)

# =========================================
# RUN APP
# =========================================

if __name__ == "__main__":

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        allow_unsafe_werkzeug=True
    )
