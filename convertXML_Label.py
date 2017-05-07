# -*- coding: utf-8 -*-
import pymysql as mysql
from xml.etree.ElementTree import ElementTree, Element, SubElement, dump
import sys
import os
import re

# MySQL DB 연결을 한다
db = mysql.connect(host='ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com', user='root', password='root', db='forstyle', charset='utf8')

class CONVERT_TEXT_TO_XML:
    # File Index
    start = 0
    end = 0
    filename = ""
    rtsp = ""

    # Path Parameter
    WRITE_PATH = 'Label' # xml

    def __init__(self, argvs=[]):
        self.argv_parser(argvs)
        self.read_db(self.start, self.end)

    def argv_parser(self, argvs):
        if (len(argvs) < 5):
            print("Usage > python -filename (String) -rtsp (String) -start (int) -end (int)")
            exit(0)
        for i in range(1, len(argvs), 2):
            if argvs[i] == '-filename' : self.filename = argvs[i + 1]
            if argvs[i] == '-rtsp' : self.rtsp = argvs[i + 1]
            if argvs[i] == '-start': self.start = argvs[i + 1]
            if argvs[i] == '-end': self.end = argvs[i + 1]
        print("TEXT 파일 "+self.filename+ " " + self.rtsp + " " + str(self.start) + " 부터 " + str(self.end) + "까지 XML 파일로 변환합니다")

    def read_db(self, start, end):

        for file_index in range(int(start), int(end), 1):
            with db.cursor() as curs:
                sql = "SELECT product_clothes_label, x1, y1, x2, y2 FROM product WHERE product_file_name="+str(file_index)
                print(sql)
                curs.execute(sql)
                rows = curs.fetchall()
                row = re.sub("[ '()]", "", str(rows))
                row = str(row).split(',')
                label, x1, y1, x2, y2 = row[0], row[1], row[2], row[3], row[4]
                
                #print(str(x1)+str(y1)+str(x2)+str(y2))
                self.make_xml(file_index)
                self.make_line_xml(label, x1, y1, x2, y2)
            self.indent(self.annotation)
            dump(self.annotation)
            file_index = str(file_index)
            ElementTree(self.annotation).write(self.WRITE_PATH + "/image_"+ file_index + ".xml")

    def make_xml(self, file_index):
        file_index = str(file_index)
        self.annotation = Element("annotation")
        SubElement(self.annotation, "folder").text = "forstyle"
        SubElement(self.annotation, "filename").text = "image_" + file_index + ".jpg"

        source = Element("source")
        self.annotation.append(source)
        SubElement(source, "database").text = "forstyle Database"
        SubElement(source, "annotation").text = "forstyle"

        owner = Element("owner")
        self.annotation.append(owner)
        SubElement(owner, "database").text = "forstyle"

        size = Element("size")
        self.annotation.append(size)
        SubElement(size, "width").text = "720"
        SubElement(size, "height").text = "480"
        SubElement(size, "depth").text = "3"

    def make_line_xml(self, label, x1, y1, x2, y2):
        object = Element("object")
        self.annotation.append(object)

        SubElement(object, "name").text = label

        bndbox = Element("bndbox")
        object.append(bndbox)
        SubElement(bndbox, "xmin").text = x1
        SubElement(bndbox, "ymin").text = y1
        SubElement(bndbox, "xmax").text = x2
        SubElement(bndbox, "ymax").text = y2

    def indent(self, elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i


def main(argvs):
    cttx = CONVERT_TEXT_TO_XML(argvs)


if __name__ == '__main__':
    main(sys.argv)