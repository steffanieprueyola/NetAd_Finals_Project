import cv2

# CHANGE THIS depending on your camera
# 0 = laptop webcam
# or "rtsp://username:password@ip_address:554/stream"
camera_source = "rtsp://admin:nyawa011306@192.168.1.126:10554/tcp/av0_0"

cap = cv2.VideoCapture(camera_source)

def generate_frames():

    while True:
        success, frame = cap.read()

        if not success:
            break

        # encode frame to JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # stream frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
