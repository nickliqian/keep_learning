import tensorflow as tf


# 创建一个以先进先出的顺序对元素进行排队的队列,并指定上限1000
q = tf.FIFOQueue(1000, tf.float32)

# 定义变量
var = tf.Variable(0.0, tf.float32)

# 定义操作，var = var + 1，返回操作后的结果
encrement_op = tf.assign_add(var, tf.constant(1.0))

# 计算后的变量入队列
en_q = q.enqueue(encrement_op)

# 创建队列管理器：指定队列，添加线程的队列操作列表enqueue_ops，指定线程数量
qr = tf.train.QueueRunner(q, enqueue_ops=[en_q]*1)

# 初始化变量
init_op = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init_op)

    # 线程协调器
    coord = tf.train.Coordinator()
    # 创建线程 子线程执行队列管理器操作
    threads = qr.create_threads(sess, coord=coord, start=True)

    # 取出线程
    for i in range(10):
        print(sess.run(q.dequeue()))

    # 回收线程
    coord.request_stop()
    coord.join(threads)

