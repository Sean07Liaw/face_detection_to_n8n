import cv2
import time

motion_threshold = 1000  # threshold: number of different pixels (you can adjust)

def motion_detect(show_img=False, motion_threshold=motion_threshold):
    try:
        cap = cv2.VideoCapture(0)  # open default camera
        time.sleep(2.0)  # give camera some time to warm up

        if not cap.isOpened():
            print("Cannot open camera")
            return

        # read the first frame as background
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from camera")
            return

        # convert background to grayscale + blur
        gray_bg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_bg = cv2.GaussianBlur(gray_bg, (21, 21), 0)

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame from camera")
                break

            # preprocess current frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # compute difference
            diff = cv2.absdiff(gray_bg, gray)
            # thresholding
            thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
            # dilate to fill in gaps
            thresh = cv2.dilate(thresh, None, iterations=2)

            # find contours
            contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            motion_detected = False
            for contour in contours:
                if cv2.contourArea(contour) < motion_threshold:
                    continue
                # if any contour area is above the threshold, motion is detected
                motion_detected = True
                # optionally draw rectangle (for display purposes):
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            if show_img:
                # display the frames (optional, for testing)
                cv2.imshow("Live", frame)
                cv2.imshow("Thresh", thresh)

            if motion_detected:
                print("Motion detected!")
                return True # exit after detecting motion

            key = cv2.waitKey(1000) & 0xFF
            if key == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    motion_detect(True,)