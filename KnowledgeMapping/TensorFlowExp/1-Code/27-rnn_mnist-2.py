import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib import rnn
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'


# 定义网络
def RNN(X, W, b, nsteps, diminput, dimhidden):
    print("a >", X)  # (16, 28, 28)
    X1 = tf.transpose(X, [1, 0, 2])  # > (28, 16, 28)
    print("b >", X1)
    X2 = tf.reshape(X1, [-1, diminput])  # > (16*28, 28)
    print("c >", X2)
    H_1 = tf.matmul(X2, W["h1"]) + b["b1"]  # (16*28, 128) = (16*28, 28) * (28, 128) + (128)
    print("d >", H_1)
    H_1 = tf.split(H_1, nsteps, 0)  # [(16, 128), (16, 128), ...] length is 28
    print("f >", H_1)
    print("f >", len(H_1))
    lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(dimhidden, forget_bias=1.0)  # 128
    print("lstm_cell", lstm_cell)
    LSTM_O, LSTM_S = rnn.static_rnn(lstm_cell, H_1, dtype=tf.float32)  # LSTM_O 28 (16, 128)
    print("LSTM_O", LSTM_O)
    print("LSTM_O[-1]", LSTM_O[-1])  # (16, 128)
    O = tf.matmul(LSTM_O[-1], W["h2"]) + b["b2"]  # (?, 10) = (16, 128) * (128, 10) + (10)
    return {"X": X, "H_1": H_1, "LSTM_O": LSTM_O, "LSTM_S": LSTM_S, "OUT": O, "X1": X1, "X2": X2, "lstm_cell": lstm_cell}


def main():
    mnist = input_data.read_data_sets("MNIST_data", one_hot=True)
    trainimgs, trainlabels, testimgs, testlabels = mnist.train.images, mnist.train.labels, mnist.test.images, mnist.test.labels

    ntrain, ntest, dim, nclasses = trainimgs.shape[0], testimgs.shape[0], trainimgs.shape[1], trainlabels.shape[1]

    print("====================================>>>")
    print("====================================>>>")
    print("====================================>>>")
    print("====================================>>>")

    # ntrain 55000
    # ntest 10000
    # dim 784
    # nclasses 10
    print("ntrain", ntrain)
    print("ntest", ntest)
    print("dim", dim)
    print("nclasses", nclasses)

    # 设置参数，权重，偏置
    diminput = 28
    dimhidden = 128
    dimoutput = nclasses
    nsteps = 28

    W = {
        "h1": tf.Variable(tf.random_normal([diminput, dimhidden])),  # [28, 128]
        "h2": tf.Variable(tf.random_normal([dimhidden, dimoutput]))  # [128, 10]
    }

    b = {
        "b1": tf.Variable(tf.random_normal([dimhidden])),  # [128]
        "b2": tf.Variable(tf.random_normal([dimoutput]))  # [10]
    }

    learning_rate = 0.001
    x = tf.placeholder("float", [None, nsteps, diminput])  # [count, 28, 28]
    y = tf.placeholder("float", [None, dimoutput])  # [count, 10]

    #                       28       10        128
    rmodel = RNN(x, W, b, nsteps, diminput, dimhidden)

    pred = rmodel["OUT"]

    # 交叉熵损失
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=pred))
    # 梯度下降
    optm = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)
    # 准确率
    accr = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1)), tf.float32))

    init = tf.global_variables_initializer()
    print("Network Ready!")

    training_epochs = 5
    batch_size = 16
    display_step = 1

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
            print(batch_xs.shape)
            print(batch_ys.shape)
            a, b, c, d, f, g = sess.run([optm, rmodel["X1"], rmodel["X2"], rmodel["H_1"], rmodel["LSTM_O"], rmodel["LSTM_S"]], feed_dict=feeds)
            print("X1", b.shape)
            print("X2", c.shape)
            print("H_1", len(d), d[0].shape)
            print("LSTM_O", len(f), f[0].shape)
            print("LSTM_S", len(g), g[0].shape)
            # print("lstm_cell", e)

            avg_cost += sess.run(cost, feed_dict=feeds) / total_batch

            if epoch % display_step == 0:
                print("Epoch: {}/{} cost: {}".format(epoch, training_epochs, avg_cost))
                feeds = {x: batch_xs, y: batch_ys}
                train_acc = sess.run(accr, feed_dict=feeds)
                print("Training accuracy: {}".format(train_acc))

                testimgs = testimgs.reshape((ntest, nsteps, diminput))
                feeds = {x: testimgs, y: testlabels}
                test_acc = sess.run(accr, feed_dict=feeds)
                print("Test accuracy: {}".format(test_acc))
    print("Optimization Finished")


if __name__ == '__main__':
    main()
