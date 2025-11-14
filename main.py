import cv2
import requests
import tempfile
import os

# 1. 抓攝影機
cap = cv2.VideoCapture(0)  # 0 為預設攝影機
ret, frame = cap.read()
cap.release()

if not ret:
    print("無法從攝影機擷取影像")
    exit(1)

# 2. 存為臨時檔案（JPEG）
tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
filename = tmp.name
cv2.imwrite(filename, frame)
tmp.close()

# 3. 發送到 n8n Webhook
webhook_url = "http://localhost:5678/webhook-test/a02d92ef-05ae-4821-8909-41e6aa096444"
with open(filename, 'rb') as f:
    files = {'image': (os.path.basename(filename), f, 'image/jpeg')}
    try:
        resp = requests.post(webhook_url, files=files)
        print("回傳狀態碼：", resp.status_code)
        print("回傳內容：", resp.text)
    except Exception as e:
        print("發送失敗：", e)

# 4. 刪除臨時檔案
os.remove(filename)
