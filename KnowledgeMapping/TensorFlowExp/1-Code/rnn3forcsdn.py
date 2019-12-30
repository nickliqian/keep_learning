import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib import rnn
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'


# 定义网络
def rnn_network(X, W, b, nsteps, diminput, dimhidden):
    X1 = tf.transpose(X, [1, 0, 2])
    X2 = tf.reshape(X1, [-1, diminput])
    H_1 = tf.matmul(X2, W["h1"]) + b["b1"]
    H_1 = tf.split(H_1, nsteps, 0)
    lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(dimhidden, forget_bias=1.0)
    LSTM_O, LSTM_S = rnn.static_rnn(lstm_cell, H_1, dtype=tf.float32)
    output = tf.matmul(LSTM_O[-1], W["h2"]) + b["b2"]
    return output


def main():
    mnist = input_data.read_data_sets("MNIST_data", one_hot=True)
    trainimgs, trainlabels, testimgs, testlabels = mnist.train.images, mnist.train.labels, mnist.test.images, mnist.test.labels

    ntrain, ntest, dim, nclasses = trainimgs.shape[0], testimgs.shape[0], trainimgs.shape[1], trainlabels.shape[1]

    # 设置参数，权重，偏置
    diminput = 28
    dimhidden = 128
    dimoutput = nclasses
    nsteps = 28

    W = {
        "h1": tf.Variable(tf.random_normal([diminput, dimhidden])),
        "h2": tf.Variable(tf.random_normal([dimhidden, dimoutput]))
    }

    b = {
        "b1": tf.Variable(tf.random_normal([dimhidden])),
        "b2": tf.Variable(tf.random_normal([dimoutput]))
    }

    learning_rate = 0.001
    x = tf.placeholder("float", [None, nsteps, diminput])  # [count, 28, 28]
    y = tf.placeholder("float", [None, dimoutput])  # [count, 10]

    pred = rnn_network(x, W, b, nsteps, diminput, dimhidden)

    # 交叉熵损失
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=pred))
    # 梯度下降
    optm = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)
    # 准确率
    label_p = tf.argmax(pred, 1)
    label_o = tf.argmax(y, 1)
    accr = tf.reduce_mean(tf.cast(tf.equal(label_p, label_o), tf.float32))

    init = tf.global_variables_initializer()
    print("Network Ready!")

    training_epochs = 5
    batch_size = 16

    sess = tf.Session()
    sess.run(init)

    print("Start optimization")

    for epoch in range(training_epochs):
        avg_cost = 0
        total_batch = int(mnist.train.num_examples / batch_size)

        for i in range(total_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            batch_xs = batch_xs.reshape((batch_size, nsteps, diminput))

            feeds = {x: batch_xs, y: batch_ys}
            sess.run(optm, feed_dict=feeds)

            avg_cost += sess.run(cost, feed_dict=feeds) / total_batch

            if i % 100 == 0:
                print("Epoch: {}/{}  step: {}/{} cost: {}".format(epoch, training_epochs, i, total_batch, avg_cost))
                feeds = {x: batch_xs, y: batch_ys}
                train_acc = sess.run(accr, feed_dict=feeds)
                print("Training accuracy: {}".format(train_acc))

                # testimgs = testimgs.reshape((ntest, nsteps, diminput))
                # feeds = {x: testimgs, y: testlabels}
                # test_acc = sess.run(accr, feed_dict=feeds)
                # print("Test accuracy: {}".format(test_acc))
    print("Optimization Finished")


if __name__ == '__main__':
    main()
