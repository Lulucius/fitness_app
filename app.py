import tkinter as tk

import cv2
from PIL import Image, ImageTk

from bicep_curl import BicepCurl
from downward_facing_dog import Downward_facing_dog
from plank import Plank
from pushups import PushUp

def start_exercise(exercise_type):
    print(f"Starting {exercise_type} exercise...")

def create_start_screen():
    start_screen = tk.Toplevel()
    start_screen.title("Start Screen")

    start_screen.geometry("500x700")
    start_screen.configure(bg="white")

    title_label1 = tk.Label(start_screen, text="FitPose", font=("Helvetica", 30))

    title_label1.pack(pady=(20, 10))


    image = Image.open("/Users/luciuszha/Downloads/dumbell_logo.jpeg")
    image = image.resize((400, 225))

    image = ImageTk.PhotoImage(image)
    image_label = tk.Label(start_screen, image=image)
    image_label.image = image
    image_label.pack()

    # button1 = tk.Button(start_screen, text= "Enter", font=("Helvetica", 24))
    # button1.pack(pady=(5, 5))

    button_frame = tk.Frame(start_screen)
    button_frame.pack(pady=20)

    push_up_button = tk.Button(button_frame, text="Pushups", command=lambda: build_exercise_screen(exercise_type='pushups', start_screen=start_screen), fg="black")
    push_up_button.config(height = 2, width = 100)
    push_up_button.config(font = ("Helvetica", 22))
    push_up_button.pack(pady = (0, 10))
    push_up_button.config(bg="black")

    bicep_curl_button = tk.Button(button_frame, text="Bicep Curls", command=lambda: build_exercise_screen(exercise_type='bicep_curl', start_screen=start_screen))
    bicep_curl_button.config(height = 2, width = 100)
    bicep_curl_button.config(font = ("Helvetica", 22))
    bicep_curl_button.pack(pady = 10)

    plank_button = tk.Button(button_frame, text="Planks", command=lambda: build_exercise_screen(exercise_type='plank', start_screen=start_screen))
    plank_button.config(height = 2, width = 100)
    plank_button.config(font = ("Helvetica", 22))
    plank_button.pack(pady = 10)

    downward_facing_dog_button = tk.Button(button_frame, text="Downward Facing Dog", command=lambda: build_exercise_screen(exercise_type='downward_facing_dog', start_screen=start_screen))
    downward_facing_dog_button.config(height = 2, width = 100)
    downward_facing_dog_button.config(font = ("Helvetica", 22))
    downward_facing_dog_button.pack(pady = 10)


    version_label = tk.Label(start_screen, text="ver 0.00010011", font=("Helvetica", 10))
    version_label.pack(pady=(10, 0))


def build_exercise_screen(exercise_type, start_screen, is_left = None):
    global is_start
    is_start = False

    if exercise_type == 'pushups':
        analyzer = PushUp()
    elif exercise_type == 'plank':
        analyzer = Plank()
    elif exercise_type == 'bicep_curl':
        analyzer = BicepCurl()
    elif exercise_type == 'downward_facing_dog':
        analyzer = Downward_facing_dog()
    
    # Function to update the canvas with webcame feed
    def start():
        global is_start
        is_start = True
    
    def update():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            if is_start:
                frame = analyzer.process_image(frame, n_frame_in_two_sec, is_left)
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                canvas.create_image(0,0, image=photo, anchor = tk.NW)
                canvas.photo = photo
        exercise_screen.after(10, update)

    exercise_screen = tk.Toplevel()
    exercise_screen.title(f"{exercise_type} Exercise")
    exercise_screen.geometry("800x600")

    # canvas for webcam feed
    canvas = tk.Canvas(exercise_screen, width=640, height=480)
    canvas.pack()
    # opens up webcam
    cap = cv2.VideoCapture(0)
    fps = cap.get(cv2.CAP_PROP_FPS)
    n_frame_in_two_sec = 2 * fps

    # create frame for buttons
    button_frame = tk.Frame(exercise_screen)
    button_frame.pack(side=tk.LEFT, padx = 10)

    # create button to start exercise
    start_button = tk.Button(button_frame, text="Start Exercise", command=start)
    start_button.pack(side=tk.LEFT, padx = 10)

    update()
    exercise_screen.mainloop()
    start_screen.withdraw()

    cap.release()
    cv2.destroyAllWindows()

    def go_back_to_start(exercise_screen, start_screen):
        exercise_screen.destroy()
        start_screen.deiconify()

root = tk.Tk()
root.title("Exercise Selection")
root.withdraw()






create_start_screen()

root.mainloop()