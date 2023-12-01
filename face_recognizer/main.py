import face_recognition
import os, sys
import cv2
import numpy as np
import math

def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    def __init__(self):
        self.encode_faces()

    def encode_faces(self):
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f'faces/{image}')
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)

        print(self.known_face_names)

    def update_known_faces(self, user_name, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_encoding = face_recognition.face_encodings(rgb_frame)[0]
        self.known_face_encodings.append(face_encoding)
        self.known_face_names.append(f'{user_name}')

    def text_input_box(self, frame, prompt):
        text = ""
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 13: 
                break
            elif key == 8 or key == 127:
                text = text[:-1]
            elif key >= 32 and key <= 126: 
                text += chr(key)

            input_frame = frame.copy()
            cv2.rectangle(input_frame, (50, 50), (450, 100), (200, 200, 200), -1)
            cv2.putText(input_frame, prompt + text, (60, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            cv2.imshow('Face Recognition', input_frame)
        return text


    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            sys.exit('Video source not found...')

        unknown_face_detected = False


        while True:
            ret, frame = video_capture.read()
            key = cv2.waitKey(1) 

            if self.process_current_frame:
                small_frame = cv2.resize(frame, (0, 0), fx = 0.25, fy = 0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                # find all faces in the current frame
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                unknown_face_detected = False 

                for face_encoding in self.face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = 'Unknown'
                    confidence = 'Unknown'

                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index].split('_')[0]
                        confidence = face_confidence(face_distances[best_match_index])

                    if confidence != 'Unknown':
                        confidenceNum = float(confidence.split('%')[0])

                    if confidenceNum < 96 or confidence == 'Unknown':
                        name = 'Unknown'
                        confidence = 'Unknown'

                    self.face_names.append(f'{name} ({confidence})')

                for name in self.face_names:
                        if name.split(' ')[0] == 'Unknown':
                            unknown_face_detected = True
            
            self.process_current_frame = not self.process_current_frame

            # display annotations
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), -1)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            if unknown_face_detected:
                cv2.putText(frame, "Press 'c' to capture your face", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow('Face Recognition', frame)

            if key == ord('q'):
                break

            if key == ord('c'):
                ret, frame_to_save = video_capture.read()
                if ret:
                    user_name = self.text_input_box(frame_to_save, "Enter your name: ")
                    if user_name:
                        cv2.imwrite(f'faces/{user_name}.png', frame_to_save)
                        self.update_known_faces(user_name, frame_to_save)

        
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()
