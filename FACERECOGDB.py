import cv2
import os
import face_recognition
import pickle
import datetime
import mysql.connector

# Initialize MySQL database connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Darian123123',
    database='matched_faces'
)
cursor = conn.cursor()


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

while True:
    success, img = cap.read()

    # Resize the image for faster processing
    imgS = cv2.resize(img, None, fx=0.25, fy=0.25)
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

            # Insert into the database
            cursor.execute('INSERT INTO faces (face_id, timestamp)VALUES (%s, %s)', (name, timestamp))
            conn.commit()
        else:
            # Unknown face
            print('Unknown face detected')

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