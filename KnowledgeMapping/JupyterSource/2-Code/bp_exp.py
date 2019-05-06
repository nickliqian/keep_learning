import tensorflow as tf
from numpy.random import RandomState

# 定义训练数据batch的大小
batch_size = 8
# 随机初始化神经网络的参数
w1 = tf.Variable(tf.random_normal([2, 3], stddev=1, seed=1))  # 3*2的权重矩阵
w2 = tf.Variable(tf.random_normal([3, 1], stddev=1, seed=1))  # 3*1的权重矩阵

# 在shape的一个维度上使用None可以方便使用不同的batch大小。
x = tf.placeholder(tf.float32, shape=(None, 2), name='x-input')
y_ = tf.placeholder(tf.float32, shape=(None, 1), name='y-input')

# 定义计算图
a = tf.matmul(x, w1)  # 前向传播
y = tf.matmul(a, w2)  # 前向传播
cross_entropy = -tf.reduce_mean(y_ * tf.log(tf.clip_by_value(y, 1e-10, 1.0)))  # 定义交叉熵损失函数
train_step = tf.train.AdadeltaOptimizer(0.001).minimize(cross_entropy)  # 定义优化方法为Ada并最小号cross_entropy

# 生成数据集
rdm = RandomState(1)
dataset_size = 128
X = rdm.rand(dataset_size, 2)  # 生成128条二维数据
# 定义数据集样本标签的生成规则，这里x1+x2<1被认为正样本，否则为负样本
Y = [[int(x1 + x2 < 1)] for (x1, x2) in X]  # X对应的标签

# 创建一个Session用来执行图
with tf.Session() as sess:
    # 初始化所有的变量
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
    print(sess.run(w1))
    print(sess.run(w2))
    STEPS = 5000
    # 迭代5000次，每次的batch_size为128
    for i in range(STEPS):
        # 每次选择batch_size个样本进行训练
        start = (i * batch_size) % dataset_size
        end = min(start + batch_size, dataset_size)
        # 通过选取的样本训练神经网络并更新参数
        sess.run(train_step, feed_dict={x: X[start:end], y_: Y[start:end]})
        # 每1000次输出损失函数的结果
        if (i % 1000 == 0):
            total_cross_entropy = sess.run(cross_entropy, feed_dict={x: X, y_: Y})
            print("After %d training step(s),cross entropy on all data is %g" % (i, total_cross_entropy))
    print(sess.run(w1))
    print(sess.run(w2))
