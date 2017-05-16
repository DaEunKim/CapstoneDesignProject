import tensorflow as tf
import sys
import re
import pymysql as mysql
import urllib.request
import os.path
import numpy as np
from PIL import Image
from tensorflow.python.framework import graph_util
from tensorflow.python.framework import tensor_shape
from tensorflow.python.platform import gfile
from tensorflow.python.util import compat




# change this as you see fit
#image_path = sys.argv[1]

label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("retrained_labels.txt")]
with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')



            
image_dir =sys.argv[1]

true = 0.0
false = 0.0
test_num = np.zeros(31)

confusion_matrix= np.zeros((31,31))
f = open('accuracy.txt', 'w')

if not gfile.Exists(image_dir):
    print("Image directory '" + image_dir + "' not found.")

sub_dirs = [x[0] for x in gfile.Walk(image_dir)]
is_root_dir = True
for sub_dir in sub_dirs:
    label_true=0.0
    label_false=0.0
    count = 0
    if is_root_dir:
      is_root_dir = False
      continue
    extensions = ['jpg', 'jpeg', 'JPG', 'JPEG']
    file_list = []
    dir_name = os.path.basename(sub_dir)
    if dir_name == image_dir:
      continue
    print("Looking for images in '" + dir_name + "'")
    for extension in extensions:
      file_glob = os.path.join(image_dir, dir_name, '*.' + extension)
      file_list.extend(gfile.Glob(file_glob))
    if not file_list:
      print('No files found')
      continue
    
    for image_path in file_list:
        image_data = tf.gfile.FastGFile(image_path, 'rb').read()
    
    
        with tf.Session() as sess:
            # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            
            predictions = sess.run(softmax_tensor, \
                     {'DecodeJpeg/contents:0': image_data})
            
            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            label = label_lines[top_k[0]]

            #confusion matrix
            dir_num = label_lines.index(re.sub("_"," ",dir_name))
            label_num = label_lines.index(label)
            confusion_matrix[dir_num][label_num] = confusion_matrix[dir_num][label_num] + 1
            
            label = re.sub(" ","_",label_lines[top_k[0]])
            if label ==dir_name:
                label_true = label_true + 1
            else :
                label_false = label_false + 1
            test_num[dir_num] = label_true + label_false
            count = count + 1
            print(count," :" +label + "(",label_num,")","=" + dir_name+ "(",dir_num,")")
            
    accuracy = label_true / (label_false+label_true) * 100
    print("test accuracy :" + str(accuracy) + "%")
    true = true + label_true
    false = false + label_false
for i in range(0,31):
    f.write("\n%22s" % label_lines[i])
    for j in range(0,31):
        f.write("%4d" % (confusion_matrix[i][j] / test_num[i] * 100))
accuracy = true / (false+true) * 100
print("test accuracy :" + str(accuracy) + "%")

        


# Read in the image_data
#image_data = tf.gfile.FastGFile(image_path, 'rb').read()

# Loads label file, strips off carriage return
"""
label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("retrained_labels.txt")]
"""
"""
# Unpersists graph from file
with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

with tf.Session() as sess:
    # Feed the image_data as input to the graph and get first prediction
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    
    predictions = sess.run(softmax_tensor, \
             {'DecodeJpeg/contents:0': image_data})
    
    # Sort to show labels of first prediction in order of confidence
    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
    label = label_lines[top_k[0]]
    label = re.sub(" ","_",label_lines[top_k[0]])
    print(label)
"""
