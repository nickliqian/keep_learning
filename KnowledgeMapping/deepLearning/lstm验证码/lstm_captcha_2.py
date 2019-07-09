


#python
# 两层LSTM
rnn_cell_layer_1 = tf.contrib.rnn.LSTMCell(num_units=self.hidden_unions, state_is_tuple=True)
rnn_cell_layer_2 = tf.contrib.rnn.LSTMCell(num_units=self.hidden_unions, state_is_tuple=True)
rnn_block = tf.contrib.rnn.MultiRNNCell([rnn_cell_layer_1, rnn_cell_layer_2], state_is_tuple=True)

outputs, _ = tf.nn.dynamic_rnn(rnn_block, self.inputs, self.seq_len, dtype=tf.float32)
outputs_shape = tf.shape(outputs)
batch_size, max_steps = outputs_shape[0], outputs_shape[1]
outputs_reshape = tf.reshape(outputs, [-1, self.hidden_unions])
# 输出经过全连接层做映射
W = tf.Variable(tf.truncated_normal([self.hidden_unions, self.classes], stddev=0.1, dtype=tf.float32),
                        name="W")
b = tf.Variable(tf.constant(0.0, dtype=tf.float32, shape=[self.classes]), name="b")


output = tf.matmul(outputs_reshape, W) + b
output_reshape = tf.reshape(output, [batch_size, -1, self.classes])
output_transpose = tf.transpose(_reshape, perm=[1, 0, 2])
# 使用损失函数 ctc_loss，该函数内部做了soft_max操作，所以全连接输出直接输入，否则编码错误
loss = tf.nn.ctc_loss(labels=self.labels, inputs=output_transpose, sequence_length=self.seq_len)

# 解码过程
decoded, log_prob = tf.nn.ctc_beam_search_decoder(output_transpose, self.seq_len, merge_repeated=False)

