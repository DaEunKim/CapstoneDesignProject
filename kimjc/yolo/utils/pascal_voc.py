# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ET
import numpy as np
import cv2
import cPickle
import copy
import yolo.config as cfg


class pascal_voc(object):
    def __init__(self, phase, rebuild=False):
        self.devkil_path = os.path.join(cfg.PASCAL_PATH, 'VOCdevkit') # PASCAL Data-set이 있는 위치
        self.data_path = os.path.join(self.devkil_path, 'VOC2007') # VOC 2007, 2012애서 선택한다
        self.cache_path = cfg.CACHE_PATH # Training 할 파일 목록이 저장할 캐쉬(Cache) 경로
        self.batch_size = cfg.BATCH_SIZE # Training Batch 사이즈
        self.image_size = cfg.IMAGE_SIZE # Training Image 사이즈
        self.cell_size = cfg.CELL_SIZE # Training CELL 사이즈
        self.classes = cfg.CLASSES # Training 클래스명들 (현재는 총 20개)
        self.class_to_ind = dict(zip(self.classes, xrange(len(self.classes)))) # ????
        self.flipped = cfg.FLIPPED # 역전 학습
        self.phase = phase
        self.rebuild = rebuild
        self.cursor = 0
        self.epoch = 1
        self.gt_labels = None
        self.prepare() # get()이 호출 전에 준비를 한다.

    def get(self):
        images = np.zeros((self.batch_size, self.image_size, self.image_size, 3))
        labels = np.zeros((self.batch_size, self.cell_size, self.cell_size, 25))
        count = 0
        while count < self.batch_size:
            imname = self.gt_labels[self.cursor]['imname']
            flipped = self.gt_labels[self.cursor]['flipped']
            images[count, :, :, :] = self.image_read(imname, flipped)
            labels[count, :, :, :] = self.gt_labels[self.cursor]['label']
            count += 1
            self.cursor += 1
            if self.cursor >= len(self.gt_labels):
                np.random.shuffle(self.gt_labels)
                self.cursor = 0
                self.epoch += 1
        return images, labels

    def image_read(self, imname, flipped=False):
        image = cv2.imread(imname)
        image = cv2.resize(image, (self.image_size, self.image_size))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)
        image = (image / 255.0) * 2.0 - 1.0
        if flipped:
            image = image[:, ::-1, :]
        return image

    # Function : 라벨을 불러온다.
    def prepare(self):
        gt_labels = self.load_labels()
        if self.flipped:
            print 'Appending horizontally-flipped training examples ...'
            gt_labels_cp = copy.deepcopy(gt_labels)
            for idx in range(len(gt_labels_cp)):
                gt_labels_cp[idx]['flipped'] = True
                gt_labels_cp[idx]['label'] = gt_labels_cp[idx]['label'][:, ::-1, :] # ??
                for i in xrange(self.cell_size):
                    for j in xrange(self.cell_size):
                        if gt_labels_cp[idx]['label'][i, j, 0] == 1:
                            gt_labels_cp[idx]['label'][i, j, 1] = self.image_size - 1 - gt_labels_cp[idx]['label'][i, j, 1]
            gt_labels += gt_labels_cp
        np.random.shuffle(gt_labels)
        self.gt_labels = gt_labels
        return gt_labels

    # Function : cache에 저장된 것이 있다면 불러와 학습할 파일을 가져온다. 없다면 ImageSet에 학습 또는 테스트할 파일명을 불러와 리스트로 저장하고, cache에 저장한다.
    def load_labels(self):
        cache_file = os.path.join(self.cache_path, 'pascal_' + self.phase + '_gt_labels.pkl') # Cache 파일의 경로를 가져온다.
        if os.path.exists(cache_file) and not self.rebuild: # cache 파일이 있다면,
            print 'Loading gt_labels from: ' + cache_file
            with open(cache_file, 'rb') as f: # cache 파일을 오픈한다.
                gt_labels = cPickle.load(f) # cPickle을 이용해 불러온다.
                #  pickle 모듈을 이용해 복잡한 데이터를 가져온다
            return gt_labels

        if self.phase == 'train': # pascal_voc("train") 넘어오는 parameter
            # VOC2007/ImageSets/Main/trainval.txt -> Train - Validation 돌려야할 ImageSets의 파일명의 목록이 적혀있다
            txtname = os.path.join(self.data_path, 'ImageSets', 'Main',
                                    'trainval.txt')
        else:
            # VOC2007/ImageSets/Main/trainval.txt -> Test 돌려야할 ImageSets의 파일명의 목록이 적혀있다
            txtname = os.path.join(self.data_path, 'ImageSets', 'Main',
                                    'test.txt')
        with open(txtname, 'r') as f: # 파일명의 목록이 적혀 잇는 파일을 읽어온다.
            self.image_index = [x.strip() for x in f.readlines()] # 이미지의 인덱스 리스트이며, 파일에서 줄(line)별로 읽어와 저장한다.
            # strip()을 이용해 공백 제거를 한다.

        gt_labels = []
        for index in self.image_index: # 이미지 인덱스 리스트에서 인덱스(파일명)를 가져온다.
            label, num = self.load_pascal_annotation(index) #
            if num == 0:
                continue
            imname = os.path.join(self.data_path, 'JPEGImages', index + '.jpg')
            gt_labels.append({'imname': imname, 'label': label, 'flipped': False})
        print 'Saving gt_labels to: ' + cache_file
        with open(cache_file, 'wb') as f:
            cPickle.dump(gt_labels, f)
        return gt_labels

    # Function : 라벨 xml 파일을 읽어와 디텍팅할 Object 개수를 통해 시작점과 끝점의 x,y 좌표와 label:Class를 가져온다
    def load_pascal_annotation(self, index): # 불러와야할 index(파일명)이 적혀 있다.
        """
        Load image and bounding boxes info from XML file in the PASCAL VOC
        format.
        """
        # traing or test
        imname = os.path.join(self.data_path, 'JPEGImages', index + '.jpg') # index(파일명)의 이미지 경로
        im = cv2.imread(imname) # 이미지를  읽어온다.
        h_ratio = 1.0 * self.image_size / im.shape[0] # 학습으로 정해져있는 이미지와 실제 이미지의 높이의 비율을 계산한다.
        w_ratio = 1.0 * self.image_size / im.shape[1] # 학습으로 정해져있는 이미지와 실제 이미지의 너비의 비율을 계산한다.
        # im = cv2.resize(im, [self.image_size, self.image_size])

        label = np.zeros((self.cell_size, self.cell_size, 25)) # checking,boxes[?,?,?,?] / name:??????
        filename = os.path.join(self.data_path, 'Annotations', index + '.xml') # index(파일명)의 라벨 경로
        tree = ET.parse(filename) # XML의 Element Tree Parsor(파서)로 읽어온다.
        objs = tree.findall('object') # object 태그(하위까지)를 찾는다.

        for obj in objs:
            bbox = obj.find('bndbox') # bndbox 태그를 찾는다.
            # Make pixel indexes 0-based
            # 태그의 값을 가져와, 실제 시작점(x,y)과 끝점(x,y)에서 위에서 구한 비율(width, height)을 곱한 값과, training에 들어갈 이미지 크기를 비교하여 큰 값을 집어 넣는다.
            x1 = max(min((float(bbox.find('xmin').text) - 1) * w_ratio, self.image_size - 1), 0) # 시작점 x 좌표
            y1 = max(min((float(bbox.find('ymin').text) - 1) * h_ratio, self.image_size - 1), 0) # 시작점 y 좌표
            x2 = max(min((float(bbox.find('xmax').text) - 1) * w_ratio, self.image_size - 1), 0) # 끝점 x 좌표
            y2 = max(min((float(bbox.find('ymax').text) - 1) * h_ratio, self.image_size - 1), 0) # 끝점 y 좌표
            cls_ind = self.class_to_ind[obj.find('name').text.lower().strip()] # cls_ind : name 태그는 라벨의 클래스이다.
            # cls_ind(class_index) - 소문자, 공백제거를 한다.
            boxes = [(x2 + x1) / 2, (y2 + y1) / 2, x2 - x1, y2 - y1] # 박스를 계산한다.
            # [ 중심점 x좌표, 중심점 y 좌표, 너비, 높이 ]
            x_ind = int(boxes[0] * self.cell_size / self.image_size) # 중심점 x * cell_size / 448
            y_ind = int(boxes[1] * self.cell_size / self.image_size) # 중심점 y * cell_size / 448
            if label[y_ind, x_ind, 0] == 1:
                continue
            # !!!!!!! 분석이 필요함.
            label[y_ind, x_ind, 0] = 1
            label[y_ind, x_ind, 1:5] = boxes
            label[y_ind, x_ind, 5 + cls_ind] = 1

        return label, len(objs)
