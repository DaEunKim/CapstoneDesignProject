# -*- coding: utf-8 -*-
import tensorflow as tf
import numpy as np
import datetime
import os
import argparse
import yolo.config as cfg
from yolo.yolo_net import YOLONet
from utils.timer import Timer
from utils.pascal_voc import pascal_voc


class Solver(object):

    # Solver 객체 생성
    def __init__(self, net, data):
        self.net = net # YOLO CNN MODEL
        self.data = data # PASCAL VOC DATA
        self.weights_file = cfg.WEIGHTS_FILE # 저장할 CKPT 파일

        # Learning step/rate
        self.max_iter = cfg.MAX_ITER # 최대 iteration 반복수
        self.initial_learning_rate = cfg.LEARNING_RATE # Training learning rate

        # Decay step/rate
        self.decay_steps = cfg.DECAY_STEPS # decay_step
        self.decay_rate = cfg.DECAY_RATE # Training decaying the learning rate

        # Iterator
        self.staircase = cfg.STAIRCASE
        self.summary_iter = cfg.SUMMARY_ITER # Summary 를 저장할 단계수
        self.save_iter = cfg.SAVE_ITER # CKPT 를 저장한 단계수

        # output_dir에는 년도,달,시간,분 대로 ckpt와 summary를 저장되는 디렉토리이다.
        self.output_dir = os.path.join(cfg.OUTPUT_DIR,
            datetime.datetime.now().strftime('%Y_%m_%d_%H_%M'))
        if not os.path.exists(self.output_dir): # output_dir 디렉토리가 없다면
            os.makedirs(self.output_dir) # output_dir 디렉토리를 생성한다.
        self.save_cfg() # config 파일을 저장한다.

        self.global_step = tf.get_variable('global_step', [],
            initializer=tf.constant_initializer(0), trainable=False)
        # global_step 을 가져온다. 새로 생성된다면 0으로 초기화한다.
        # tf.get_variable : 파라밑터로 이미 존재하는 변수를 가져오거나 새로 만든다.

        self.learning_rate = tf.train.exponential_decay(
            self.initial_learning_rate, self.global_step, self.decay_steps,
            self.decay_rate, self.staircase, name='learning_rate')
        # tf.exponential_decay : 학습 상수(learning rate)에 지수 decay를 적용한다.
        # -- decayed_learning_rate = learning_rate * decay_rate * (global_step / decay_steps)

        # self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.net.loss, global_step=self.global_step)
        self.optimizer = tf.train.GradientDescentOptimizer(
            learning_rate=self.learning_rate).minimize(
            self.net.loss, global_step=self.global_step)
        # tf.train.GradientDescentOptimize : Gradient descent 알고리즘을 이용한 Optimizer

        self.ema = tf.train.ExponentialMovingAverage(decay=0.9999)
        # tf.train.ExponentialMovingAverage : 지수(exponential decay)를 이용해 평균으로 이동함을 유지한다
        # Evalutaions that use averaged parameters sometimes produce significantly better results than the final trained values.

        self.averages_op = self.ema.apply(tf.trainable_variables()) # tf.trainable_variables() : trainable=True인 모든 변수를 반환한다.

        # tf.control_dependencies(control_inputs) : default graph을 사용하여 감싼다
        # - parameter인 control_inputs은 Tensor 또는 Operation으로 실행, 계산 가능한 Operation
        with tf.control_dependencies([self.optimizer]):
            self.train_op = tf.group(self.averages_op)

        self.summary_op = tf.summary.merge_all() # tf.summary.merge_all : graph에서 모든 summary(요약)을 합친다.

        self.saver = tf.train.Saver(self.net.collection, max_to_keep=None) # tf.train.Saver() tf변수를 저장하거나 불러오는 class.

        self.writer = tf.summary.FileWriter(self.output_dir, flush_secs=60) # tf.summary.FileWriter() 요약과 이벤트를 주어진 디렉터리에 이벤트 파일을 생성하는 class.
        self.ckpt_file = os.path.join(self.output_dir, 'save.ckpt') # ckpt가 저장될 path

        self.sess = tf.Session() # tf.Session() : TensorFlow operations을 실행하는 class
        self.sess.run(tf.global_variables_initializer()) # tf.global_variables_initialize 변수 초기화를 한다.

        # 기존의 weight 파일이 있다면 saver에서 불러온다.
        if self.weights_file is not None: # weight 파일이 있다면
            print 'Restoring weights from: ' + self.weights_file
            self.saver.restore(self.sess, self.weights_file) # ckpt 파일을 불러온다.

        self.writer.add_graph(self.sess.graph) # event file에 Graph를 추가한다

    # Function : CNN 모델은 training 한다.
    def train(self):

        train_timer = Timer() # 타이머 : 실제 training 하는데 걸리는 시간을 계산
        load_timer = Timer() # 타이머 : data-set에서 데이터를 읽어오는데(load) 걸리는 시간을 계산

        # max_iter 반복 수 만큼 step을 진행한다.
        for step in xrange(1, self.max_iter + 1):

            # data-set에서 데이터를 읽어오는데 걸리는 시간을 계산한다.
            load_timer.tic() # 타이머를 시작
            """data-set(image,label) 가져온다."""
            images, labels = self.data.get() # 이미지와 라벨을 가져온다.
            # 여기서의 data는 pascal이며 main문에서 pascal = pascal_voc('train'), utils.pascal_voc 참고.
            load_timer.toc() # 타이머를 종료

            feed_dict = {self.net.x: images, self.net.labels: labels}

            if step % self.summary_iter == 0:
                if step % (self.summary_iter * 10) == 0:
                    run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
                    run_metadata = tf.RunMetadata()

                    train_timer.tic()
                    summary_str, loss, _ = self.sess.run(
                        [self.summary_op, self.net.loss, self.train_op],
                        feed_dict=feed_dict)
                    train_timer.toc()

                    self.writer.add_run_metadata(run_metadata,
                            'step_{}'.format(step), step)

                    log_str = ('{} Epoch: {}, Step: {}, Learning rate: {},'
                        ' Loss: {:5.3f}\nSpeed: {:.3f}s/iter,'
                        ' Load: {:.3f}s/iter, Remain: {}').format(
                        datetime.datetime.now().strftime('%m/%d %H:%M:%S'),
                        self.data.epoch,
                        int(step),
                        round(self.learning_rate.eval(session=self.sess), 6),
                        loss,
                        train_timer.average_time,
                        load_timer.average_time,
                        train_timer.remain(step, self.max_iter))
                    print log_str

                else:
                    train_timer.tic()
                    summary_str, _ = self.sess.run(
                        [self.summary_op, self.train_op],
                        feed_dict=feed_dict)
                    train_timer.toc()

                self.writer.add_summary(summary_str, step)

            else:
                train_timer.tic()
                _ = self.sess.run(self.train_op, feed_dict=feed_dict)
                train_timer.toc()

            if step % self.save_iter == 0:
                print '{} Saving checkpoint file to: {}'.format(
                    datetime.datetime.now().strftime('%m/%d %H:%M:%S'),
                    self.output_dir)
                self.saver.save(self.sess, self.ckpt_file,
                    global_step=self.global_step)

    # Function : config 파일을 저장한다.
    def save_cfg(self):
        with open(os.path.join(self.output_dir, 'config.txt'), 'w') as f: # 파일 쓰기를 한다.
            cfg_dict = cfg.__dict__ # __dict__ : 클래스의 독립적인 네임스페이스를 딕셔너리(Dictionary) 타입으로 저장한다.
            for key in sorted(cfg_dict.keys()): # 올림차순으로 정렬한다
                if key[0].isupper(): # isupper : 모드 문자가 대문자일 경우 True를 반환한다.
                    cfg_str = '{}: {}\n'.format(key, cfg_dict[key])
                    f.write(cfg_str) # 파일에 쓴다.


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', default=None, type=str)
    parser.add_argument('--gpu', default=None, type=int)
    args = parser.parse_args()

    if args.weights is not None:
        cfg.WEIGHTS_FILE = os.path.join(cfg.WEIGHTS_DIR, args.weights)
    if args.gpu is not None:
        cfg.GPU = str(args.gpu)

    cfg.GPU = '0,1,2,3'
    cfg.WEIGHTS_FILE = os.path.join(cfg.WEIGHTS_DIR, 'YOLO_small.ckpt')
    # cfg.DISPLAY_ITER = 1

    os.environ['CUDA_VISIBLE_DEVICES'] = cfg.GPU

    yolo = YOLONet('train')
    pascal = pascal_voc('train')

    solver = Solver(yolo, pascal) # Solver instance 생성

    solver.train()

if __name__ == '__main__':

    # python train.py --weights YOLO_small.ckpt --gpu 0
    main()
