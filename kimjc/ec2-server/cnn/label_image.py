#-*- coding: utf-8 -*-
import tensorflow as tf
import pymysql as mysql
import sys
import re
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def connect_db(class_, result):
    # db를 연결합니다.
    db = mysql.connect(host='localhost', user='root', password='root', db='forstyle', charset='utf8')

    # Cursor
    curs = db.cursor()

    # sql query
    sql = "SELECT product_file_name, product_brand FROM product WHERE product_clothes_label='" + str(class_)+"' order by rand() limit 20"
    curs.execute(sql)
    rows = curs.fetchall()

    for data in rows:
        data = str(data) # 문자열로 형변환
        data = re.sub("[ '()]", "", data) # 정규식 제거
        #print(data)
        result = result+str(data)+"/"
    return result
    db.close()

if __name__ == '__main__':
    # change this as you see fit
    image_path = sys.argv[1]
    # Read in the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("/var/www/html/code/cnn/retrained_labels.txt")]
    # Unpersists graph from file
    with tf.gfile.FastGFile("/var/www/html/code/cnn/retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')
    with tf.Session() as sess:
        #print "tf.Session()"
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
             {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        label = label_lines[top_k[0]]
        label = re.sub(" ","_",label_lines[top_k[0]])
        os.system("python3 /var/www/html/code/cnn/color.py "+str(sys.argv[1])+" "+str(label))
        #result = ""
        #result = connect_db(label, result)
        #result = label+":"+result
        #print result
