import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

# 创建图
g = tf.Graph()
print(g)
with g.as_default():
    a = tf.constant(1)
    b = tf.constant(2)
    c = tf.add(a, b)
    print(c)
    # 占位符
    plt = tf.placeholder(tf.float32)
    exp = tf.placeholder(tf.float32, [3, 2])
    exp2 = tf.placeholder(tf.float32, [None, 2])


# 这里使用的是默认图
con_1 = tf.constant(3.0)
con_2 = tf.constant(4.0)

sum = tf.add(con_1, con_2)
print(sum)

# 图 程序包含在内
print(tf.get_default_graph())


# 会话 为整个图分配资源
with tf.Session() as sess:
    # 这些数据包含在图中
    print(con_1.graph)
    print(con_2.graph)
    print(sum.graph)
    print(sess.graph)
    print(sess.run(sum))

'''
    图
    操作 op
    数据 Tensor
    会话 Session
'''

p = 1
# 重载运算符
p = p + a


# sess = tf.Session() -> sess.run(...) -> sess.close()
# run 运行 ops和tensor
with tf.Session(graph=g, config=tf.ConfigProto(log_device_placement=True)) as sess_g:
    print('>>>', sess_g.run([a, b, p, plt, exp], feed_dict={plt: 4.0, exp: [[1, 2], [1, 2], [3, 4]]}))
    print('graph >', a.graph)
    print('op >', a.op)
    print('name >', a.name)
    print('shape >', a.shape)

# 交互式

# 张量：
    # 名字
    # 形状 shape 阶
    # 类型
# 张量属性
