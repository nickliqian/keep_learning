import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


def main(argv):

    # 获取数据实例
    mnist = input_data.read_data_sets("D:/A/data/mnist/input_data/", one_hot=True)

    # 准备数据占位符，x ->[None, 784]  y_true-->[None, 10]
    with tf.variable_scope("data"):
        # 手写数字特征值
        x = tf.placeholder(tf.float32, [None, 784])

        # 手写数字的目标值
        y_true = tf.placeholder(tf.int32, [None, 10])

    # 准备参数，建立模型，w->[784, 10] b->[10]
    with tf.variable_scope("model"):
        # 权重
        weights = tf.Variable(tf.random_normal([784, 10], mean=0.0, stddev=1.0), name="weight")

        # 偏置
        bias = tf.Variable(tf.constant(0.0, shape=[10]), name="bias")

        # 通过矩阵运算得出预测结果[None, 784] *[784, 10] + [10]
        y_predict = tf.matmul(x, weights) + bias

    # softmax回归，以及交叉熵损失计算
    with tf.variable_scope("loss"):
        # labels-->真实值， logits-->预测值
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_true, logits=y_predict))

    # 梯度下降
    with tf.variable_scope("SGD"):
        train_op = tf.train.GradientDescentOptimizer(0.3).minimize(loss)

    # 计算准确率
    equal_list = tf.equal(tf.argmax(y_true, 1), tf.argmax(y_predict, 1))

    accuracy = tf.reduce_mean(tf.cast(equal_list, tf.float32))

    # 收集损失和准确率，权重
    tf.summary.scalar("loss", loss)

    tf.summary.scalar("accuracy", accuracy)

    tf.summary.histogram("weght", weights)

    # 变量初始化op
    init_op = tf.global_variables_initializer()

    # 合并变量
    merged = tf.summary.merge_all()

    with tf.Session() as sess:

        # 初始化变量
        sess.run(init_op)

        # 建立事件文件
        filewriter = tf.summary.FileWriter("./tmp11/", graph=sess.graph)

        # 指定迭代次数去训练
        for i in range(1000):

            mnist_x, mnist_y = mnist.train.next_batch(50)

            # 运行梯度下降op
            sess.run(train_op, feed_dict={x: mnist_x, y_true: mnist_y})

            print("准确率：", sess.run(accuracy, feed_dict={x: mnist_x, y_true: mnist_y}))

            # 运行收集op
            summary = sess.run(merged, feed_dict={x: mnist_x, y_true: mnist_y})

            # 写入事件文件
            filewriter.add_summary(summary, i)

        print("测试集里面的准确率：", sess.run(accuracy, feed_dict={x: mnist.test.images, y_true: mnist.test.labels}))

    return None


if __name__ == "__main__":
    tf.app.run()