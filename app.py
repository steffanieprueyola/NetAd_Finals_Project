from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO
import cv2
import datetime
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading", logger=True, engineio_logger=True)

# Camera storage
cameras = {
    0: 0  # Local webcam
}

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

        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' +
                frame +
                b'\r\n'
            )

# ROUTES

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed/<int:id>/')
def video_feed(id):
    return Response(
        gen_frames(id),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

# REAL-TIME LOG GENERATOR

def generate_logs():

    sample_logs = [
        {"message": "Motion detected at Camera 1", "type": "warning"},
        {"message": "Unauthorized access attempt", "type": "danger"},
        {"message": "Camera connection stable", "type": "success"},
        {"message": "Person detected in restricted area", "type": "warning"},
        {"message": "Face recognition triggered", "type": "info"},
        {"message": "Low light detected", "type": "warning"},
        {"message": "System scan completed", "type": "success"},
        {"message": "Object movement detected", "type": "info"}
    ]

    while True:

        current_log = sample_logs[int(time.time()) % len(sample_logs)]

        log = {
            "message": current_log["message"],
            "type": current_log["type"],
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        socketio.emit('new_log', log)

        time.sleep(3)
        
# START BACKGROUND THREAD

socketio.start_background_task(target=generate_logs)

if __name__ == '__main__':
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        allow_unsafe_werkzeug=True
    )
