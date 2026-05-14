from flask import Flask, render_template, Response, request
import cv2
import os

app = Flask(__name__)

# In-memory camera configurations: ideally, a database or persistent storage should be used.
cameras = {}

def find_camera(id):
    try:
        return cameras[int(id)]
    except (IndexError, ValueError):
        return None

def gen_frames(camera_id):
    cam = find_camera(camera_id)
    if not cam:
        raise Exception("Camera not found or not connected.")

    cap = cv2.VideoCapture(cam)

    while True:
        # Capture frame-by-frame
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

@app.route('/video_feed/<string:id>/', methods=["GET"])
def video_feed(id):
    """Video streaming route. Put this in the src attribute of an img tag."""
    try:
        return Response(gen_frames(id),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/add_camera', methods=["POST"])
def add_camera():
    ip_address = request.form.get('ip_address')
    username = request.form.get('username')
    password = request.form.get('password')
    if ip_address and username and password:
        # Assuming we create a camera stream URL like so.
        stream_url = f'rtsp://{username}:{password}@{ip_address}/...'
        cameras[len(cameras)] = stream_url  # Store camera
  
        return {"success": True, "message": "Camera added successfully."}
    else:
        return {"success": False, "message": "Failed to add camera."}

if __name__ == '__main__':
    # Secure the application by ensuring it listens on the proper host and port
    app.run(host='0.0.0.0', port=5000)
