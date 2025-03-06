import cv2
import numpy as np
from utils.alert_utils import play_alert
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Load Haar Cascade for face and eye detection
face_cascade = cv2.CascadeClassifier("../data/haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("../data/haarcascade_eye.xml")

# Initialize camera
cap = cv2.VideoCapture(0)
EYE_CLOSED_FRAMES = 20  # Number of frames to detect drowsiness
COUNTER = 0
is_running = False

# Function to start/stop the drowsiness detection
def toggle_detection():
    global is_running
    if is_running:
        is_running = False
        start_button.config(text="Start Detection")
    else:
        is_running = True
        start_button.config(text="Stop Detection")
        detect_drowsiness()

# Function to detect drowsiness
def detect_drowsiness():
    global COUNTER, is_running

    if is_running:
        ret, frame = cap.read()
        if not ret:
            return

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Assume eyes are in the upper half of the face
            roi_gray = gray[y:y+h//2, x:x+w]
            roi_color = frame[y:y+h//2, x:x+w]

            # Detect eyes within the face region
            eyes = eye_cascade.detectMultiScale(roi_gray)

            # If no eyes are detected, increment the counter
            if len(eyes) == 0:
                COUNTER += 1
                if COUNTER >= EYE_CLOSED_FRAMES:
                    print("Drowsiness detected!")
                    play_alert("../assets/alert.wav")  # Play alert sound
            else:
                COUNTER = 0

            # Draw rectangles around the eyes
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

        # Convert the frame to RGB for displaying in Tkinter
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

        # Repeat the function after 10ms
        video_label.after(10, detect_drowsiness)

# Function to release resources and close the app
def on_closing():
    global is_running
    is_running = False
    cap.release()
    root.destroy()

# Create the main Tkinter window
root = tk.Tk()
root.title("Driver Drowsiness Detection")
root.protocol("WM_DELETE_WINDOW", on_closing)

# Create a label to display the video feed
video_label = ttk.Label(root)
video_label.pack(padx=10, pady=10)

# Create a start/stop button
start_button = ttk.Button(root, text="Start Detection", command=toggle_detection)
start_button.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()