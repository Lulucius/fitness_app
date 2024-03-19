import firebase_admin
from firebase_admin import credentials, storage

fb_cred = 'key.json'

cred = credentials.Certificate(fb_cred)
firebase_admin.initialize_app(cred, {
    'storageBucket': "fitnessapplication-ebf52.appspot.com"
})

bucket = storage.bucket()

def upload_video(video_path):
    blob = bucket.blob(video_path)

    if blob.exists():
        print("This file already exists on cloud.")
        print(blob.public_url)
        return blob.public_url
    else:
        outfile = video_path
        blob.upload_from_filename(outfile)
        with open(outfile, 'rb') as fp:
            blob.upload_from_file(fp)
        print("This file is uploaded to cloud.")
        blob.make_public()
        return blob.public_url