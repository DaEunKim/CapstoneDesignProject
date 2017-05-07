# -*- coding: utf-8 -*-
from xml.etree.ElementTree import ElementTree, Element, SubElement, dump
import sys
import os

class CONVERT_TEXT_TO_XML:
    # File Index
    start = 0
    end = 0
    filename = ""
    rtsp = ""

    # Path Parameter
    READ_PATH = 'Labels' # text
    WRITE_PATH = 'Label' # xml

    def __init__(self, argvs=[]):
        self.argv_parser(argvs)
        self.read_text(self.start, self.end)

    def argv_parser(self, argvs):
        if (len(argvs) < 3):
            print("Usage > python convertXML_Label.py -start (int) -end (int)")
            exit(0)
        for i in range(1, len(argvs), 2):
            if argvs[i] == '-start': self.start = argvs[i + 1]
            if argvs[i] == '-end': self.end = argvs[i + 1]
        print("DB의 "+str(self.start) + " 부터 " + str(self.end) + "까지 XML 파일로 변환합니다")

    def read_text(self, start, end):
        self.READ_PATH = os.path.join(self.READ_PATH, self.filename)
        for file_index in range(int(start), int(end),1000):
            # print(file_index)
            self.make_xml(file_index)
            file_index = str(file_index)
            file_path = os.path.join(self.READ_PATH, self.rtsp + file_index + '.txt')
            print(file_path)
            if not os.path.isfile(file_path):
                continue
            with open(file_path, 'r') as f:
                n = f.readline()
                print(n)
                for line in range(0,int(n),1):
                    line = f.readline()
                    print(line)
                    list = line.split()
                    self.make_line_xml(list)
            self.indent(self.annotation)
            dump(self.annotation)
            ElementTree(self.annotation).write(self.WRITE_PATH + "/" + self.rtsp + file_index + ".xml")

    def make_xml(self, file_index):
        file_index = str(file_index)
        self.annotation = Element("annotation")
        SubElement(self.annotation, "folder").text = "SignTelecom"
        SubElement(self.annotation, "filename").text = self.rtsp + file_index + ".jpg"

        source = Element("source")
        self.annotation.append(source)
        SubElement(source, "database").text = "SignTelecom Database"
        SubElement(source, "annotation").text = "SignTelecom"

        owner = Element("owner")
        self.annotation.append(owner)
        SubElement(owner, "database").text = "KST - KJC"

        size = Element("size")
        self.annotation.append(size)
        SubElement(size, "width").text = "720"
        SubElement(size, "height").text = "480"
        SubElement(size, "depth").text = "3"

    def make_line_xml(self, list):
        object = Element("object")
        self.annotation.append(object)

        SubElement(object, "name").text = "Car"

        bndbox = Element("bndbox")
        object.append(bndbox)
        SubElement(bndbox, "xmin").text = list[0]
        SubElement(bndbox, "ymin").text = list[1]
        SubElement(bndbox, "xmax").text = list[2]
        SubElement(bndbox, "ymax").text = list[3]

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