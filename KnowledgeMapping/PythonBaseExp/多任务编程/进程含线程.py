import threading
import time
from multiprocessing import Process, Pool
import os
import random


class Work(threading.Thread):

    def __init__(self, process_name, thread_name):
        super(Work, self).__init__()
        self.process_name = process_name
        self.thread_name = thread_name

    def study(self):
        print("study {} {}".format(self.process_name, self.thread_name))
        r = random.random()
        time.sleep(r)

    def sleep(self):
        print("sleep {} {}".format(self.process_name, self.thread_name))
        r = random.random()
        time.sleep(r)

    def work(self):
        print("work {} {}".format(self.process_name, self.thread_name))
        r = random.random()
        time.sleep(r)

    def run(self):
        self.study()
        self.sleep()
        self.work()
        self.study()
        self.sleep()
        self.work()
        self.study()
        self.sleep()
        self.work()


def more_threading(process_name):
    print('Run child process %s (%s)...' % (process_name, os.getpid()))
    num = 5
    jobList = []
    for i in range(1, num + 1):
        thread_name = "Thread" + str(i)
        c = Work(process_name, thread_name)
        c.start()
        jobList.append(c)
    # 主线程等待子线程
    for t in jobList:
        t.join()


if __name__ == '__main__':
    print('Parent process %s.' % os.getpid())
    process_num = 3
    p = Pool(process_num)
    for i in range(1, process_num+1):
        p.apply_async(more_threading, args=("Process-" + str(i),))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')


