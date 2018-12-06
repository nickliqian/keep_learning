# -*- coding: utf-8 -*-
# @Topic : 
# @Title : 
# @Content : 
# @Author : LiQian
# @Create Time : 2018/12/06 16:52
# @Update Time : 2018/12/06 16:52
import tensorflow as tf
import numpy as np

"""
1. 当我们import tensorflow的时候，就已经创建了一个默认的图了。
import tensorflow as tf
print(tf.get_default_graph())
$ result:
<tensorflow.python.framework.ops.Graph object at 0x7fe0ae6b2208>

2. 有新的操作，默认添加到默认图中
import tensorflow as tf
c = tf.constant(value=1)
print(c.graph)
print(tf.get_default_graph())
$ result:
<tensorflow.python.framework.ops.Graph object at 0x7f39496a90f0>
<tensorflow.python.framework.ops.Graph object at 0x7f39496a90f0>

3. 自定义一个新的图并在新的图中做操作
import tensorflow as tf
print(tf.get_default_graph())
g = tf.Graph()
print(g)
with g.as_default():
    d = tf.constant(value=2)
    print(d.graph)
f = tf.constant(value=2)
print(f.graph)
$ result:
<tensorflow.python.framework.ops.Graph object at 0x7f0debc51dd8>
<tensorflow.python.framework.ops.Graph object at 0x7f0debbad160>
<tensorflow.python.framework.ops.Graph object at 0x7f0debbad160>
你会发现，新建的图和默认图是不一样，在with外面做的操作又属于默认图了

4. as_default前面必须使用with才有效
import tensorflow as tf
print(tf.get_default_graph())
g2 = tf.Graph()
print("g2:", g2)
g2.as_default()
e = tf.constant(value=15)
print(e.graph)
$ result:
<tensorflow.python.framework.ops.Graph object at 0x7f6a1cd14da0>
g2: <tensorflow.python.framework.ops.Graph object at 0x7f6a1cc70240>
<tensorflow.python.framework.ops.Graph object at 0x7f6a1cd14da0>

5. session包含了操作对象执行的环境
import tensorflow as tf
# 向默认图中加入操作
a = tf.constant(2.)
b = tf.constant(5.)
c = a * b
# 创建会话
sess = tf.Session()
# 传入参数，即代表在计算流中计算这个参数
r = sess.run(c)
print(r)
# 关闭会话
sess.close()

6. session上下文管理器
import tensorflow as tf
# 向默认图中加入操作
a = tf.constant(2.)
b = tf.constant(5.)
c = a * b
# 使用上下文管理器
with tf.Session() as sess:
    r = sess.run(c)
print(r)


"""

import tensorflow as tf

import tensorflow as tf
c = tf.constant(2.)

print(tf.get_default_session())
sess1 = tf.Session()
sess2 = tf.Session()

print(sess1)
print(sess2)

with sess1.as_default():
  print(tf.get_default_session())
  print(c.eval())
