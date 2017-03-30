import numpy as np
import cv2
import tensorflow as tf
import sys
import os.path
from tensorflow.python.platform import gfile

def calculate_h(image_name):

    image = cv2.imread(image_name)

    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  

    img_h, img_s, img_v = cv2.split(img_hsv)

    mean_h = np.mean(img_h)

    #cv2.imshow("Image", image)
    #cv2.waitKey(0)
    #print(mean_h)

    return mean_h

    # define range of blue color in HSV
    #lower_blue = np.array([110,50,50])
    #upper_blue = np.array([130,255,255])

    # Threshold the HSV image to get only blue colors
    #mask = cv2.inRange(img_hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image  
    #img_result = cv2.bitwise_and(image,image, mask= mask)  

    #cv2.imshow( 'mask', mask )  
    #cv2.imshow( 'img_result', img_result ) 

    #cv2.imshow("Image", image)
    #cv2.waitKey(0)

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

    array = search_folder(sys.argv[1])

    print(array)

    boundary = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


    for mean_h in array :
        boundary[int(mean_h) // 10] += 1

    print (boundary)
    