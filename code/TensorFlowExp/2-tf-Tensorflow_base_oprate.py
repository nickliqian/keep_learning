import tensorflow as tf


sess = tf.Session()
# 张量创建数据类型API
# a = tf.zeros([3, 4], tf.float32)
# print(a)
# b = a.eval(session=sess)
# print(b)
#
# c = tf.ones([3, 4], tf.float32)
# print(c)
# b = a.eval(session=sess)
# print(c)

# stddev 标准差
# d = tf.random_normal(([3, 4]), mean=0.0, stddev=1.0)
# print(d.eval(session=sess))
# d = tf.random_normal(([3, 4]), mean=0.0, stddev=2.0)
# print(d.eval(session=sess))

# 类型转换
# e = tf.cast([[1, 2, 3]], tf.float32)
# print(e.eval(session=sess))

# 形状改变


# 切片和扩展


# 数学操作


# 变量 储存 持久化
con = tf.constant([1, 2, 3, 4])
var = tf.Variable([1, 1], [2, 2], name='var')
print(con)
print(var)

# 定义初始化变量的OP
init_op = tf.global_variables_initializer()

with sess:
    sess.run(init_op)
    tf.summary.FileWriter('/home/nick/Desktop/gitProject/ralph_doc_to_chinese/code/TensorFlowExp/board/', graph=sess.graph)
    sess.run([con, var])

