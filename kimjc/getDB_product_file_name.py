#-*- coding: utf-8 -*-
import urllib.request
import pymysql as mysql
import re

# MySQL DB 연결을 한다
db = mysql.connect(host='ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com', user='root', password='root', db='forstyle', charset='utf8')
output_file = open("test.txt", 'w')

with db.cursor() as curs:
    sql = "SELECT product_file_name FROM product"
    curs.execute(sql)

    # 데이타 Fetch
    rows = curs.fetchall()
    rows = re.sub("[ ()]", "", str(rows))
    #print(rows)
    rows = str(rows).split(',,')


    for item in rows:
    	item = re.sub(",", "", str(item))
    	item = "image_"+item
    	output_file.write('{}\n'.format(item))
    
    # 파일을 닫는다
    output_file.close()