# Generic Imports
import tensorflow as tf
import numpy as np
import cv2

#from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
import keras.applications.imagenet_utils as imagenet_utils

model = ResNet50(weights="imagenet")

def rotate_90(img):
    return np.transpose(img, axes=(1, 0, 2))[:, ::-1]

def process_image(img):
    height = img.shape[0]
    width = img.shape[1]

    # ensure image is portrait
    assert height >= width

    # make a square based on the width
    input_square = cv2.resize(img[0:width, 0:width].copy(), (224, 224))
    cv2.imshow("deubg", input_square)

    input_square = input_square[:, :, ::-1]
    input_square = preprocess_input(input_square)
    input_square = input_square.reshape((1, 224, 224, 3))

    out = model.predict(input_square)
    predictions = imagenet_utils.decode_predictions(out)

    pred_strings = [pred[1] + " " + str(round(100 * pred[2], 1)) + "%" for pred in predictions[0]]

    img = img.copy()
    img = cv2.resize(img, (800, int(800 * height / width)))

    cv2.circle(img, (400, 400), 8, (0, 0, 0), 3)

    cv2.rectangle(img, (0, 800), (800, int(800 * height / width)), (255, 255, 255), -1)

    for i in range(len(pred_strings)):
        string = pred_strings[i]
        cv2.putText(img, string, (10, 850 + i * 55), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 0), 2)

    return img

cap = cv2.VideoCapture(1)
#cv2.namedWindow("image", cv2.WINDOW_NORMAL)

while True:
    img = cap.read()[1]
    out = process_image(rotate_90(img))
    cv2.imshow("image", out[::2, ::2])

    cv2.waitKey(10)
