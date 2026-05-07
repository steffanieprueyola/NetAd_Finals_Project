import cv2
import os
from datetime import datetime

class CameraIntegration:

    def __init__(self, camera_url):
        self.camera_url = camera_url
        self.cap = None

    def connect_camera(self):
        self.cap = cv2.VideoCapture(self.camera_url)

        if not self.cap.isOpened():
            print("ERROR: Cannot connect to camera.")
            return False

        print("Camera connected successfully.")
        return True

    def start_stream(self):

        if self.cap is None:
            print("Camera is not initialized.")
            return

        while True:

            ret, frame = self.cap.read()

            if not ret:
                print("Failed to receive frame.")
                break

            cv2.imshow("IP Camera Live Feed", frame)

            key = cv2.waitKey(1)

            # Press Q to quit
            if key == ord('q'):
                break

            # Press S to save snapshot
            elif key == ord('s'):
                self.save_snapshot(frame)

        self.release_resources()

    def save_snapshot(self, frame):

        if not os.path.exists("snapshots"):
            os.makedirs("snapshots")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"snapshots/snapshot_{timestamp}.jpg"

        cv2.imwrite(filename, frame)

        print(f"Snapshot saved: {filename}")

    def release_resources(self):

        if self.cap:
            self.cap.release()

        cv2.destroyAllWindows()

        print("Camera resources released.")

