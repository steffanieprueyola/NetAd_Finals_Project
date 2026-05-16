import cv2
from flask import Flask, Response, render_template_string

app = Flask(__name__)

# Your verified network path and credentials
camera_source = "rtsp://admin:nyawa011306@192.168.1.126:10554/tcp/av0_0"
cap = cv2.VideoCapture(camera_source)

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            # Reconnect logic if network dropped packets
            cap.open(camera_source)
            cv2.waitKey(1000)
            continue

        # Encode frame to JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Stream frame over HTTP multipart chunks
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# 1. Route to serve the basic HTML page
@app.route('/')
def index():
    # Simple HTML template that embeds the video stream route as an image source
    html_template = """
    <html>
        <head>
            <title>School Project - Camera Web Server</title>
        </head>
        <body style="background-color: #222; color: white; text-align: center; font-family: sans-serif;">
            <h1>CCTV Ethernet Network Feed</h1>
            <p>Streaming from: 192.168.1.126:10554</p>
            <div style="margin-top: 20px;">
                <img src="{{ url_for('video_feed') }}" style="border: 4px solid #444; border-radius: 8px; max-width: 80%;">
            </div>
        </body>
    </html>
    """
    return render_template_string(html_template)

# 2. Route that streams the actual MJPEG bytes
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Starts the local development server on Port 5000
    app.run(host='0.0.0.0', port=5000, debug=False)
