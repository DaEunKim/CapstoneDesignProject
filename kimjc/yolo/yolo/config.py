# -*- coding: utf-8 -*-
import os

"""
Path Parameter
각 종 디렉토리의 경로명 작성
"""
DATA_PATH = 'data'

# PASCAL 이미지 데이터셋과 라벨이 포함된 경로명
PASCAL_PATH = os.path.join(DATA_PATH, 'pascal_voc')

CACHE_PATH = os.path.join(DATA_PATH, 'cache')

OUTPUT_DIR = os.path.join(DATA_PATH, 'output')

WEIGHTS_DIR = os.path.join(DATA_PATH, 'weights')

WEIGHTS_FILE = None

# .ckpt 모델에 이어서 Training 시킬 경우,
# WEIGHTS_FILE = os.path.join(DATA_PATH, 'weights', 'YOLO_small.ckpt')

# Training 클래스의 종류
CLASSES = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
           'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant', 'sheep', 'sofa',
           'train', 'tvmonitor']

# 역전 학습
FLIPPED = True


"""
Model Parameter
CNN 모델의 파라미터 설정
"""

IMAGE_SIZE = 448

CELL_SIZE = 7

BOXES_PER_CELL = 2

ALPHA = 0.1

DISP_CONSOLE = False

OBJECT_SCALE = 1.0
NOOBJECT_SCALE = 1.0
CLASS_SCALE = 2.0
COORD_SCALE = 5.0


"""
Solver Paramter
"""

GPU = ''

LEARNING_RATE = 0.0001

DECAY_STEPS = 30000

DECAY_RATE = 0.1
# https://www.tensorflow.org/api_docs/python/tf/train/exponential_decay

STAIRCASE = True

BATCH_SIZE = 45

MAX_ITER = 15000

SUMMARY_ITER = 10

SAVE_ITER = 1000

"""
Model Test Paramter
"""
THRESHOLD = 0.2

IOU_THRESHOLD = 0.5
