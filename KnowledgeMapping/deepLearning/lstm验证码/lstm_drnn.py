import tensorflow as tf
import numpy as np


def dynamic_rnn(rnn_type='lstm'):
    # 创建输入数据,3代表batch size,6代表输入序列的最大步长(max time),4代表每个序列的维度
    # X = np.random.randn(10, 40, 80)
    X = np.random.randn(3, 6, 4)

    print(X)

    # 第二个输入的实际长度为4
    X[1, 4:] = 0

    print(X)

    # 记录三个输入的实际步长
    X_lengths = [6, 4, 6]

    rnn_hidden_size = 5
    if rnn_type == 'lstm':
        cell = tf.contrib.rnn.BasicLSTMCell(num_units=rnn_hidden_size, state_is_tuple=True)
    else:
        cell = tf.contrib.rnn.GRUCell(num_units=rnn_hidden_size)

    outputs, last_states = tf.nn.dynamic_rnn(
        cell=cell,
        dtype=tf.float64,
        sequence_length=X_lengths,
        inputs=X)

    print(outputs)

    with tf.Session() as session:
        session.run(tf.global_variables_initializer())
        o1, s1 = session.run([outputs, last_states])
        # print(np.shape(o1))
        # print(o1)
        # print(np.shape(s1))
        # print(s1)


if __name__ == '__main__':
    dynamic_rnn(rnn_type='lstm')