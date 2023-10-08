#importing necessary libraries
import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import time

face_count = 0
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

            # Cropping and saving the detected face
            detected_face = frame[y:y + h, x:x + w]
            face_filename = os.path.join(output_dir, f"face_{face_count}.jpg")
            cv2.imwrite(face_filename, detected_face)

        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

    root.after(10, update_video)  # Update video feed every 10ms
