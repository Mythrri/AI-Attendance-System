import cv2
import csv
import os
from datetime import datetime

name = input("Enter Your Name: ").strip()
if name == "":
    name = "Student_1"

file_exists = os.path.isfile("attendance.csv")
f = open("attendance.csv", "a", newline="")
writer = csv.writer(f)
if not file_exists:
    writer.writerow(["Name", "Time", "Date"])

print(f"\nWelcome {name}! Camera starting... Press 'q' to exit\n")

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

marked = False

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
        if not marked:
            now = datetime.now()
            writer.writerow([name, now.strftime("%H:%M:%S"), now.strftime("%d-%m-%Y")])
            f.flush()
            print(f"Attendance Marked for {name}")
            marked = True

    status = f"Marked: {name}" if marked else "Show Face to Mark"
    cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    cv2.imshow("AI Attendance - Press q to exit", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
f.close()