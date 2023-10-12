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



capture_count = 0

def update_video():
    global face_count, cap, face_cascade, video_label, face_name

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
            if face_name != "":
                face_filename = os.path.join(output_dir, f"{face_name}_{capture_count}.jpg")
                cv2.imwrite(face_filename, detected_face)

        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

    root.after(1, update_video)  # Update video feed every 10ms

# Recording the data of the corresponding face
def record_name():
    global face_count, data_file, success_label, face_name, capture_count

    # Get the name entered by the user
    detected_name = name_entry.get()

    if detected_name:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        data_file.write(f"Name: {detected_name}, Face {face_count} detected at {timestamp}\n")
        face_count += 1
        face_name = detected_name

        # Capture and save five images of the user
        capture_count = 0
        while capture_count < 5:
            time.sleep(1)  # Delay for stability
            capture_count += 1
            success_label.config(text=f"Captured {capture_count} images")
            root.update()
            if capture_count == 5:
                success_label.config(text="Name recorded successfully!")


# Recording the data of the corresponding face
def record_name():
    global face_count, data_file, success_label, face_name, capture_count

    # Get the name entered by the user
    detected_name = name_entry.get()

    if detected_name:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        data_file.write(f"Name: {detected_name}, Face {face_count} detected at {timestamp}\n")
        face_count += 1
        face_name = detected_name

        # Capture and save five images of the user
        capture_count = 0
        while capture_count < 5:
            time.sleep(1)  # Delay for stability
            capture_count += 1
            success_label.config(text=f"Captured {capture_count} images")
            root.update()
            if capture_count == 5:
                success_label.config(text="Name recorded successfully!")



# main window Interface Design

root = tk.Tk()
root.title("Face Detection")

#Styling for the components of the GUI
style = ttk.Style()
style.configure("TButton", font=("Courier New", 12, "bold"), foreground="white", background="green",
                padding=(10, 5))
style.configure("TLabel", font=("Courier New", 12, "bold"))
style.configure("TEntry", font=("Courier New", 12, "bold"))
root.configure(background="light green")

video_label = ttk.Label(root)
video_label.pack()

# Form for entering data
name_label = ttk.Label(root, text="Enter your name:")
name_label.pack()
name_entry = ttk.Entry(root)
name_entry.pack()


record_button = ttk.Button(root, text="Record Name", command=record_name, style="TButton")  # Apply button style
record_button.pack()

success_label = ttk.Label(root, text="")
success_label.pack()


cap = cv2.VideoCapture(0)

# Haar Cascade Classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Create an exit button
exit_button = ttk.Button(root, text="Exit", command=root.quit, style="TButton")
exit_button.pack()


update_video()

root.mainloop()

# Release the camera and close the data file when the application is closed
cap.release()
data_file.close()
cv2.destroyAllWindows()
