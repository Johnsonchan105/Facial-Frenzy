from keras.models import load_model
import cv2
import numpy as np
from keras.utils import get_file

# Load the pre-trained emotion detection model
emotion_model_url = "https://github.com/priya-dwivedi/face_and_emotion_detection/raw/master/emotion_detector_models/model_v6_23.hdf5"
emotion_model_path = get_file("emotion_detector_model", emotion_model_url, cache_subdir="models")
emotion_model = load_model(emotion_model_path)

# Load the face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Define emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Open the webcam
video_capture = cv2.VideoCapture(0)

# Create a window to display the webcam feed
cv2.namedWindow('window_frame')

# Main loop for real-time emotion detection
while True:
    # Read a frame from the webcam
    ret, frame = video_capture.read()

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Process each detected face
    for (x, y, w, h) in faces:
        # Extract the region of interest (ROI) corresponding to the face
        face_roi = gray_frame[y:y+h, x:x+w]

        # Resize the face ROI to the input size expected by the model
        face_roi = cv2.resize(face_roi, (48, 48))

        # Normalize the pixel values to the range [0, 1]
        face_roi = face_roi / 255.0

        # Expand dimensions to match the model's input shape
        face_roi = np.expand_dims(face_roi, axis=0)
        face_roi = np.expand_dims(face_roi, axis=-1)

        # Make a prediction using the emotion detection model
        emotion_prediction = emotion_model.predict(face_roi)

        # Get the index of the predicted emotion
        emotion_index = np.argmax(emotion_prediction)

        # Get the corresponding emotion label
        emotion_label = emotion_labels[emotion_index]

        # Display the emotion label on the frame
        cv2.putText(frame, emotion_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Draw a rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the frame with emotion labels
    cv2.imshow('window_frame', frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
video_capture.release()
cv2.destroyAllWindows()
