import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'


'''
    图
    操作 op
    数据 Tensor
    会话 Session
'''


# 1. 创建图
g = tf.Graph()
print(g)
with g.as_default():
    a = tf.constant(1)
    b = tf.constant(2)
    c = tf.add(a, b)
    print('add运算后的张量：', c)
    # 使用占位符
    plt = tf.placeholder(tf.float32)
    exp = tf.placeholder(tf.float32, [3, 2])
    exp2 = tf.placeholder(tf.float32, [None, 2])


# 2. 使用默认图创建tensor和op --> 图将程序包含在内
con_1 = tf.constant(3.0)
con_2 = tf.constant(4.0)
sum_m = tf.add(con_1, con_2)
print(sum_m)
print(tf.get_default_graph())  # 查看默认图


# 3. 会话，为整个图分配资源 ------> sess = tf.Session() -> sess.run(...) -> sess.close()
with tf.Session() as sess:
    print('查看张量con_1所在的图：', con_1.graph)  # 打印Tensor --> 这些打印Tensor包含在默认图中
    print('查看张量con_2所在的图：', con_2.graph)
    print('查看张量sum_m所在的图：', sum_m.graph)
    print('查看会话sess所在的图：', sess.graph)
    print('查看sess.run(sum_m)：', sess.run(sum_m))


# 4. 重载运算符
p = 1
p = p + a


# 5. run 运行 ops和Tensor --> config可显示硬件信息
# 6. 张量：名字/形状(shape-阶)/类型 -> 张量属性
with tf.Session(graph=g, config=tf.ConfigProto(log_device_placement=True)) as sess_g:
    print('运行张量 >>>', sess_g.run([a, b, p, plt, exp], feed_dict={plt: 4.0, exp: [[1, 2], [1, 2], [3, 4]]}))
    print('张量属性 graph >', a.graph)
    print('张量属性 op >', a.op)
    print('张量属性 name >', a.name)
    print('张量属性 shape >', a.shape)

# 7. 交互式接口


# 8. 静态形状与动态性状
# # 1、静态形状不能跨阶转,(4)-->(2,2)
# # 2、对于本身形状确定的张量，就不能继续设置静态形状
# # 3、动态形状改变，元素个数一定要匹配

con = tf.constant([1, 2, 3, 4])
print('1>', con.get_shape)

plt1 = tf.placeholder(tf.float32, [None, 2])
print('2>', plt1.get_shape)
plt1.set_shape([5, 2])
print('3>', plt1.get_shape)
# plt1.set_shape([6, 1])  # ValueError: Shapes (5, 2) and (6, 1) are not compatible

plt2 = tf.placeholder(tf.float32, [3, 2])
print('4>', plt2.get_shape)
# plt2.set_shape([6, 2])  # ValueError: Shapes (3, 2) and (6, 2) are not compatible
reshape_plt2 = tf.reshape(plt2, [2, 3])
print('5>', reshape_plt2.get_shape)



