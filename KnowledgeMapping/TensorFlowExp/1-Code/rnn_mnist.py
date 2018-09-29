""" Recurrent Neural Network.
A Recurrent Neural Network (LSTM) implementation example using TensorFlow library.
This example is using the MNIST database of handwritten digits (http://yann.lecun.com/exdb/mnist/)
Links:
    [Long Short Term Memory](http://deeplearning.cs.cmu.edu/pdfs/Hochreiter97_lstm.pdf)
    [MNIST Dataset](http://yann.lecun.com/exdb/mnist/).
Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
"""

from __future__ import print_function

import tensorflow as tf
from tensorflow.contrib import rnn

# Import MNIST data
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("D:\A\data\mnist\input_data", one_hot=True)

'''
To classify images using a recurrent neural network, we consider every image
row as a sequence of pixels. Because MNIST image shape is 28*28px, we will then
handle 28 sequences of 28 steps for every sample.
'''

# Training Parameters  训练参数
learning_rate = 0.001  # 学习率
training_steps = 10000  # 训练次数
batch_size = 128  # 每次训练的图片张数
display_step = 200  # 多少次显示一次准确率

# Network Parameters  网络参数
num_input = 28  # MNIST data input (img shape: 28*28)
timesteps = 28  # timesteps
num_hidden = 128  # hidden layer num of features  隐层节点数
num_classes = 10  # MNIST total classes (0-9 digits)  特征种类

# tf Graph input
X = tf.placeholder("float", [None, timesteps, num_input])  # [?, 28, 28]
Y = tf.placeholder("float", [None, num_classes])  # [?, 10]

# Define weights  定义权重和偏偏置
weights = {
    'out': tf.Variable(tf.random_normal([num_hidden, num_classes]))  # [128, 10]
}
biases = {
    'out': tf.Variable(tf.random_normal([num_classes]))  # [10]
}


# 定义网络
def RNN(x, weights, biases):
    # Prepare data shape to match `rnn` function requirements
    # Current data input shape: (batch_size, timesteps, n_input)
    # Required shape: 'timesteps' tensors list of shape (batch_size, n_input)

    # Unstack to get a list of 'timesteps' tensors of shape (batch_size, n_input)
    # x = tf.unstack([?, 28, 28], 28, 1)  每一行看作一个时刻的输入，所有行可以看作是一个连续的时间序列输入
    x = tf.unstack(x, timesteps, 1)  # [?, 28, 28] -> list for 28 ele is [?, 28]
    print("RNN x1", x)
    print("RNN x1", len(x))

    # Define a lstm cell with tensorflow  定义一个LSTM神经元  num_hidden = 128
    lstm_cell = rnn.BasicLSTMCell(num_hidden, forget_bias=1.0)

    # Get lstm cell output  输出  # list for 28 ele is [?, 128] x输入一个28元素的时间序列 输出指定的特征形状
    # 实际上此时就已经作了一个循环神经网络的计算，我们只需要得到最后一个输出，最后一个输出具有前面所有特征的记忆
    #
    outputs, states = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)
    print("outputs", outputs)
    print("outputs", len(outputs))
    print("outputs", outputs[-1])

    print("states", states)  # c [?, 128]  h [?, 128]
    print("states", len(states))

    # Linear activation, using rnn inner loop last output  # 线性激活
    # outputs[-1] 选择最后一个时刻的元素 [?, 128]
    return tf.matmul(outputs[-1], weights['out']) + biases['out']


# 输入 权重 偏置 前面几步主要处理输入得到输出
logits = RNN(X, weights, biases)
prediction = tf.nn.softmax(logits)  # 激活

# Define loss and optimizer  损失和优化器
loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
    logits=logits, labels=Y))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
train_op = optimizer.minimize(loss_op)

# Evaluate model (with test logits, for dropout to be disabled)  评价模型
correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# Initialize the variables (i.e. assign their default value)
init = tf.global_variables_initializer()

# Start training
with tf.Session() as sess:
    # Run the initializer
    sess.run(init)

    for step in range(1, training_steps + 1):
        break
        batch_x, batch_y = mnist.train.next_batch(batch_size)
        print("batch_x", batch_x.shape)  # [128, 784]
        print("batch_y", batch_y.shape)  # [128, 10]
        # Reshape data to get 28 seq of 28 elements
        batch_x = batch_x.reshape((batch_size, timesteps, num_input))  # [128, 28, 28]
        # Run optimization op (backprop)
        sess.run(train_op, feed_dict={X: batch_x, Y: batch_y})  # 训练
        if step % display_step == 0 or step == 1:
            # Calculate batch loss and accuracy  输出准确率
            loss, acc = sess.run([loss_op, accuracy], feed_dict={X: batch_x,
                                                                 Y: batch_y})
            print("Step " + str(step) + ", Minibatch Loss= " + \
                  "{:.4f}".format(loss) + ", Training Accuracy= " + \
                  "{:.3f}".format(acc))

    print("Optimization Finished!")

    # Calculate accuracy for 128 mnist test images
    test_len = 128
    test_data = mnist.test.images[:test_len].reshape((-1, timesteps, num_input))
    test_label = mnist.test.labels[:test_len]
    print("Testing Accuracy:", sess.run(accuracy, feed_dict={X: test_data, Y: test_label}))
