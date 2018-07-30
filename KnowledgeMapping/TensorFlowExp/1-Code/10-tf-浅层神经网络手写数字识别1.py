import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


def main():

    mnist = input_data.read_data_sets("D:\A\data\mnist\input_data", one_hot=True)

    with tf.variable_scope("data"):
        x = tf.placeholder(tf.float32, [None, 784])

        y_true = tf.placeholder(tf.int32, [None, 10])

    with tf.variable_scope("model"):
        weights = tf.Variable(tf.random_normal([784, 10], mean=0.0, stddev=1.0), name="weight")

        bias = tf.Variable(tf.constant(0.0, shape=[10]), name="bias")

        y_predict = tf.matmul(x, weights) + bias

    with tf.variable_scope("loss"):
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_true, logits=y_predict))

    with tf.variable_scope("SGD"):
        train_op = tf.train.GradientDescentOptimizer(0.3).minimize(loss)

    # 计算准确率
    equal_list = tf.equal(tf.argmax(y_true, 1), tf.argmax(y_predict, 1))
    accuracy = tf.reduce_mean(tf.cast(equal_list, tf.float32))

    init_op = tf.global_variables_initializer()

    with tf.Session() as sess:

        sess.run(init_op)

        for i in range(100):
            mnist_x, mnist_y = mnist.train.next_batch(50)

            # 运行梯度下降OP
            sess.run(train_op, feed_dict={x: mnist_x, y_true: mnist_y})

            print("准确率：", sess.run(accuracy, feed_dict={x: mnist_x, y_true: mnist_y}))

        print("测试集里面的准确率：", sess.run(accuracy, feed_dict={x: mnist.test.images, y_true: mnist.test.labels}))

    return None


if __name__ == "__main__":
    main()