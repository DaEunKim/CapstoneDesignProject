# -*- coding: utf-8 -*-
import time, datetime

class Timer(object):
    '''
    A simple timer.
    '''
    def __init__(self):
        self.init_time = time.time()
        self.total_time = 0.
        self.calls = 0
        self.start_time = 0.
        self.diff = 0.
        self.average_time = 0.
        self.remain_time = 0.

    # Function : 시작 시간을 잰다.
    def tic(self):
        # using time.time instead of time.clock because time time.clock
        # does not normalize for multithreading
        self.start_time = time.time()

    # Function : 시작 시간에서 현재 시간(종료)을 빼어, 전체 걸린 시간을 계산한다.
    def toc(self, average=True):
        self.diff = time.time() - self.start_time
        self.total_time += self.diff
        self.calls += 1
        self.average_time = self.total_time / self.calls # 평균 시간을 계산한다.
        if average:
            return self.average_time
        else:
            return self.diff

    # Function : 남은 시간을 계산한다.
    def remain(self, iters, max_iters):
        if iters == 0:
            self.remain_time = 0
        else:
            # 반복수 당 걸리는 시간을 계산한다.
            self.remain_time = (time.time() - self.init_time) * \
                                (max_iters - iters) / iters
        return str(datetime.timedelta(seconds=int(self.remain_time)))
