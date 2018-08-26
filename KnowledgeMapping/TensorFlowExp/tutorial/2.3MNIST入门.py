import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import os

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


mnist = input_data.read_data_sets("D:\\A\\data\\mnist\\input_data", one_hot=True)

# input y 占位符
x = tf.placeholder("float", [None, 784])
y_ = tf.placeholder("float", [None, 10])

# 变量：权重，偏置，预测值
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
# 预测值 计算模型
y = tf.nn.softmax(tf.matmul(x, W) + b)

# 测试集评估的时候不会运行到这两步
# 计算成本cast：交叉熵 cross_entropy
cross_entropy = -tf.reduce_sum(y_ * tf.log(y))
# 梯度下降算法，修改变量，降低成本（降低交叉熵，可以设定学习率）
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

# 初始化变量
init = tf.initialize_all_variables()

# 创建会话，初始化变量
sess = tf.Session()
sess.run(init)

# 训练模型
for i in range(1000):
    # 取出一百个随机数据
    # feed数据用来训练
    batch_xs, batch_ys = mnist.train.next_batch(50)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
    # 评估模型 评估准确率
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    # 根据测试集计算所学习到模型目前的准确率
    print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
