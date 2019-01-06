#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import time
import shutil
from PIL import Image
from queue import Queue
from threading import Thread
import hashlib


def change_type(q):
    while True:
        if q.empty():
            print("done")
            break
        file = q.get()
        try:
            print(file)
            input_file = os.path.join(base_dir, file)
            img = Image.open(input_file)

            output_file = os.path.join(output_dir, file.replace(".jpg", ".png"))
            img.save(output_file)

            myhash = hashlib.md5()
            with open(output_file, "wb") as f:
                b = f.read()
                myhash.update(b)
                md5_value = myhash.hexdigest()
            print(md5_value)

        except OSError:
            pass


def main():
    s = time.time()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        pass
    file_list = os.listdir(base_dir)
    q = Queue()

    for f in file_list:
        if f.endswith(".jpg"):
            q.put(f)

    task_list = list()
    for i in range(4):
        t = Thread(target=change_type, args=(q,))
        t.start()
        task_list.append(t)
    for t in task_list:
        t.join()

    e = time.time()
    print("speed time: {}s".format(e - s))


if __name__ == '__main__':
    base_dir = r"D:\A\图像识别\test_change\origin"
    output_dir = r"D:\A\图像识别\test_change\result"
    main()
