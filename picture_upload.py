import cv2
import requests
import tempfile
import os

def upload_to_n8n(frame, timeout=10):
    # 1. save frame to a temporary JPEG file
    tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    filename = tmp.name
    cv2.imwrite(filename, frame)
    tmp.close()

    # 2. send to n8n Webhook
    webhook_url = "http://localhost:5678/webhook-test/a02d92ef-05ae-4821-8909-41e6aa096444"
    print("Uploading image to n8n webhook:", webhook_url)
    with open(filename, 'rb') as f:
        files = {'image': (os.path.basename(filename), f, 'image/jpeg')}
        try:
            resp = requests.post(webhook_url, files=files, timeout=timeout)
            print("Response status code:", resp.status_code)
            print("Response content:", resp.text)
            return resp.status_code
        except Exception as e:
            print("Failed to send:", e)
            raise

    # 3. delete the temporary file
    os.remove(filename)


# Example usage: capture a frame from the webcam and upload it
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)  # 0 is the default camera
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Failed to capture image from camera")
        exit(1)

    upload_to_n8n(frame)