import tensorflow as tf


# 定义 constant var op 等
one = tf.constant(1)
state = tf.Variable(0, name="counter")
new_value = tf.add(state, one)
update = tf.assign(state, new_value)

# 初始化op var
init_op = tf.initialize_all_variables()

with tf.Session() as sess:
    sess.run(init_op)  # 需要先运行初始化操作
    print("init", sess.run(state))  # 打印初始值

    # 运行op:update，更新state，打印state
    for _ in range(3):
        a, b, c = sess.run([state, update, new_value])  # 返回update后的变量结果
        # print(sess.run(state))
        print(a, b, c)