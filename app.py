from flask import Flask, render_template, Response
from flask_socketio import SocketIO
from camera.stream import generate_frames
import cv2
import datetime
import os

os.makedirs("logs", exist_ok=True)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

def write_log(event_type, message):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"{time} | {event_type} | {message}\n"

    # Save to file
    with open("logs/activity.log", "a") as f:
        f.write(log_entry)

    # SEND TO FRONTEND (REAL-TIME)
    socketio.emit("log_event", {
        "time": time,
        "type": event_type,
        "message": message
    })

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
