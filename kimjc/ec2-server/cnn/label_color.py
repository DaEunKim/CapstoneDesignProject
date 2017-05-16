#-*- coding: utf-8 -*-
import numpy as np
import cv2
import tensorflow as tf
import sys
import os.path
from tensorflow.python.platform import gfile
import matplotlib.pyplot as plt
import pymysql as mysql
import urllib.request
import re
from PIL import Image
import os

def vectorize(hist):
    vector = np.zeros((16,), dtype = np.int)

    for i in range(16):
        sum = 0
        for j in range(16):
            sum += hist[i*16 + j]
        vector[i] = sum

    return vector

def calculate_rgb(image_name):

    image = cv2.imread(image_name)

    h = np.shape(image)[0]
    w = np.shape(image)[1]
    image = image[  h//6 :(h//6)*5, w//6 : (w//6)*5 ]

    image = cv2.resize(image, (100,100), interpolation= cv2.INTER_AREA)

    img_r, img_g, img_b = cv2.split(image)

    hist_r,bins = np.histogram(img_r.ravel(),256,[0,256])
    hist_g,bins = np.histogram(img_g.ravel(),256,[0,256])
    hist_b,bins = np.histogram(img_b.ravel(),256,[0,256])

    r = vectorize(hist_r)
    g = vectorize(hist_g)
    b = vectorize(hist_b)

    rgb_vector = np.append(np.append(r,g),b)
    return rgb_vector
def search_db_rgb(rgb, category):

    #db = mysql.connect(host='localhost', user='root', password='root', db='forstyle', charset='utf8')
    db = mysql.connect(host='ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com', user='root', password='root', db='forstyle', charset='utf8')

    curs = db.cursor()


    sql = "SELECT product_file_name, product_brand, c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27,c28,c29,c30" + \
    ",c31,c32,c33,c34,c35,c36,c37,c38,c39,c40,c41,c42,c43,c44,c45,c46,c47,c48 FROM product WHERE c1 IS NOT NULL AND product_clothes_label = '" + category + "'"
    curs.execute(sql)

    rows = curs.fetchall()

    result_list = []
    c = []
    for row in rows:
        c = row[2:]

        sum = 0
        for _ in range(0,48):
            sum += abs(rgb[_] - c[_])

        result_list.append((sum,row[0],row[1]))

    result_list = sorted(result_list, key = lambda x: x[0])[0:10]


    #print(result_list)

    result = []
    category= category+":"
    for i in result_list:
        result.append(i[1])
        category = category+str(i[1])+","+str(i[2])+"/"
    db.close()
    return category

if __name__ == '__main__':

    if (sys.argv[1] == 'write_rgb'):
        write_rgb_db()
        exit()

    if (sys.argv[1].split('.')[-1] == 'jpg'):
        rgb = calculate_rgb(sys.argv[1])
        #print(rgb)
        result = search_db_rgb(rgb, sys.argv[2])
        print(result)

