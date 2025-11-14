import cv2
import time

def main():
    cap = cv2.VideoCapture(0)  # 開啟預設攝影機
    time.sleep(2.0)  # 給攝影機暖機一點時間

    # 讀取第一張影格當作背景
    ret, frame = cap.read()
    if not ret:
        print("無法讀取攝影機影格")
        cap.release()
        return

    # 將背景轉灰階 + 模糊化
    gray_bg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_bg = cv2.GaussianBlur(gray_bg, (21, 21), 0)

    # 偵測參數
    motion_threshold = 1000  # 閾值：差異像素數量（你可調）
    cooldown_seconds = 2     # 偵測到之後暫停多久再繼續偵測

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 預處理當前影格
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # 計算差異
        diff = cv2.absdiff(gray_bg, gray)
        # 閾值化
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        # 擴張 (dilate) 以填補間隙
        thresh = cv2.dilate(thresh, None, iterations=2)

        # 找輪廓
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        for contour in contours:
            if cv2.contourArea(contour) < motion_threshold:
                continue
            # 若有輪廓面積大於門檻，就認定有移動
            motion_detected = True
            # 可畫框（例如顯示）：
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # 顯示影像（可選，用於測試）
        cv2.imshow("Live", frame)
        cv2.imshow("Thresh", thresh)

        if motion_detected:
            print("偵測到移動！截圖／上傳可在這裡觸發")
            # 這邊你可加上：儲存影格、呼叫上傳函式
            time.sleep(cooldown_seconds)  # 暫停一段時間再繼續偵測

            # 更新背景為當前影格（視情況決定是否更新）
            gray_bg = gray

        # 按 q 鍵退出
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
