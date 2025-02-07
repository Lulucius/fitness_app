from pathlib import Path

import cv2
import numpy as np

import pose_module as pm
from firebase import upload_video


def analyze_planks(video_path=0, is_showed=True):
    cap = cv2.VideoCapture(video_path)
    output_path = Path(video_path).stem + '_output.mp4'
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = 720
    height = 480
    out = cv2.VideoWriter(output_path, cv2.VideoWriter.fourcc('m', 'p', '4','v'), fps, (width, height))
    n_frame_in_two_sec = 2 * fps
    
    plank = Plank()

    while True:
        success, img = cap.read()
        if not success:
            break

        img = plank.process_image(img, n_frame_in_two_sec)
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

class Plank:
    def __init__(self):
        # font
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        # fontSacle
        self.fontScale = 0.5
        self.color = (255, 0, 0)
        self.thickness = 1
        self.elbow_error = 0
        self.hip_error = 0
        self.hip_error2 = 0
        self.leg_error = 0
        self.overall_feedback = ''
        self.leg_feedback = ''
        self.elbow_feedback = ''
        self.hip_feedback = ''
        self.hip_feedback2 = ''
        self.detector = pm.PoseDetector()
    
    def process_image(self, img, n_frame_in_two_sec, _=None):
        img = cv2.resize(img, (800, 600))
        img = self.detector.find_pose(img, False)
        lmList = self.detector.find_position(img, False)
        
        if len(lmList) != 0:
            elbowAngle = self.detector.find_angle(img, 12, 14, 16)
            hipAngle = self.detector.find_angle(img, 12, 24, 26)
            legAngle = self.detector.find_angle(img, 24, 26, 28)

            if not 65 <= elbowAngle <= 90:
                self.elbow_error += 1
            if self.elbow_error == n_frame_in_two_sec:
                print("Bring your shoulder vertically above your elbow")
                self.elbow_feedback = "Bring your shoulder vertically above your elboew"
                self.elbow_error = 0


            if hipAngle < 140:
                self.hip_error += 1
            if self.hip_error == n_frame_in_two_sec:
                print("Make your back staight. Bring your buttocks DOWN")
                self.hip_feedback = "Make your back straight. Bring your buttocks DOWN"
                self.hip_error = 0
            
            if hipAngle > 190:
                self.hip_error += 1
            if self.hip_error == n_frame_in_two_sec:
                print("Make your back staight. Bring your buttocks UP")
                self.hip_feedback2 = "Make your back straight. Bring your buttocks UP"
                self.hip_error = 0


            if legAngle < 150:
                self.leg_error += 1
            if self.leg_error == n_frame_in_two_sec:
                print("Make your legs straighter")
                self.leg_feedback = ("Make your legs straighter")
                self.leg_error = 0


            if 65 <= elbowAngle <= 90:
                if 140 < hipAngle < 190:
                    if legAngle >150:
                        print("You have good form")
                        self.overall_feedback = ("You have good form")
                    else:
                        print("There are improvements to be made")
                        self.overall_feedback = ("There are improvements to be made")
                else:           
                    print("There are improvements to be made")
                    self.overall_feedback = ("There are improvements to be made")
            else:
                print("There are improvements to be made")
                self.overall_feedback = ("There are improvements to be made")       


        if self.overall_feedback != '':
            cv2.putText(img, self.overall_feedback, (00,185), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 4)
            return img

        if self.elbow_feedback != '':
            cv2.putText(img, self.elbow_feedback, (00,185), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 4)
            return img
     
        if self.hip_feedback != '':
            cv2.putText(img, self.hip_feedback, (00,185), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 4)  
            return img

        if self.hip_feedback2 != '':
            cv2.putText(img, self.hip_feedback2, (00,185), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 4) 
            return img          


        
                

