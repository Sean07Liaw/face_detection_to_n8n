import cv2
import threading
import motion_detect
import Haar_cascade
import picture_upload
import receive_from_n8n

def main():
    if motion_detect.motion_detect():
        face = Haar_cascade.detect_face(True)

    Haar_cascade.show_bounded_faces(face[0], face[1])
    cv2.waitKey(1)

    picture_upload.upload_to_n8n(face[0])

    receive_from_n8n.run_server()

    print("等待 webhook 資料...")
    try:
        # 等 webhook 資料，最多等 120 秒
        data = receive_from_n8n.get_received_data(timeout=120)
        print("main.py 收到資料：", data)
    except Exception as e:
        print("等 webhook 資料超時或發生錯誤：", e)

    receive_from_n8n.shutdown_server()

if __name__ == "__main__":
    main()