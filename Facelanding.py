from tkinter import *
from tkinter import messagebox
import ast
import cv2
import os
import face_recognition
import pickle
import datetime
import mysql.connector
from tkinter import ttk
import tkinter as tk

root=Tk()
root.title('Landing page')
root.geometry('903x603')
root.config(bg="#fff")
root.resizable(False,False)

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Darian123123',
    database='matched_faces'
)

cursor = conn.cursor()

def Database_display():
    root = Tk()
    root.title('Database Table Viewer')

    # Display the table
    tree = ttk.Treeview(root, columns=('face_id', 'timestamp', 'location'), show='headings',)
    tree.heading('face_id', text='ID')
    tree.heading('timestamp', text='Timestamp')
    tree.heading('location', text='Location')
    tree.pack(padx=10, pady=10)
    
    
    # Clear previous data in the table
    for row in tree.get_children():
        tree.delete(row)

        # Establish connection to the MySQL database
    conn = mysql.connector.connect(user='root', password='Darian123123', host='localhost', database='matched_faces')
    cursor = conn.cursor()

        # Execute SQL query to retrieve data
    cursor.execute('SELECT face_id, timestamp, location FROM faces ORDER BY timestamp DESC')
    rows = cursor.fetchall()

        # Insert retrieved data into the Treeview
    for row in rows:
        tree.insert('', 'end', values=(row[0], row[1], row[2]))
        
    def item_selected(event):
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']


    tree.bind('<<TreeviewSelect>>', item_selected)

    tree.grid(row=0, column=0, sticky='nsew')

    scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')
        # Close the database connection
    conn.close()

    
    # Run the Tkinter main loop
    root.mainloop()

# Initialize the video capture object

date = datetime.datetime.now()
cap = cv2.VideoCapture(0)  # Use camera index 0 (default camera)
if not cap.isOpened():
    print('Error: Camera not found')
    exit()

# Load known face encodings and IDs from a pickle file
print('Loading known face encodings')
with open('encodefile.p', 'rb') as file:
    encodinglistknown, ids = pickle.load(file)
print('Known face encodings loaded')



def camera():

    while True:
        success, img = cap.read()

        # Resize the image for faster processing
        imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        # Detect faces in the current frame and encode them
        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        # Compare detected face encodings with known encodings
        for encodeface, faceloc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodinglistknown, encodeface)
            faceDis = face_recognition.face_distance(encodinglistknown, encodeface)

            # Find the index of the best match
            best_match_index = faceDis.argmin()

            if matches[best_match_index]:
                # A known face is detected
                name = ids[best_match_index]
                print(f'Matched face with ID: {name}')                   
                timestamp = datetime.datetime.now()
                location = ('Entrace')
               
                # Insert into the database
                cursor.execute('INSERT INTO faces (face_id, timestamp, location)VALUES (%s, %s, %s)', (name, timestamp, location))
                conn.commit() 
            else:
                # Unknown face
                print('Unknown')
                cursor.execute('INSERT INTO faces (face_id, timestamp, location)VALUES (%s, %s, %s)', (name, timestamp, location))
                conn.commit() 
        
        # Display the image
        cv2.imshow('Face Recognition', img)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

    # Close the database connection
    conn.close()
    
####################################^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Camera^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



img = PhotoImage(file='website_images/PAINT.png')
Label(root,image=img,bg='white').place(x=0,y=0)

frame=Frame(root,width=797,height=34,bg='#1A087C')
frame.place(x=50,y=25)

Home_indicate=Button(frame,width=27,pady=3,text='Home', bg='#56a1f8',fg='white',border=1).place(x=2,y=3)


Home_indicate=Button(frame,width=27,pady=3,text='Profiles/images', bg='#56a1f8',fg='white',border=1).place(x=201,y=3)


Contact_indicate=Button(frame,width=27,pady=3,text='Database', bg='#56a1f8',fg='white',border=1,command=Database_display).place(x=399,y=3)


Home_indicate=Button(frame,width=27,pady=3,text='Camera', bg='#56a1f8',fg='white',border=1,command=camera).place(x=597,y=3)


root.mainloop()