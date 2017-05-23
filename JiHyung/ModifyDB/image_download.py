#-*- coding: utf-8 -*-
import urllib.request
import pymysql as mysql
import re

def imageDownlad(imageUrl, count):
    image = urllib.request.urlopen(imageUrl)
    if imageUrl[-3:-1] == 'gif':
        fileName = 'casual_skirt_short/image_' + str(count) + '.gif'
    else:
        fileName = 'casual_skirt_short/image_' + str(count) + '.jpg'

    imageFile = open(fileName, 'wb')
    imageFile.write(image.read())
    imageFile.close()

# MySQL DB로 쿼리 보내기
db = mysql.connect(host='ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com', user='root', password='root', db='forstyle', charset='utf8')

with db.cursor() as curs:
    sql = "SELECT product_file_name,product_shopping_img_url FROM product WHERE product_clothes_label = 'casual_skirt_short'"
    curs.execute(sql)

    rows = curs.fetchall()

    for row in rows:
        index = row[0]
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
        imageDownlad(href, index)
db.close()