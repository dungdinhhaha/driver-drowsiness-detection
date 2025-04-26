import cv2
import dlib
import numpy as np
import pygame
import time
import os
from scipy.spatial import distance as dist
from imutils import face_utils

pygame.mixer.init()

try:
    if os.path.exists("sounds/alarm.wav"):
        pygame.mixer.music.load("sounds/alarm.wav")
        print("Alarm sound loaded successfully")
    else:
        print("Warning: Alarm sound file not found at sounds/alarm.wav")
except pygame.error as e:
    print(f"Warning: Could not load alarm sound: {e}")
    print("The program will continue without sound alerts")

def eye_aspect_ratio(eye):
  
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
   
    ear = (A + B) / (2.0 * C)
    return ear

EYE_AR_THRESH = 0.26  
EYE_AR_CONSEC_FRAMES = 30  
COUNTER = 0               # Counter for consecutive frames with closed eyes
ALARM_ON = False          # Flag to track if alarm is currently playing

# Initialize dlib's face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

# Get the indices for left and right eyes
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Drowsiness detection started. Press 'q' to quit.")

# Main loop
while True:
    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame from webcam.")
        break
    
    # Resize frame for faster processing
    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the grayscale frame
    faces = detector(gray, 0)
    
    # Process each face found
    for face in faces:
        # Get face coordinates
        x1, y1 = face.left(), face.top()
        x2, y2 = face.right(), face.bottom()
        
        # Determine the facial landmarks
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)
        
        # Extract the left and right eye coordinates
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        
        # Calculate the EAR for both eyes
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        
        # Average the EAR for both eyes
        ear = (leftEAR + rightEAR) / 2.0
        
        # Draw contours around eyes
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        
        # Check if the EAR is below the threshold
        if ear < EYE_AR_THRESH:
            COUNTER += 1
            # If eyes are closed for a sufficient number of frames, trigger alarm
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                # Draw red rectangle around face
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                # Display warning text
                cv2.putText(frame, "PHAT HIEN BUON NGU!", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # Play alarm if not already playing
                if not ALARM_ON:
                    ALARM_ON = True
                    try:
                        pygame.mixer.music.play(-1)  # Loop alarm sound
                    except:
                        print("Could not play alarm sound")
        else:
            # Draw green rectangle around face when not drowsy
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Reset counter if eyes are open
            COUNTER = 0
            # Stop alarm if it's playing
            if ALARM_ON:
                ALARM_ON = False
                try:
                    pygame.mixer.music.stop()
                except:
                    pass
        
        # Display EAR value
        cv2.putText(frame, f"EAR: {ear:.2f}", (300, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Display the frame
    cv2.imshow("Drowsiness Detection", frame)
    
    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit() 