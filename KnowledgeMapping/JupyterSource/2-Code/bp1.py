import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def get_next_batch(i_count):
    while True:
        if i_count >= max_batch - 1:
            i_count = int(i_count % max_batch)
        a_x = test_X[i_count * batch_size:(i_count + 1) * batch_size]
        if a_x.shape[0] != 100:
            i_count += 1
            continue
        a_y = np.zeros([batch_size, num_classes])
        for index, j in enumerate(train_y[i_count * batch_size:(i_count + 1) * batch_size]):
            if j == 0:
                a_y[index, :] = [1, 0]
            elif j == 1:
                a_y[index, :] = [0, 1]
        return a_x, a_y


def get_next_batch_test():
    a_x = train_X
    a_y = np.zeros([train_X.shape[0], num_classes])
    for index, j in enumerate(test_y):
        if j == 0:
            a_y[index, :] = [1, 0]
        else:
            a_y[index, :] = [0, 1]
    return a_x, a_y


def mmscaler(data):
    # feature_range 映射到指定范围
    maxmin = MinMaxScaler(feature_range=[0, 1])
    data = maxmin.fit_transform(data)
    return data


df = pd.read_csv("123456.csv")
# 分割数据
train, test = train_test_split(df, test_size=.3, random_state=12)
print(train.shape, test.shape)
train_X = train.drop('loan_status', axis=1)
train_X = mmscaler(train_X)  # 归一化
train_y = train['loan_status']  # 归一化

test_X = test.drop('loan_status', axis=1)
test_X = mmscaler(test_X)
test_y = test['loan_status']

num_classes = 2  # 输出大小
input_size = 65  # 输入大小
hidden_units_size = 30  # 隐藏层节点数量
batch_size = 100
training_iterations = 3000  # 1000000

rows_number = train_X.shape[0]
max_batch = int(rows_number / batch_size)   # 301

X = tf.placeholder(tf.float32, shape=[None, input_size])
Y = tf.placeholder(tf.float32, shape=[None, num_classes])

W1 = tf.Variable(tf.random_normal([input_size, hidden_units_size], stddev=0.1))
B1 = tf.Variable(tf.constant(0.1), [hidden_units_size])
hidden_opt_1 = tf.matmul(X, W1) + B1  # 输入层到隐藏层正向传播

W2 = tf.Variable(tf.random_normal([hidden_units_size, num_classes], stddev=0.1))
B2 = tf.Variable(tf.constant(0.1), [num_classes])
hidden_opt_2 = tf.nn.relu(hidden_opt_1)  # 激活函数，用于计算节点输出值

final_opt = tf.matmul(hidden_opt_2, W2) + B2  # 隐藏层到输出层正向传播

# 对输出层计算交叉熵损失
loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=Y, logits=final_opt))
# 梯度下降算法，这里使用了反向传播算法用于修改权重，减小损失
opt = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(loss)

# 计算准确率
origin_y = tf.argmax(Y, axis=1)
predict_y = tf.argmax(final_opt, axis=1)

correct_prediction = tf.equal(origin_y, predict_y)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

batch_input_test, batch_labels_test = get_next_batch_test()
with tf.Session() as sess:
    init = tf.global_variables_initializer()
    sess.run(init)
    for i in range(training_iterations):
        # 初始化变量
        batch_input, batch_labels = get_next_batch(i)
        # 训练
        _, cost_ = sess.run([opt, loss], feed_dict={X: batch_input, Y: batch_labels})
        if i % 1000 == 0:
            accuracy_test = sess.run(accuracy, feed_dict={X: batch_input_test, Y: batch_labels_test})
            print("acc_test: {}".format(accuracy_test))
