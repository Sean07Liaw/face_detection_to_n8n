import cv2
import time
import os

def show_bounded_faces(frame, faces):
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Face Detection", frame)
    cv2.waitKey(1)

def detect_face(show_img=False, detection_threshold=30, sharp_threshold=10.0):
    # 1. 載入人臉級聯檔案
    cascade_path = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    relative_cascade_path = os.path.relpath(cascade_path, script_dir)
    face_cascade = cv2.CascadeClassifier(relative_cascade_path)
    if face_cascade.empty():
        print("Failed to load face cascade file")
        return

    try:
        # 2. 開啟攝影機（0 為預設攝影機）
        cap = cv2.VideoCapture(0)
        time.sleep(2.0)  # 銜接攝影機暖機時間

        if not cap.isOpened():
            print("Cannot open camera")
            return

        detected_list = [False] * detection_threshold
        i = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame, exiting")
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

            if show_img:
                show_bounded_faces(frame, faces)

            detected = False
            if len(faces) > 0:
                detected_list[i] = True
                i += 1
                i = i % detection_threshold
                detected = all(detected_list)

            if detected:
                # 6. 如果偵測到人臉，取最大人臉並檢查是否模糊
                areas = [w * h for (x, y, w, h) in faces]
                index_of_largest = areas.index(max(areas))
                (x, y, w, h) = faces[index_of_largest]
                cut_face = frame[y:y+h, x:x+w]
                sharp_value = cv2.Laplacian(cut_face, cv2.CV_64F).var()
                # print("Sharpness value:", sharp_value)
                if sharp_value > sharp_threshold:
                    print("Face detected!")
                    return [frame, faces]  # exit after detecting a face

            # 7. 按 q 鍵退出
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("按下 q 鍵，退出")
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    face_frame = detect_face(show_img=True,sharp_threshold=1900.0)
    show_bounded_faces(face_frame[0], face_frame[1])
    cv2.waitKey(0)