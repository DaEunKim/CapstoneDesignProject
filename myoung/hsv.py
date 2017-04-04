import numpy as np
import cv2
import tensorflow as tf
import sys
import os.path
from tensorflow.python.platform import gfile
import matplotlib.pyplot as plt

def calculate_h(image_name):

    image = cv2.imread(image_name)

    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  

    img_h, img_s, img_v = cv2.split(img_hsv)

    mean_h = np.mean(img_h)

    hist = cv2.calcHist(img_h*2,[0],None,[360],[0,360])
    #print(hist.T)
    print(np.argmax(hist))

    cv2.imshow("Image", image)
    cv2.waitKey(0)

    return mean_h * 2

def search_folder(image_dir):

    if not gfile.Exists(image_dir):
        print("Image directory '" + image_dir + "' not found.")
        return None

    result = {}
    extensions = ['jpg', 'jpeg', 'JPG', 'JPEG']
    file_list = []
    print("Looking for images in '" + image_dir + "'")

    for extension in extensions:
        file_glob = os.path.join(image_dir, '*.' + extension)
        file_list.extend(gfile.Glob(file_glob))

    if not file_list:
        print('No files found')
        return 0
  
    array = []

    for file_name in file_list:
        array.append(calculate_h(file_name))

    return array
 

if __name__ == '__main__':

    tmp = sys.argv[1].split('.')

    if(tmp[-1] == 'jpg'):
        calculate_h(sys.argv[1])
    else:
        array = search_folder(sys.argv[1])
    