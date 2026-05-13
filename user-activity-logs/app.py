from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import cv2

app = Flask(__name__)
socketio = SocketIO(app)

# CCTV / IP Camera URL
camera_url = "rtsp:// " #url

cap = cv2.VideoCapture(camera_url)

# Generate camera frames
def generate_frames():
    while True:
        success, frame = cap.read()

        if not success:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Main dashboard
@app.route('/')
def index():
    return render_template('index.html')

# Video stream route
@app.route('/video')
def video():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

# Run server
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
