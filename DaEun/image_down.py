#-*- coding: utf-8 -*-
import urllib.request
import pymysql as mysql
import re
from PIL import Image

def imageDownlad(imageUrl, count):
    image = urllib.request.urlopen(imageUrl)
    if imageUrl[-3:-1] == 'gif':
        fileName = 'Images/001/image_' + str(count) + '.gif'
    else:
        fileName = 'Images/001/image_' + str(count) + '.jpg'

    imageFile = open(fileName, 'wb')
    imageFile.write(image.read())
    imageFile.close()

    file_path = "/Users/Dani/Documents/CapstoneDesignProject/DaEun/Images/001/image_"+str(count)+".jpg"
    im = Image.open(file_path)
    mypalette = im.getpalette()
    #print(mypalette)
    #im.putpalette(mypalette)
    new_im = Image.new("RGBA", im.size)
    new_im.paste(im)
    #new_im.save("/var/www/html/image/image_"+str(i)+".jpg")
    new_im.save("/Users/Dani/Documents/CapstoneDesignProject/DaEun/Images/001/image_"+str(count)+".jpg")



# MySQL DB ¿¬°áÀ» ÇÑŽÙ
db = mysql.connect(host='ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com', user='root', password='root', db='forstyle', charset='utf8')

with db.cursor() as curs:
    #sql = "SELECT product_shopping_img_url FROM product WHERE product_file_name > 9000 AND product_file_name < 12001"
    sql = "SELECT product_file_name,product_shopping_img_url FROM product WHERE product_file_name >= 17207 and product_file_name <=17784 "

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