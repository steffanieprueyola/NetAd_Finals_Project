import cv2

# Replace with your CCTV RTSP URL
camera_url = 0
cap = cv2.VideoCapture(camera_url)

def generate_frames():
    while True:
        success, frame = cap.read()

        if not success:
            continue

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        )
