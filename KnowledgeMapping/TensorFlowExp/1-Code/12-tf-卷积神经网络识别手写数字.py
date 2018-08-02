import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


def weight_variable(shape):
    w = tf.Variable(tf.random_normal(shape=shape, mean=0.0, stddev=1.0))
    return w


def bias_variable(shape):
    b = tf.Variable(tf.constant(0.0, shape=shape))
    return b


# 得出卷积层网络模型
def model():
    # 准备输入数据占位符
    with tf.variable_scope("data"):
        x = tf.placeholder(tf.float32, [None, 784])
        y_true = tf.placeholder(tf.int32, [None, 10])

    # 卷积层1
    with tf.variable_scope("conv1"):
        # 初始化卷积层1的参数，5*5 filter的大小，1是图片输入通道，32输出filter数量
        w_conv1 = weight_variable([5, 5, 1, 32])  # filter

        # 初始化偏置量 一个卷积核有一个偏置量
        b_con1 = bias_variable([32])

        # 对输入图片改变形状  [None, 784] -> [-1, 28, 28, 1]
        x_shape = tf.reshape(x, [-1, 28, 28, 1])  # input

        # 进行卷积，激活，池化操作
        # input, filter, strides, padding, use_cudnn_on_gpu=True, data_format="NHWC", name=None
        # 输入    卷积核   步长     边缘,     use_cudnn_on_gpu=True, data_format="NHWC", name=None
        # 卷积 + 偏置量
        x_conv2d1 = tf.nn.conv2d(x_shape, w_conv1, strides=[1, 1, 1, 1], padding="SAME") + b_con1
        # 激活
        x_relu1 = tf.nn.relu(x_conv2d1)
        # 池化
        # value, ksize, strides, padding, data_format="NHWC", name=None
        # 输入   池化窗口
        # 池化窗口 [batch, height, width, channels]  [1, height, width, 1]
        # 步长    [batch, height, width, channels]  [1, stride,stride, 1]
        x_pool1 = tf.nn.max_pool(x_relu1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")

    # 卷积层2
    with tf.variable_scope("conv2"):
        # 初始化卷积层1的参数，5*5 filter的大小，1是图片输入通道，32输出filter数量
        w_conv2 = weight_variable([5, 5, 32, 64])

        # 初始化偏置量
        b_conv2 = bias_variable([64])

        # 进行卷积，激活，池化操作
        x_conv2d2 = tf.nn.conv2d(x_pool1, w_conv2, strides=[1, 1, 1, 1], padding="SAME") + b_conv2
        x_relu2 = tf.nn.relu(x_conv2d2)
        # x_relu2 = tf.nn.relu(tf.nn.conv2d(x_pool1, w_conv2, strides=[1, 1, 1, 1], padding="SAME") + b_conv2)

        # ksize 池化窗口大小
        x_pool2 = tf.nn.max_pool(x_relu2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")

    # 全连接层1
    with tf.variable_scope("FC1"):
        # 首先对上一层结果进行改变 [None, 7, 7, 64] -> [None, 7*7*64]
        x_fc1 = tf.reshape(x_pool2, [-1, 7*7*64])

        # 初始化参数 w,b
        w_fc1 = weight_variable([7 * 7 * 64, 1024])
        b_fc1 = bias_variable([1024])

        # 特征加权计算
        x_fc_matmul1 = tf.matmul(x_fc1, w_fc1) + b_fc1
        x_fc1_relu1 = tf.nn.relu(x_fc_matmul1 + b_fc1)

    # 全连接层2
    with tf.variable_scope("FC1"):
        # 初始化权重和偏置 [1024, 10] -> [10]
        w_fc2 = weight_variable([1024, 10])
        b_fc2 = bias_variable([10])

        # 特征加权计算
        y_predict = tf.matmul(x_fc_matmul1, w_fc2) + b_fc2

    return x, y_true, y_predict


def main():

    mnist = input_data.read_data_sets("/home/nick/Desktop/jupyterNotebook/data/mnist/input_data", one_hot=True)

    # 构建好模型，得出输出结果
    x, y_true, y_predict = model()

    with tf.variable_scope("compute"):
        # 计softmax，交叉熵损失
        loss_soft = tf.nn.softmax_cross_entropy_with_logits(labels=y_true, logits=y_predict)
        loss = tf.reduce_mean(loss_soft)

    # 梯度下降
    with tf.variable_scope("SGD"):
        train_op = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

    # 计算准确率
    with tf.variable_scope("acc"):
        equal_list = tf.equal(tf.argmax(y_true, 1), tf.argmax(y_predict, 1))
        accuracy = tf.reduce_mean(tf.cast(equal_list, tf.float32))

    init_op = tf.global_variables_initializer()
    saver = tf.train.Saver()
    # 会话
    with tf.Session() as sess:
        # 初始化
        sess.run(init_op)

        # 指定迭代次数
        for i in range(10):
            # 获取数据
            mnist_x, mnist_y = mnist.train.next_batch(50)

            # 运行优化器 运行梯度下降OP
            sess.run(train_op, feed_dict={x: mnist_x, y_true: mnist_y})

            print("准确率：", sess.run(accuracy, feed_dict={x: mnist_x, y_true: mnist_y}))

        print("测试集里面的准确率：", sess.run(accuracy, feed_dict={x: mnist.test.images, y_true: mnist.test.labels}))

        # 加载模型
        saver.restore(sess, "./ckpt/")
        for i in range(100):
            x_test, y_test = mnist.test.next_batch(1)
            print("图片{} 原始值{} 目标值{}"
                  .format(i,
                          tf.argmax(y_test, 1).eval(),
                          tf.argmax(sess.run(y_predict, feed_dict={x: x_test, y_true: y_test}), 1).eval()))

    return None


if __name__ == "__main__":
    main()















