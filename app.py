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


    button1 = tk.Button(start_screen, text= "Log In", font=("Helvetica", 24))
    button1.pack(pady=(500, 5))

    button2 = tk.Button(start_screen, text= "Sign Up", font=("Helvetica", 24))
    button2.pack(pady=(5, 5))


    version_label = tk.Label(start_screen, text="ver 0.00010011", font=("Helvetica", 10))
    version_label.pack(pady=(10, 0))


    

    


root = tk.Tk()
root.title("Exercise Selection")
root.withdraw()






create_start_screen()

root.mainloop()