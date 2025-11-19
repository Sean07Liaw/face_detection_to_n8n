import cv2
import time
import os

def main():
    # 1. 載入人臉級聯檔案
    cascade_path = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    relative_cascade_path = os.path.relpath(cascade_path, script_dir)
    face_cascade = cv2.CascadeClassifier(relative_cascade_path)
    if face_cascade.empty():
        print("載入人臉級聯檔案失敗")
        return

    # 2. 開啟攝影機（0 為預設攝影機）
    cap = cv2.VideoCapture(0)
    time.sleep(2.0)  # 銜接攝影機暖機時間

    if not cap.isOpened():
        print("無法開啟攝影機")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("讀取影格失敗，跳出")
            break

        # 3. 預處理：將影格轉為灰階
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 4. 偵測人臉
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # 5. 如果偵測到人臉，畫框
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 6. 顯示影格
        cv2.imshow("Face Detection", frame)

        # 7. 按 q 鍵退出
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("按下 q 鍵，退出")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
