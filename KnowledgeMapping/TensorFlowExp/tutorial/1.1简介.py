import tensorflow as tf
import numpy as np

# 使用 NumPy 生成假数据(phony data), 总共 100 个点.
x_data = np.float32(np.random.rand(2, 100))  # 随机输入 (2, 100)
y_data = np.dot([0.100, 0.300], x_data) + 0.300  # (1, 2)*(2, 100) + （b） -> (1, 100) + （1）

# 构造一个线性模型
# 训练的过程中var的值会被不断修改
# 而placeholder是用来填充真实的训练数据的
b = tf.Variable(tf.zeros([1]))  # (1)
W = tf.Variable(tf.random_uniform([1, 2], -1.0, 1.0))  # 产生介于 -0.1~0.1之间形状为 (1,2)的矩阵  (1, 2)
y = tf.matmul(W, x_data) + b  # (1, 2)*(2, 100) + （w）  线性模型 matmul代表矩阵的相乘方式

# 最小化方差
loss = tf.reduce_mean(tf.square(y - y_data))  # 计算损失 重要，这里计算目前值与目标值的差，使用梯度下降来不断修改变量的值，直到损失值最小
optimizer = tf.train.GradientDescentOptimizer(0.5)  # 最基本的梯度下降优化器
train = optimizer.minimize(loss)  # 训练以获得最小的损失值

# 初始化变量
init = tf.initialize_all_variables()

# 启动图 (graph)
sess = tf.Session()
writer = tf.summary.FileWriter("logs/", sess.graph)
sess.run(init)

# 拟合平面
for step in range(0, 500):
    sess.run(train)
    if step % 20 == 0:
        print(step, sess.run(W), sess.run(b), sess.run(loss))

# 得到最佳拟合结果 W: [[0.100  0.200]], b: [0.300]