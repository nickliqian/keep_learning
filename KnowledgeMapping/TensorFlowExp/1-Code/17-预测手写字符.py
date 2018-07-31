# -*- coding: utf-8 -*-
# @Topic : 
# @Title : 
# @Content : 
# @Author : LiQian
# @Create Time : 2018/07/31 19:08
# @Update Time : 2018/07/31 19:08
# !/usr/bin/python3.5
# -*- coding: utf-8 -*-
import os

import numpy as np
import tensorflow as tf

from PIL import Image

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# 第一次遍历图片目录是为了获取图片总数
input_count = 0
for i in range(0, 10):
    dir_path = '/home/ubuntu/mnist/mnist_digits_images/%s/' % i  # 这里可以改成你自己的图片目录，i为分类标签
    for rt, dirs, files in os.walk(dir_path):
        for filename in files:
            input_count += 1

# 定义对应维数和各维长度的数组
input_images = np.array([[0] * 784 for i in range(input_count)])  # [8000 784]
input_labels = np.array([[0] * 10 for i in range(input_count)])  # [8000 10]

# 第二次遍历图片目录是为了生成图片数据和标签
index = 0
for i in range(0, 10):
    dir_path = '/home/ubuntu/mnist/mnist_digits_images/%s/' % i  # 这里可以改成你自己的图片目录，i为分类标签
    for _, _, files in os.walk(dir_path):
        for filename in files:
            filename = dir_path + filename
            img = Image.open(filename)
            width = img.size[0]
            height = img.size[1]
            for h in range(0, height):
                for w in range(0, width):
                    # 通过这样的处理，使数字的线条变细，有利于提高识别准确率
                    if img.getpixel((w, h)) > 230:
                        input_images[index][w + h * width] = 0
                    else:
                        input_images[index][w + h * width] = 1
            input_labels[index][i] = 1
            index += 1

# 定义输入节点，对应于图片像素值矩阵集合和图片标签(即所代表的数字)
x = tf.placeholder(tf.float32, shape=[None, 784])
y_ = tf.placeholder(tf.float32, shape=[None, 10])

x_image = tf.reshape(x, [-1, 28, 28, 1])

# 定义第一个卷积层的variables和ops
W_conv1 = tf.Variable(tf.truncated_normal([7, 7, 1, 32], stddev=0.1))
b_conv1 = tf.Variable(tf.constant(0.1, shape=[32]))

L1_conv = tf.nn.conv2d(x_image, W_conv1, strides=[1, 1, 1, 1], padding='SAME')
L1_relu = tf.nn.relu(L1_conv + b_conv1)
L1_pool = tf.nn.max_pool(L1_relu, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

# 定义第二个卷积层的variables和ops
W_conv2 = tf.Variable(tf.truncated_normal([3, 3, 32, 64], stddev=0.1))
b_conv2 = tf.Variable(tf.constant(0.1, shape=[64]))

L2_conv = tf.nn.conv2d(L1_pool, W_conv2, strides=[1, 1, 1, 1], padding='SAME')
L2_relu = tf.nn.relu(L2_conv + b_conv2)
L2_pool = tf.nn.max_pool(L2_relu, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

# 全连接层
W_fc1 = tf.Variable(tf.truncated_normal([7 * 7 * 64, 1024], stddev=0.1))
b_fc1 = tf.Variable(tf.constant(0.1, shape=[1024]))

h_pool2_flat = tf.reshape(L2_pool, [-1, 7 * 7 * 64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

# dropout
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

# readout层
W_fc2 = tf.Variable(tf.truncated_normal([1024, 10], stddev=0.1))
b_fc2 = tf.Variable(tf.constant(0.1, shape=[10]))

y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

# 定义优化器和训练op
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
train_step = tf.train.AdamOptimizer((1e-4)).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
saver = tf.train.Saver()
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    saver.restore(sess, "./save/")

    prediction = tf.argmax(y_conv, 1)
    for i in range(1000):
        predint = prediction.eval(feed_dict={x: [input_images[i]], keep_prob: 1.0}, session=sess)
        print('recognize result:')
        print(predint[0])
