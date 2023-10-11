#importing necessary libraries
import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import time

face_count = 0
face_name = ""
cap = None
face_cascade = None
video_label = None
output_dir = "detected_faces"
os.makedirs(output_dir, exist_ok=True)
# data file to record the data
data_file = open("detected_faces_data.txt", "a")



# To update the video and data feed
def update_video():
    global face_count, cap, face_cascade, video_label

    ret, frame = cap.read()

    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Adjust the cropping area to include more of the detected face
            x -= int(w * 0.1)
            y -= int(h * 0.1)
            w = int(w * 1.2)
            h = int(h * 1.2)

            # Make sure the cropping area is within the frame boundaries
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if x + w > frame.shape[1]:
                w = frame.shape[1] - x
            if y + h > frame.shape[0]:
                h = frame.shape[0] - y

            # Cropping and saving the detected face
            detected_face = frame[y:y + h, x:x + w]
            face_filename = os.path.join(output_dir, f"face_{face_count}.jpg")
            cv2.imwrite(face_filename, detected_face)

        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

    root.after(10, update_video)  # Update video feed every 10ms

def record_name():
    global face_count, data_file, success_label

    # Get the name entered by the user
    detected_name = name_entry.get()

    if detected_name:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        data_file.write(f"Name: {detected_name}, Face {face_count} detected at {timestamp}\n")
        face_count += 1

        # Display a success message
        success_label.config(text="Name recorded successfully!")
