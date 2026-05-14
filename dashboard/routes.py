from flask import render_template, session, redirect, url_for, Response
from dashboard import dashboard_bp
from flask_socketio import emit
import cv2
import time
import datetime
from extensions import socketio

# ---------------- LOGIN PROTECTION ----------------
@dashboard_bp.route("/dashboard")
def home():
    if "user" not in session:
        return redirect(url_for("auth.login_page"))

    return render_template("index.html")


# ---------------- CAMERA ----------------
cameras = {0: 0}

def gen_frames():
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        if not success:
            break

        _, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    cap.release()


@dashboard_bp.route("/video_feed/0")
def video_feed():
    return Response(
        gen_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# ---------------- REAL TIME LOGS ----------------
def generate_logs():
    logs = [
        {"message": "Motion detected", "type": "warning"},
        {"message": "Camera stable", "type": "success"},
        {"message": "Unauthorized access", "type": "danger"},
        {"message": "System running", "type": "info"}
    ]

    while True:
        log = logs[int(time.time()) % len(logs)]

        socketio.emit("new_log", {
            "message": log["message"],
            "type": log["type"],
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        time.sleep(3)


# start background logs
socketio.start_background_task(generate_logs)
