from statistics import mode
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import cv2
from keras.models import load_model
import numpy as np

from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.preprocessor import preprocess_input

import random
import time
class EmotionGame():
    def __init__(self) -> None:
        self.detection_model_path = './trained_models/haarcascade_frontalface_default.xml'
        self.emotion_model_path = './trained_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
        self.emotion_labels = get_labels('fer2013')

        self.face_detection = load_detection_model(self.detection_model_path)
        self.emotion_classifier = load_model(self.emotion_model_path, compile=False)
        self.emotion_target_size = self.emotion_classifier.input_shape[1:3]

        self.frame_window = 10
        self.emotion_offsets = (20, 40)
        self.emotion_window = []
        #pull high score from API
        self.highscore = 0
        self.score = 0
        self.level = 1
        self.time_limit = 3
        #self.total_time = 90
        self.num_guesses = 3
        self.pictures = []

        self.emotion_score = {
            'neutral': 10,
            'happy': 15,
            'surprise': 20,
            'angry': 25,
            'sad': 30,
            'fear': 35,
            'disgust': 40
        }

    def gen_random_emotion(self):
        emotions = ['happy', 'sad', 'neutral', 'angry', 'surprise', 'fear', 'disgust']
        return random.choice(emotions)

    def emotion_detection(self, faces, gray_image, rgb_image):
        for face_coordinates in faces:
            x1, x2, y1, y2 = apply_offsets(face_coordinates, self.emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]
            try:
                gray_face = cv2.resize(gray_face, (self.emotion_target_size))
            except:
                continue

            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            emotion_prediction = self.emotion_classifier.predict(gray_face, verbose=False)
            emotion_probability = np.max(emotion_prediction)
            emotion_label_arg = np.argmax(emotion_prediction)
            emotion_text = self.emotion_labels[emotion_label_arg]
            self.emotion_window.append(emotion_text)

            if len(self.emotion_window) > self.frame_window:
                self.emotion_window.pop(0)
            try:
                emotion_mode = mode(self.emotion_window)
            except:
                continue

            if emotion_text == 'angry':
                color = emotion_probability * np.asarray((255, 0, 0))
            elif emotion_text == 'sad':
                color = emotion_probability * np.asarray((0, 0, 255))
            elif emotion_text == 'happy':
                color = emotion_probability * np.asarray((255, 255, 0))
            elif emotion_text == 'surprise':
                color = emotion_probability * np.asarray((0, 255, 255))
            else:
                color = emotion_probability * np.asarray((0, 255, 0))

            color = color.astype(int)
            color = color.tolist()

            draw_bounding_box(face_coordinates, rgb_image, color)
            draw_text(face_coordinates, rgb_image, emotion_mode,
                    color, 0, -45, 1, 1)
            return emotion_text
    def run_game(self):
        cv2.namedWindow('window_frame')
        video_capture = cv2.VideoCapture(0)
        start_time = time.time()
        end_emotion = ''
        expected_emotion = self.gen_random_emotion()
        curr_guesses = 0
        while True:
            ret, frame = video_capture.read()
            bgr_image = video_capture.read()[1]
            gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
            rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
            faces = detect_faces(self.face_detection, gray_image)
            cv2.putText(rgb_image, "Score: " + str(self.score), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            if(curr_guesses != 0):
                cv2.putText(rgb_image, "Guesses: " + str(self.num_guesses-curr_guesses + 1), (int(frame.shape[1]-150),20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            if curr_guesses == 0:
                intro = rgb_image.copy()
                cv2.putText(intro, "Welcome to FACIAL FRENZY", (int(frame.shape[1] / 3), int(frame.shape[0] / 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow('window_frame', cv2.cvtColor(intro, cv2.COLOR_RGB2BGR))
                cv2.waitKey(2000)

                rules = rgb_image.copy()
                cv2.putText(rules, "You have 5 seconds to imitate the emotion :D", (int(frame.shape[1] / 3), int(frame.shape[0] / 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow('window_frame', cv2.cvtColor(rules, cv2.COLOR_RGB2BGR))
                cv2.waitKey(2000)

                pts = rgb_image.copy()
                cv2.putText(pts, "Making the correct face increases your score!", (int(frame.shape[1] / 3), int(frame.shape[0] / 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow('window_frame', cv2.cvtColor(pts, cv2.COLOR_RGB2BGR))
                cv2.waitKey(2000)

                highscore = rgb_image.copy()
                cv2.putText(highscore, "And keep track of your high score online!", (int(frame.shape[1] / 3), int(frame.shape[0] / 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow('window_frame', cv2.cvtColor(highscore, cv2.COLOR_RGB2BGR))
                cv2.waitKey(2000)

                start = rgb_image.copy()
                cv2.putText(start, "Now starting the game, your emotion is " + expected_emotion, (int(frame.shape[1] / 3), int(frame.shape[0] / 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow('window_frame', cv2.cvtColor(start, cv2.COLOR_RGB2BGR))
                cv2.waitKey(1800)

                rd = rgb_image.copy()
                cv2.putText(rd, "Ready?", (int(frame.shape[1] / 3), int(frame.shape[0] / 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow('window_frame', cv2.cvtColor(rd, cv2.COLOR_RGB2BGR))
                cv2.waitKey(1000)

                g = rgb_image.copy()
                cv2.putText(g, "Go!", (int(frame.shape[1] / 3), int(frame.shape[0] / 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow('window_frame', cv2.cvtColor(g, cv2.COLOR_RGB2BGR))
                cv2.waitKey(700)
                curr_guesses += 1
                start_time = time.time()
                continue
            if time.time() - start_time < self.time_limit:
                end_emotion = self.emotion_detection(faces, gray_image, rgb_image)
            else:
                self.pictures.append(rgb_image)
                curr_guesses += 1
                announce = rgb_image.copy()
                text_position = (int(frame.shape[1] / 4), int(frame.shape[0] / 6))
                if expected_emotion == end_emotion:
                    self.score += self.emotion_score[end_emotion]
                    cv2.putText(announce, "You Got It Right!", text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                else:
                    cv2.putText(announce, "You Got It Wrong :(", text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                cv2.imshow('window_frame', cv2.cvtColor(announce, cv2.COLOR_RGB2BGR))
                cv2.waitKey(1000)
                expcted = rgb_image.copy()
                while True:
                    temp = self.gen_random_emotion()
                    if temp != expected_emotion:
                        expected_emotion = temp
                        break
                if curr_guesses > self.num_guesses:
                    break
                cv2.putText(expcted, "Your Next Emotion is " + expected_emotion, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow('window_frame', cv2.cvtColor(expcted, cv2.COLOR_RGB2BGR))
                cv2.waitKey(2000)
                ready = rgb_image.copy()
                cv2.putText(ready, "Ready?", text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow('window_frame', cv2.cvtColor(ready, cv2.COLOR_RGB2BGR))
                cv2.waitKey(1000)
                start_time = time.time()
            bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
            cv2.imshow('window_frame', bgr_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        ret, frame = video_capture.read()
        conclude = frame.copy()
        cv2.putText(conclude, "Thank you for playing!", (int(frame.shape[1] / 3), int(frame.shape[0] / 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow('window_frame', conclude)
        cv2.waitKey(2000)
        video_capture.release()
        cv2.destroyAllWindows()
if __name__ == "__main__":
    game = EmotionGame()
    game.run_game()
