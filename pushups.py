import time
from pathlib import Path

import cv2
import numpy as np

import pose_module as pm
from firebase import upload_video

def analyze_pushups(video_path=0, is_showed=True):
    cap = cv2.VideoCapture(video_path)
    output_path = Path(video_path).stem + '_output.mp4'
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = 720
    height = 480
    out = cv2.VideoWriter(output_path, cv2.VideoWriter.fourcc('m', 'p', '4','v'), fps, (width, height))
    n_frame_in_two_sec = 2 * fps

    pushup = PushUp()

    while True:
        success, img = cap.read()
        if not success:
            break

        img = pushup.process_image(img, n_frame_in_two_sec)
        print(img.shape)
        out.write(img)

        if is_showed:
            cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    out.release()
    print("Released")
    final_url = upload_video(output_path)
    return final_url

class PushUp:
    def __init__(self):
        self.detector = pm.PoseDetector()
        self.count = 0
        self.prev_count = 0
        self.direction = 0
        self.prev_per = 0
        self.e = 0
        self.d = 0
        self.error_messages = []
        self.error_times = []

    def process_image(self, img, n_frame_in_two_sec, _=None):
        img = cv2.resize(img, (800, 600))
        img = self.detector.find_pose(img, False)
        lmList = self.detector.find_position(img, False)

        if len(lmList) != 0:
            elbowAngle = self.detector.find_angle(img, 12, 14, 16)
            buttAngle = self.detector.find_angle(img, 12, 24, 26)
            legAngle = self.detector.find_angle(img, 24, 26, 28)

            percent = np.interp(elbowAngle, (80, 160), (100, 0))

            # check for errors
            if self.direction == 0:
                if legAngle < 160:
                    self.d += 1
                    if self.d == n_frame_in_two_sec:
                        self.error_messages.append("Make your legs straighter")
                        self.error_times.append(time.time())
                        self.d = 0

                if buttAngle < 155:
                    self.d += 1
                    if self.d == n_frame_in_two_sec:
                        self.error_messages.append("Make your back straight")
                        self.error_times.append(time.time())
                        self.d = 0

                if self.prev_per > percent:
                    self.e += 1
                    if self.e == n_frame_in_two_sec:
                        self.error_messages.append("Bring your chest closer to the ground")
                        self.error_times.append(time.time())
                        self.e = 0

            if self.direction == 1:
                if legAngle < 160:
                    self.d += 1
                    if self.d == n_frame_in_two_sec:
                        self.error_messages.append("Make your legs straighter")
                        self.error_times.append(time.time())
                        self.d = 0

                if buttAngle < 155:
                    self.d += 1
                    if self.d == n_frame_in_two_sec:
                        self.error_messages.append("Make your back straight")
                        self.error_times.append(time.time())
                        self.d = 0

                if self.prev_per > percent:
                    self.e += 1
                    if self.e == n_frame_in_two_sec:
                        self.error_messages.append("Higher! Straighten your hands!")
                        self.error_times.append(time.time())
                        self.e = 0
            
            if elbowAngle <= 70:
                if self.direction == 0:
                    self.count += 0.5
                    self.direction = 1
                
            if elbowAngle >= 165:
                if self.direction == 1:
                    self.count += 0.5
                    self.direction = 0
            
            if self.prev_count != int(self.count):
                self.prev_count = int(self.count)

        # Display error messages for 1 second
        current_time = time.time()
        
        for i in range(len(self.error_times) -1, -1, -1):
            if current_time - self.error_times[i] >= 2.0:
                del self.error_messages[i]
                del self.error_times[i]
        
        for i, error in enumerate(self.error_messages):
            cv2.putText(img, error, (00,185), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 4)
            cv2.putText(img, str(self.count), (600, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 4)
        return img
    