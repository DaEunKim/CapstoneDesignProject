# -*- coding: utf-8 -*-
import urllib.request
import pymysql as mysql
import re
from PIL import Image
import os
import cv2


def image_crob(image_name, x1, y1, x2, y2):
    image = cv2.imread(image_name)

    image = image[y1:y2, x1: x2]

    cv2.imwrite(image_name, image)


def imageDownlad(imageUrl, count, label_name, x1, y1, x2, y2):
    dir_name = "/home/capstone/Desktop/forstyle/" + label_name
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    image = urllib.request.urlopen(imageUrl)
    if imageUrl[-3:-1] == 'gif':
        fileName = '/home/capstone/Desktop/forstyle/' + label_name + '/image_' + str(count) + '.gif'
    else:
        fileName = '/home/capstone/Desktop/forstyle/' + label_name + '/image_' + str(count) + '.jpg'

    imageFile = open(fileName, 'wb')
    imageFile.write(image.read())
    imageFile.close()

    file_path = "/home/capstone/Desktop/forstyle/" + label_name + "/image_" + str(count) + ".jpg"
    try:
        im = Image.open(file_path)
    except IOError:
        return
    mypalette = im.getpalette()
    # print(mypalette)
    # im.putpalette(mypalette)
    new_im = Image.new("RGBA", im.size)
    new_im.paste(im)
    # new_im.save("/var/www/html/image/image_"+str(i)+".jpg")
    new_im.save("/home/capstone/Desktop/forstyle/" + label_name + "/image_" + str(count) + ".jpg")

    image_crob("/home/capstone/Desktop/forstyle/" + label_name + "/image_" + str(count) + ".jpg", x1, y1, x2, y2)


# MySQL DB ¿¬°áÀ» ÇÑŽÙ
db = mysql.connect(host='ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com', user='root', password='root',
                   db='forstyle', charset='utf8')

with db.cursor() as curs:
    # sql = "SELECT product_shopping_img_url FROM product WHERE product_file_name > 9000 AND product_file_name < 12001"
    sql = "SELECT product_file_name,product_shopping_img_url,product_clothes_label,x1,y1,x2,y2 FROM product WHERE x1 IS NOT NULL AND product_file_name >0  AND product_file_name<23000"
    curs.execute(sql)

    rows = curs.fetchall()

    for row in rows:
        img = row
        index = row[0]
        label_name = row[2]
        row = str(row[1])
        row = re.sub('[,\'\"\(\)]', "", row)
        if (row[0:4] == 'http'):
            href = str(row)
        # http ·Î œÃÀÛÇÏÁö ŸÊÀ» °æ¿ì µµžÞÀÎ ÁÖŒÒžŠ ŸÕ¿¡ ºÙ¿© ¿¬°áÇÑŽÙ

        elif row == '':
            continue
        else:
            href = 'http://' + str(row)
        print(href)

        x1 = img[3]
        y1 = img[4]
        x2 = img[5]
        y2 = img[6]

        try:
            imageDownlad(href, index, label_name, x1, y1, x2, y2)
        except:
            continue


db.close()

