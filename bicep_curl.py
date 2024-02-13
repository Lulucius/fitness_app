import time
from pathlib import Path

import cv2
import numpy as np

import pose_module as pm
#from firebase import upload_video

def analyze_bicep_curl(video_path=0, left=False, is_showed=True):
    cap = cv2.VideoCapture(video_path)
    output_path = Path(video_path).stem + '_output.mp4'
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = 720
    height = 480
    out = cv2.VideoWriter(output_path, cv2.VideoWriter.fourcc('m', 'p', '4','v'), fps, (width, height))

    bicep = BicepCurl()

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            break
        img = cv2.resize(img, (720, 480))
        img = bicep.process_image(img, left, )

        out.write(img)

        if is_showed:
            cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    out.release()
    # print("Released")
    # final_url = upload_video(output_path)
    # return final_url

class BicepCurl:
    def __init__(self):
        self.count = 0
        self.prev_count = 0
        self.direction = 0  # 0 if going up, 1 if going down
        self.prev_per = 0
        self.e = 0
        self.detector = pm.PoseDetector()
        self.error_messages = []
        self.error_times = []
    
    def process_image (self, img, _, left=False):
        img = self.detector.find_pose(img, False)
        lmList = self.detector.find_position(img, False)

        if len(lmList) != 0:
            if left:
                angle = self.detector.find_angle(img, 11, 13, 15)
            else:
                angle = self.detector.find_angle(img, 11, 13, 15)
            percentage = np.interp(angle, (25, 155), (0, 100))
        

            # check for errors
            if self.direction == 0:
                if self.prev_per > percentage:
                    self.e += 1
                    if self.e == 30:
                        self.error_messages.append("Lift your arm higher")
                        self.error_times.append(time.time())
                        self.e = 0
            
            if self.direction == 1:
                if self.prev_per < percentage:
                    self.e += 1
                    if self.e == 30:
                        self.error_messages.append("Put your arm all the way down")
                        self.error_times.append(time.time())
                        self.e = 0
            
            if percentage == 100:
                if self.direction == 0:
                    self.count += 0.5
                    self.direction = 1
            
            if percentage == 0:
                if self.direction == 1:
                    self.count += 0.5
                    self.direction = 0

            
            self.prev_per = percentage
            if self.prev_count != int(self.count):
                prev_count = int(self.count)

    
        # Display error messages for 1 second
        current_time = time.time()
        
        for i in range(len(self.error_times) -1, -1, -1):
            if current_time - self.error_times[i] >= 2.0:
                del self.error_messages[i]
                del self.error_times[i]
        
        for i, error in enumerate(self.error_messages):
            cv2.putText(img, error, (50, 100 * i * 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 4)
            cv2.putText(img, str(self.count), (600, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 4)
        return img

analyze_bicep_curl("bad_bicep_curl_ex.mov") 