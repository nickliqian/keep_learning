import tensorflow as tf


def get_batch(count):
    x_train = None
    y_train = None
    return x_train, y_train


def get_test_batch():
    x_test = None
    y_test = None
    return x_test, y_test


def weight_variable(shape):
    """
    返回指定形状的权重
    :param shape:list
    :return:tf.Variable
    """
    w = tf.Variable(tf.random_normal(shape=shape, mean=0.0, stddev=1.0))
    return w


def bias_variable(shape):
    """
    返回指定形状的偏置量
    :param shape:
    :return:
    """
    b = tf.Variable(tf.constant(0.0, shape=shape))
    return b


def model():
    # 输入占位符，与输入形状保持一致
    with tf.variable_scope("data"):
        x = tf.placeholder(tf.float32, [None, 784])  # [100, 784]
        y_true = tf.placeholder(tf.int32, [None, 10])  # [100, 10]

    # 卷积层1
    with tf.variable_scope("conv1"):
        w_conv1 = weight_variable([5, 5, 1, 32])  # 权重
        b_conv1 = bias_variable([32])  # 偏置
        x_reshape_conv1 = tf.reshape(x, [-1, 28, 28, 1])  # 转为 [size, height, width, channel] 格式
        conv_conv1 = tf.nn.conv2d(x_reshape_conv1, w_conv1, strides=[1, 1, 1, 1], padding="SAME") + b_conv1  # 卷积
        relu_conv1 = tf.nn.relu(conv_conv1)  # 将卷积之后的结果带入激活函数
        pool_conv1 = tf.nn.max_pool(relu_conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")  # [-1, 14, 14, 32]
        print(pool_conv1)

    # 卷积层2 input [-1, 14, 14, 32]
    with tf.variable_scope("conv2"):
        w_conv2 = weight_variable([5, 5, 32, 64])  # 注意权重的通道数有更新
        b_conv2 = bias_variable([64])
        conv_conv2 = tf.nn.conv2d(pool_conv1, w_conv2, strides=[1, 1, 1, 1], padding="SAME") + b_conv2
        relu_conv2 = tf.nn.relu(conv_conv2)
        pool_conv2 = tf.nn.max_pool(relu_conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")
        print(pool_conv2)

    # 全连接层1 input [-1, 7, 7, 64] -> [-1, 7*7*64] * [1024, X] -> [-1, 1024]
    with tf.variable_scope("fc1"):
        w_fc1 = weight_variable([7*7*64, 1024])  # 最后一位代表输出的通道数量
        b_fc1 = bias_variable([1024])  # 偏置通道数量与权重一样，即是有多少权重就有多少偏置量
        x_reshape_fc1 = tf.reshape(pool_conv2, [-1, 7*7*64])
        matmul_fc1 = tf.matmul(x_reshape_fc1, w_fc1) + b_fc1  # 特征加权计算
        relu_fc1 = tf.nn.relu(matmul_fc1 + b_fc1)
        print(relu_fc1)

    # 全连接层2
    with tf.variable_scope("fc2"):
        w_fc2 = weight_variable([1024, 10])
        b_fc2 = bias_variable([10])
        matmul_fc2 = tf.matmul(relu_fc1, w_fc2) + b_fc2
        y_predict = matmul_fc2  # 数值
        print(y_predict)
    return x, y_true, y_predict


def main():
    x, y_true, y_predict = model()
    print(x, y_true, y_predict)

    # 计算softmax，交叉熵损失 oneHot >>> 全连接后的数值
    with tf.variable_scope("compute"):
        loss_soft = tf.nn.softmax_cross_entropy_with_logits(labels=y_true, logits=y_predict)
        print("loss_soft", loss_soft)
        loss = tf.reduce_mean(loss_soft)
        print("loss", loss)

    # 梯度下降
    with tf.variable_scope("SGD"):
        train_op = tf.train.GradientDescentOptimizer(0.0001).minimize(loss)

    # 计算准确率
    with tf.variable_scope("acc"):
        equal_list = tf.equal(tf.argmax(y_true, 1), tf.argmax(y_predict, 1))  # 判断最大值的位数是否一致
        accuracy = tf.reduce_mean(tf.cast(equal_list, tf.float32))  # 求得准确率

    init_op = tf.global_variables_initializer()
    saver = tf.train.Saver()

    with tf.Session() as sess:
        sess.run(init_op)

        # 训练
        for i in range(100):
            x_train, y_train = get_batch(100)
            sess.run(train_op, feed_dict={x: x_train, y_true: y_train})  # 运行优化器
            accuracy_value = sess.run(accuracy, feed_dict={x: x_train, y_true: y_train})  # 计算准确率
            print("loop<{}>  accuracy: {}".format(i, accuracy_value))

        # 验证测试集
        x_test, y_test = get_test_batch()
        test_accuracy_value = sess.run(accuracy, feed_dict={x: x_test, y_true: y_test})  # 计算准确率
        print("test set accuracy: {}".format(test_accuracy_value))


if __name__ == '__main__':
    main()
