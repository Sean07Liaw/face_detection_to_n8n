import cv2
import time
import os
import requests
import mediapipe as mp

# 1. 偵測與上傳設定
WEBHOOK_URL = "https://你的-n8n-host/webhook/camera‐capture"   # 替換為你的 n8n Webhook URL
COOLDOWN_SECONDS = 1  # 當偵測到人臉後，暫停多少秒再偵測下一次

# 2. 初始化 MediaPipe 人臉偵測
mp_face_detection = mp.solutions.face_detection
mp_drawing       = mp.solutions.drawing_utils

face_detector = mp_face_detection.FaceDetection(
    model_selection=0,           # 模型選擇（0或1，0為短距離/一般使用） :contentReference[oaicite:2]{index=2}
    min_detection_confidence=0.5 # 偵測信心度門檻
)

def send_image_to_webhook(image_path):
    """將影像檔案上傳到 n8n Webhook 的函式"""
    with open(image_path, 'rb') as f:
        files = {'image': (os.path.basename(image_path), f, 'image/jpeg')}
        try:
            resp = requests.post(WEBHOOK_URL, files=files)
            print("上傳狀態碼：", resp.status_code, "回傳內容：", resp.text)
        except Exception as e:
            print("上傳失敗：", e)

def main():
    # 3. 開啟預設攝影機
    cap = cv2.VideoCapture(0)
    time.sleep(2.0)  # 給攝影機暖機時間，讓影像穩定

    if not cap.isOpened():
        print("無法開啟攝影機")
        return

    last_upload_time = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("讀取影格失敗，跳出迴圈")
                break

            # 4. 將影格轉為 RGB（MediaPipe 要求）並進行偵測
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results   = face_detector.process(image_rgb)

            # 5. 如果偵測到至少一張人臉，且冷卻時間已過
            if results.detections and (time.time() - last_upload_time) > COOLDOWN_SECONDS:
                print(f"偵測到 {len(results.detections)} 張人臉 – 擷取影像並上傳")

                # 6. 儲存當前影格作為 JPEG 檔案
                timestamp  = int(time.time())
                filename   = f"face_capture_{timestamp}.jpg"
                cv2.imwrite(filename, frame)

                # 7. 呼叫上傳函式
                # send_image_to_webhook(filename)
                os.remove(filename)  # 上傳後刪除本地檔案

                # 8. 更新最後上傳時間
                last_upload_time = time.time()

                # (選項) 若想畫出偵測框，可使用：
                for detection in results.detections:
                    mp_drawing.draw_detection(frame, detection)
                cv2.imshow("Face Detected", frame)
                # 暫停一下顯示，避免重複
                cv2.waitKey(2000)

            # 9. 顯示影像預覽（可在 Windows 測試時使用）
            cv2.imshow("Camera", frame)

            # 10. 檢查是否按下 q 鍵退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("按下 q 鍵，退出程式")
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        face_detector.close()

if __name__ == "__main__":
    main()
