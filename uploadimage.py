import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import shutil
import os

my_w = tk.Tk()
my_w.geometry("900x600")
my_w.title('Upload, Capture & Display Images')

cap = cv2.VideoCapture(0)

def capture_image():
    ret, frame = cap.read()
    cv2.imwrite("captured_image.png", frame)
    

def upload_file():
    f_types = [('Jpg Files', '*.jpg'), ('PNG Files', '*.png')]
    filenames = tk.filedialog.askopenfilenames(multiple=True, filetypes=f_types)
    destination_folder = "Py/images"  # Define your destination folder here
    
    col = 1
    row = 3
    
    for f in filenames:
        img = Image.open(f)
        img = img.resize((150, 150))
        img = ImageTk.PhotoImage(img)
        e1 = tk.Label(my_w)
        e1.grid(row=row, column=col)
        e1.image = img
        e1['image'] = img
        
        if col == 3:
            row += 1
            col = 1
        else:
            col += 1
        
        # Copy the uploaded file to the destination folder
        shutil.copy(f, destination_folder)

b1 = tk.Button(my_w, text='Upload Files', width=20, command=upload_file)
b1.place(x=10,y=10)

capture_btn = tk.Button(my_w, text='Capture Image', width=20, command=capture_image)
capture_btn.place(x=180,y=10)

my_w.mainloop()
