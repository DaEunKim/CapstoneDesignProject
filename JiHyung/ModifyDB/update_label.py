import pymysql as mysql
import sys
import re
import os.path
from tensorflow.python.platform import gfile

db = mysql.connect(host='ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com', user='root', password='root',
                   db='forstyle', charset='utf8')

curs = db.cursor()
sql = """update product set product_clothes_label = ""%s"" where product_file_name = %s"""

image_dir = sys.argv[1]

if not gfile.Exists(image_dir):
    print("Image directory '" + image_dir + "' not found.")

sub_dirs = [x[0] for x in gfile.Walk(image_dir)]

for sub_dir in sub_dirs:
    dir_name = os.path.basename(sub_dir)
    if dir_name == image_dir:
        continue
    extensions = ['jpg', 'jpeg', 'JPG', 'JPEG']
    file_list = []

    for extension in extensions:
        file_glob = os.path.join(image_dir, dir_name, '*.' + extension)
        file_list.extend(gfile.Glob(file_glob))

    for image_path in file_list:
        tmp = re.split('image_', image_path)
        image_name = re.split('\.', tmp[1])
        print(dir_name, ":", image_name[0])
        curs.execute(sql, (dir_name, image_name[0]))
db.commit()
db.close()