import os
import time

from flask import request, jsonify, Flask
from bicep_curl import analyze_bicep_curl
from plank import analyze_planks
from pushups import analyze_pushups
from downward_facing_dog import analyze_downward_facing_dogs

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.mp4', '.mov']

@app.route('/')
def home():
    return 'Fitness API'

@app.route('/analyze/<exercise_type>', methods=['GET', 'POST']) # route for uploading image
def edit_video(exercise_type):
    uploaded_video = request.files.getlist("video1")[0]
    video1_filename = uploaded_video.filename
    url = ''

    if video1_filename != '':
        _, video_file_ext = os.path.splitext(video1_filename)
        uploaded_video.save(video1_filename)

        if exercise_type == 'pushups':
            url = analyze_pushups(video_path=video1_filename, is_showed = False)
        elif exercise_tpe == 'plank':
            url = analyze_planks(video_path=video1_filename, is_showed = False)
        elif exercise_tpe == 'bicep_curl':
            url = analyze_bicep_curl(video_path=video1_filename, is_showed = False)
        elif exercise_tpe == 'downward_facing_dog':
            url = analyze_downward_facing_dogs(video_path=video1_filename, is_showed = False)

        if os.path.isfile(video1_filename):
            os.remove(video1_filename)
        return jsonify(url)
    
    return jsonify('')

if __name__ == "__main__":
    app.run(host='0.0.0.0')