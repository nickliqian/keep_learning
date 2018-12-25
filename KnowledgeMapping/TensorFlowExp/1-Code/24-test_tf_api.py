#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tensorflow as tf
import numpy as np

A = [[1, 3, 4, 5, 6]]
B = [[1, 3, 4, 3, 2]]

correct_pred = tf.equal(A, B)
accuracy = tf.reduce_min(tf.reduce_mean(tf.cast(correct_pred, tf.float32), axis=0))
# accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
# accuracy = tf.cast(correct_pred, tf.float32)

with tf.Session() as sess:
    print(sess.run(accuracy))
