import tensorflow as tf


# 同步队列
q = tf.FIFOQueue(3, tf.float32)

en_many = q.enqueue_many(([0.1, 0.2, 0.3],))  # 这里注意

out_q = q.dequeue()

data = out_q + 1

en_q = q.enqueue(data)

with tf.Session() as sess:
    sess.run(en_many)

    for i in range(2):
        sess.run(en_q)

    for i in range(q.size().eval()):
        print(sess.run(q.dequeue()))