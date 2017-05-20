#-*- coding: utf-8 -*-
import urllib.request
import pymysql as mysql
import re

def imageDownlad(imageUrl, count):
    image = urllib.request.urlopen(imageUrl)
    if imageUrl[-3:-1] == 'gif':
        fileName = 'label/image_' + str(count) + '.gif'
    else:
        fileName = 'label/image_' + str(count) + '.jpg'

    imageFile = open(fileName, 'wb')
    imageFile.write(image.read())
    imageFile.close()

# MySQL DB ¿¬°áÀ» ÇÑŽÙ
db = mysql.connect(host='ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com', user='root', password='root', db='forstyle', charset='utf8')

with db.cursor() as curs:
    sql = "SELECT product_shopping_img_url FROM product WHERE product_file_name > 18130 AND product_file_name < 21401"
    curs.execute(sql)

    # µ¥ÀÌÅž Fetch
    rows = curs.fetchall()
    index = 18131
    for row in rows:
        row = str(row)
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
        index += 1

db.close()

