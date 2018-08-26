# encoding=utf-8
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import os

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

mnist = input_data.read_data_sets("D:\\A\\data\\mnist\\input_data", one_hot=True)


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


myGraph = tf.Graph()
with myGraph.as_default():
    with tf.name_scope('inputsAndLabels'):
        x_raw = tf.placeholder(tf.float32, shape=[None, 784])
        y = tf.placeholder(tf.float32, shape=[None, 10])

    with tf.name_scope('hidden1'):
        x = tf.reshape(x_raw, shape=[-1, 28, 28, 1])
        W_conv1 = weight_variable([5, 5, 1, 32])
        b_conv1 = bias_variable([32])
        l_conv1 = tf.nn.relu(tf.nn.conv2d(x, W_conv1, strides=[1, 1, 1, 1], padding='SAME') + b_conv1)
        l_pool1 = tf.nn.max_pool(l_conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

        tf.summary.image('x_input', x, max_outputs=10)
        tf.summary.histogram('W_con1', W_conv1)
        tf.summary.histogram('b_con1', b_conv1)

    with tf.name_scope('hidden2'):
        W_conv2 = weight_variable([5, 5, 32, 64])
        b_conv2 = bias_variable([64])
        l_conv2 = tf.nn.relu(tf.nn.conv2d(l_pool1, W_conv2, strides=[1, 1, 1, 1], padding='SAME') + b_conv2)
        l_pool2 = tf.nn.max_pool(l_conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

        tf.summary.histogram('W_con2', W_conv2)
        tf.summary.histogram('b_con2', b_conv2)

    with tf.name_scope('fc1'):
        W_fc1 = weight_variable([64 * 7 * 7, 1024])
        b_fc1 = bias_variable([1024])
        l_pool2_flat = tf.reshape(l_pool2, [-1, 64 * 7 * 7])
        l_fc1 = tf.nn.relu(tf.matmul(l_pool2_flat, W_fc1) + b_fc1)
        keep_prob = tf.placeholder(tf.float32)
        l_fc1_drop = tf.nn.dropout(l_fc1, keep_prob)

        tf.summary.histogram('W_fc1', W_fc1)
        tf.summary.histogram('b_fc1', b_fc1)

    with tf.name_scope('fc2'):
        W_fc2 = weight_variable([1024, 10])
        b_fc2 = bias_variable([10])
        y_conv = tf.matmul(l_fc1_drop, W_fc2) + b_fc2

        tf.summary.histogram('W_fc1', W_fc1)
        tf.summary.histogram('b_fc1', b_fc1)

    with tf.name_scope('train'):
        cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y_conv, labels=y))
        train_step = tf.train.AdamOptimizer(learning_rate=1e-4).minimize(cross_entropy)
        correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        tf.summary.scalar('loss', cross_entropy)
        tf.summary.scalar('accuracy', accuracy)

with tf.Session(graph=myGraph) as sess:
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver()

    merged = tf.summary.merge_all()
    summary_writer = tf.summary.FileWriter("C:/tf_logs", graph=sess.graph)

    for i in range(100):
        batch = mnist.train.next_batch(50)
        sess.run(train_step, feed_dict={x_raw: batch[0], y: batch[1], keep_prob: 0.5})
        if i % 50 == 0:
            train_accuracy = accuracy.eval(feed_dict={x_raw: batch[0], y: batch[1], keep_prob: 1.0})
            print('step %d training accuracy:%g' % (i, train_accuracy))

            summary = sess.run(merged, feed_dict={x_raw: batch[0], y: batch[1], keep_prob: 1.0})
            summary_writer.add_summary(summary, i)

    test_accuracy = accuracy.eval(feed_dict={x_raw: mnist.test.images, y: mnist.test.labels, keep_prob: 1.0})
    print('test accuracy:%g' % test_accuracy)

    saver.save(sess, save_path='./model/mnistmodel', global_step=1)
