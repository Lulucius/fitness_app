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

    title_label1 = tk.Label(start_screen, text="App Name", font=("Helvetica", 24))
    title_label1.pack(pady=(10, 0))


    image = Image.open("/Users/luciuszha/Desktop/Coding Extras/logo_image.jpg")
    image = image.resize((400, 225))

    image = ImageTk.PhotoImage(image)
    image_label = tk.Label(start_screen, image=image)
    image_label.image = image
    image_label.pack()

    # button1 = tk.Button(start_screen, text= "Enter", font=("Helvetica", 24))
    # button1.pack(pady=(5, 5))

    button_frame = tk.Frame(start_screen)
    button_frame.pack(pady=20)

    push_up_button = tk.Button(button_frame, text="Push-ups", command=lambda: build_exercise_screen(exercise_type='pushups', start_screen=start_screen))
    push_up_button.pack(padx = 10)


    version_label = tk.Label(start_screen, text="ver 0.00010011", font=("Helvetica", 10))
    version_label.pack(pady=(10, 0))


def build_exercise_screen(exercise_type, start_screen, is_left = None):
    if exercise_type == 'pushups':
        print("Pushups")



    

    


root = tk.Tk()
root.title("Exercise Selection")
root.withdraw()






create_start_screen()

root.mainloop()