import cv2
from keras.models import load_model
from PIL import Image
import sys
import numpy as np
import keras.losses
import tensorflow as tf


def huber_loss(y_true, y_pred, clip_delta=1.0):
    error = y_true - y_pred
    cond = tf.keras.backend.abs(error) < clip_delta

    squared_loss = 0.5 * tf.keras.backend.square(error)
    linear_loss = clip_delta * (tf.keras.backend.abs(error) - 0.5 * clip_delta)

    return tf.where(cond, squared_loss, linear_loss)


'''
 ' Same as above but returns the mean loss.
'''


def huber_loss_mean(y_true, y_pred, clip_delta=500.0):
    return tf.keras.backend.mean(huber_loss(y_true, y_pred, clip_delta))

def my_loss(y_true, y_pred):
  error = y_true - y_pred
  cond  = y_true == nonVector
  cond2 = y_pred < nonVector/2

  squared_loss = 0.5 * tf.keras.backend.square(error)
  tmp = tf.where(cond, 0.0, squared_loss)

  return tf.where(cond2, tmp, squared_loss)

'''
 ' Same as above but returns the mean loss.
'''
def my_loss_mean(y_true, y_pred):
  return tf.keras.backend.mean(my_loss(y_true, y_pred))


keras.losses.huber_loss_mean = huber_loss_mean
keras.losses.huber_loss_mean = my_loss

leftPath = sys.argv[1]
rightPath = sys.argv[2]
model = load_model('best_model.hdf5')
nonVector = -1000

image = Image.open(leftPath)
new_image = image.resize((1280, 720))
new_image.save('tmpLeft.jpg')

image = Image.open(rightPath)
new_image = image.resize((1280, 720))
new_image.save('tmpRight.jpg')

left = []
right = []

left.append(cv2.cvtColor(cv2.imread("tmpLeft.jpg"), cv2.COLOR_BGR2GRAY))
right.append(cv2.cvtColor(cv2.imread("tmpRight.jpg"), cv2.COLOR_BGR2GRAY))

left = np.stack(left)
right = np.stack(right)

[pred_target_cam, pred_target_windows] = model.predict([left, right])

number_of_windows = 0

for photo in range(len(pred_target_windows)):
    for window in range(len(pred_target_windows[photo])):
        # for i in range(len(pred_target_windows[photo][window])):
        #     if pred_target_windows[photo][window][1] < nonVector / 10:
            if pred_target_windows[photo][window][1] < -1:
                pred_target_windows[photo][window][1] = nonVector
            else:
                number_of_windows += 1

number_of_windows = number_of_windows / 4
print(pred_target_cam[0])
print(pred_target_windows[0])
print("Number of windows: ", number_of_windows)
