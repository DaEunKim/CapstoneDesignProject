import numpy as np
import cv2
import tensorflow as tf
import sys
import os.path
from tensorflow.python.platform import gfile
import matplotlib.pyplot as plt
import pymysql as mysql

#-*- coding: utf-8 -*-

def calculate_h(image_name):

image = cv2.imread(image_name)

img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

img_h, img_l, img_s = cv2.split(img_hsv)

h = np.shape(img_h)[0]
w = np.shape(img_h)[1]
# 1/4 crop
#tmp_img_h = img_h[  h//4 :(h//4)*3, w//4 : (w//4)*3 ]

# 1/9 crop
tmp_img_h = img_h[  h//3 :(h//3)*2, w//3 : (w//3)*2 ]

#print(np.shape(tmp_img_h))

#mean_h = np.mean(img_h)

hist = cv2.calcHist(tmp_img_h,[0],None,[180],[0,180])

hist_l = cv2.calcHist(img_l, [0], None, [255], [0,255])

#print(hist.T)
#print(np.argmax(hist))

"""
plt.plot(hist)
plt.title("Histogram of Hue")
plt.show()
"""

"""
plt.plot(hist_l)
plt.title("Histogram of Luminaunce")
plt.show()
"""

#print(np.argmax(hist) * 2)
#cv2.imshow("Origin_Image", image)
#cv2.imshow("crob_Image", tmp_img_h)
#cv2.waitKey(0)

return np.argmax(hist) * 2

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

def connect_db(class_):

    # MySQL DB 연결을 한다
    db = mysql.connect(host='localhost', user='root', password='root', db='product', charset='utf8')

    # Connection 으로부터 Cursor 생성
    curs = db.cursor()

    # SQL문 실행
    sql = "SELECT [img_col] FROM [table_name] where [color_class='class_']"
    curs.execute(sql)

    # 데이타 Fetch
    rows = curs.fetchall()
    print(rows)
    db.close()

def write_hsv_db():
    # MySQL DB 연결을 한다
    db = mysql.connect(host='localhost', user='root', password='root', db='forstyle', charset='utf8')

    # Connection 으로부터 Cursor 생성
    curs = db.cursor()

    # SQL문 실행
    sql = "SELECT product_file_name FROM demo"
    curs.execute(sql)

    # 데이타 Fetch
    rows = curs.fetchall()
    # print(rows)

    for img in rows:

        # 사진 보고 hsv값 추출하기    img[0] = product_file_name
        image_name = "/var/www/html/topten/image_" + str(img[0]) + ".jpg"
               hsv = calculate_h(image_name)

        # UPDATA문
        sql = "UPDATE demo SET product_color_label = '" + str(hsv) + "'" + " WHERE product_file_name = '" + str(img[0]) + "'"
        curs.execute(sql)

    db.commit()
    db.close()

def search_db(class_, result):

    db = mysql.connect(host='localhost', user='root', password='root', db='forstyle', charset='utf8')

    curs = db.cursor()

    sql = "SELECT product_file_name FROM demo WHERE product_color_label=" + str(class_)
    curs.execute(sql)

    rows = curs.fetchall()

    for data in rows:
        result.append(data[0])

    db.commit()
    db.close()



if __name__ == '__main__':

    tmp = sys.argv[1].split('.')

    if(tmp[-1] == 'jpg'):
        class_ = calculate_h(sys.argv[1])

        if(class_ == 0):
            class_ = 777

        #print(class_)

        result = []

        search_db(class_, result)

        sim = 1

        while True:
            if(len(result) >= 20):
                break

            search_db(class_-sim, result)
            search_db(class_+sim, result)
            sim += 1
        print(result)
    else:
        array = search_folder(sys.argv[1])
        print (array)