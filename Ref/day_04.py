import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'


# 创建图
# g = tf.Graph()
#
# with g.as_default():
#     a = tf.constant(10.0)
#     b = tf.constant(11.0)
#     c = tf.add(a, b)
#     print(a.graph)
#
# print(g)
#
# con_1 = tf.constant(3.0)
# con_2 = tf.constant(4.0)
#
# # print(con_1)
#
# sum = tf.add(con_1, con_2)
#
# # print(sum)
# print(tf.get_default_graph())
#
#
# with tf.Session(graph=g) as sess:
#     print(con_1.graph)
#     print(con_2.graph)
#     print(sum.graph)
#     print(sess.graph)
#     print(sess.run(sum))



# Python程序

# a = 0.0
# # b = 1
#
# c = a + val_1


# sess = tf.Session()
#
# sess.run(val)
#
# sess.close()
#  会话

# val_1 = tf.constant(3.0)
# # val_2 = tf.constant(4.0)
#
# # 占位符
# plt = tf.placeholder(tf.float32)
#
# example = tf.placeholder(tf.float32, [None, 2])
#
# print(example)
#
#
# sum = tf.add(val_1, plt)
#
#
# with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
#     # print(sess.run([sum, example], feed_dict={plt: 10.0, example: [[1, 2], [3, 4], [7, 8]]}))
#     print(val_1.graph)
#     print("------")
#     print(val_1.op)
#     print("------")
#     print(val_1.name)
#     print("------")
#     print(val_1.shape)


# 静态形状与动态性状
# 1、静态形状不能跨阶转,(4)-->(2,2)
# 2、对于本身形状确定的张量，就不能继续设置静态形状
# 3、动态形状改变，元素个数一定要匹配

# con = tf.constant([1, 2, 3, 4])

# plt = tf.placeholder(tf.float32, [3, 2])
#
# print(plt.get_shape())
#
# # plt.set_shape([2, 2]) 错误
#
# reshape_data = tf.reshape(plt, [2, 4])
#
# print(reshape_data.get_shape())

# 变量

# con = tf.constant([1, 2, 3, 4])
#
# var = tf.Variable([[1, 1], [2, 2]], name="var")
#
# print(con, var)
#
# # 定义一个初始化变量的OP
# init_op = tf.global_variables_initializer()
#
# with tf.Session() as sess:
#     sess.run(init_op)
#     print(var.eval())
#
#     tf.summary.FileWriter('./tmp/summary/test/', graph=sess.graph)
#
#     print(sess.run([con, var]))

#
# def my_linearregression():
#     """
#     自实现线性回归
#     :return: None
#     """
#     with tf.variable_scope("data"):
#         # 1、准备真实的数据，X, matrix[100,1]  Y [100]
#         X = tf.Variable(tf.random_normal([100, 1], mean=0.0, stddev=1.0), name="x_data")
#
#         # 得出真实的目标值
#         y_true = tf.matmul(X, tf.constant([[0.7]])) + 0.8
#
#     with tf.variable_scope("model"):
#         # 2、建立模型，随机指定一些权重和偏置，得出预测结果
#         Weights = tf.Variable(tf.random_normal([1, 1], mean=1.0, stddev=1.0), name="weight")
#         bias = tf.Variable(0.0)
#
#         y_predict = tf.matmul(X, Weights) + bias
#
#     with tf.variable_scope("train"):
#         # 3、训练，梯度下降API--->减少损失，学习率,均方误差
#         loss = tf.reduce_mean(tf.square(y_true - y_predict))
#
#         train_op = tf.train.GradientDescentOptimizer(0.2).minimize(loss)
#
#     # 收集变量
#     tf.summary.scalar("loss", loss)
#     tf.summary.scalar("bias", bias)
#
#     tf.summary.histogram("weight", Weights)
#
#     # 初始化变量
#     init_op = tf.global_variables_initializer()
#
#     # 合并变量
#     merged = tf.summary.merge_all()
#
#     # 创建一个保存实例
#     save = tf.train.Saver()
#
#     # 开启会话
#     with tf.Session() as sess:
#
#         # 初始化变量op
#         sess.run(init_op)
#
#         # 打印初始的权重和偏置
#         print("初始参数，权重%f, 偏置%f" % (Weights.eval(), bias.eval()))
#
#         # 添加事件文件
#         filewriter = tf.summary.FileWriter('./tmp/summary/test/', graph=sess.graph)
#
#         # 判断是否有模型文件，有就直接加载模型
#         if os.path.exists("./tmp/model/checkpoint"):
#             save.restore(sess, "./tmp/model/")
#
#         # 循环迭代优化
#         for i in range(20):
#
#             # 运行训练op
#             sess.run(train_op)
#
#             summ = sess.run(merged)
#
#             filewriter.add_summary(summ, i)
#
#             # 打印更新的参数
#             print("第%d次，更新参数权重%f, 偏置%f" % (i, Weights.eval(), bias.eval()))
#
#         # 保存模型
#         save.save(sess, "./tmp/model/")
#
#     return None
#
#
# if __name__ == "__main__":
#     my_linearregression()




# 自定义命令行参数

tf.app.flags.DEFINE_string("data_dir", "./data/", "数据的目录")
tf.app.flags.DEFINE_integer("max_step", 10000, "训练的次数")

FLAGS = tf.app.flags.FLAGS


def main(argv):
    print(argv)
    print(FLAGS.data_dir)
    print(FLAGS.max_step)


if __name__ == "__main__":
    tf.app.run()


# 图   整个程序，默认注册，创建图
# 会话   掌握很多资源，run(),不能是一个简单运算符，必须是tensor,
    # feed_dict    place_holder

# 张量 形状，数据类型，本身tensor类型
# 初始化，动态性状和静态形状

# 变量   一种特殊的张量，可以保存和加载，但是必须初始化

# tensorboard， 事件文件，

# 自实现线性回归（弄懂，写几遍）
































