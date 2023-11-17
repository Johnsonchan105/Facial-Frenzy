from keras import Sequential
from keras.models import load_model
import cv2
import numpy as np
from keras.preprocessing.image import img_to_array

class_labels = {0: 'Angry', 1: 'Fear', 2: 'Happy', 3: 'Neutral', 4: 'Sad', 5: 'Surprise'}
classes = list(class_labels.values())

print(class_labels)