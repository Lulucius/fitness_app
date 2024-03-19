from bicep_curl import analyze_bicep_curl
from pushups import analyze_pushups

def analyze_exercise(exercise_type:str, video_path=0, left=True):
    if exercise_type == 'bicep_curl':
        analyze_bicep_curl(video_path="bad_bicep_curl_ex.mov", left=True) 
    if exercise_type == 'pushups':
        analyze_pushups(video_path="pushup2.mov")
    if exercise_type == 'plank':
        analyze_pushups(video_path="plank_video.mp4")
    if exercise_type == 'downward_facing_dog':
        analyze_pushups(video_path="downward_dog2.mp4")
    
