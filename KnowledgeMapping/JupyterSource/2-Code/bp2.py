import os
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
        a_y = train_y[i_count * batch_size:(i_count + 1) * batch_size]
        return a_x, a_y


def get_next_batch_test():
    a_x = train_X[0:100]
    a_y = test_y[0:100]
    return a_x, a_y


def mmscaler(data):
    # feature_range 映射到指定范围
    maxmin = MinMaxScaler(feature_range=[0,1])
    data = maxmin.fit_transform(data)
    return data


df = pd.read_csv("123456.csv")
# 分割数据
train, test = train_test_split(df, test_size=.3, random_state=12)
print(train.shape, test.shape)
train_X = train.drop('loan_status', axis=1)
train_X = mmscaler(train_X)  # 归一化

train_y = np.zeros([train_X.shape[0], 2])
for index, value in enumerate(train['loan_status']):
    if value == 0:
        train_y[index, :] = [1, 0]
    elif value == 1:
        train_y[index, :] = [0, 1]
train_y = pd.DataFrame(train_y)

test_X = test.drop('loan_status', axis=1)
test_X = mmscaler(test_X)   # 归一化
test_y = np.zeros([test_X.shape[0], 2])
for index, value in enumerate(test['loan_status']):
    if value == 0:
        test_y[index, :] = [1, 0]
    elif value == 1:
        test_y[index, :] = [0, 1]
test_y = pd.DataFrame(test_y)

num_classes = 2  # 输出大小
input_size = 65  # 输入大小
hidden_units_size = 30  # 隐藏层节点数量
batch_size = 100
training_iterations = 100000  # 1000000

rows_number = train_X.shape[0]
max_batch = int(rows_number / batch_size)   # 301

# 随机初始化神经网络的参数
w1 = tf.Variable(tf.random_normal([input_size, hidden_units_size], stddev=1, seed=1))
w2 = tf.Variable(tf.random_normal([hidden_units_size, num_classes], stddev=1, seed=1))
B1 = tf.Variable(tf.constant(0.1), [hidden_units_size])
B2 = tf.Variable(tf.constant(0.1), [num_classes])

# 在shape的一个维度上使用None可以方便使用不同的batch大小。
x = tf.placeholder(tf.float32, shape=(None, input_size), name='x-input')
y_ = tf.placeholder(tf.float32, shape=(None, num_classes), name='y-input')

# 定义计算图
a = tf.matmul(x, w1) + B1
a_r = tf.nn.relu(a)
y = tf.matmul(a_r, w2) + B2

cross_entropy = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=y_, logits=y))  # 定义交叉熵损失函数
train_step = tf.train.AdadeltaOptimizer(0.001).minimize(cross_entropy)  # 定义优化方法为Ada并最小号cross_entropy

# 计算准确率
origin_y = tf.argmax(y_, axis=1)
predict_y = tf.argmax(y, axis=1)

correct_prediction = tf.equal(origin_y, predict_y)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# 创建一个Session用来执行图
with tf.Session() as sess:
    # 初始化所有的变量
    init_op = tf.global_variables_initializer()
    sess.run(init_op)

    STEPS = 10000

    saver = tf.train.Saver()

    if os.path.exists("model/"):
        try:
            saver.restore(sess, "model/")
        # 判断捕获model文件夹中没有模型文件的错误
        except ValueError:
            print("model文件夹为空，将创建新模型")
    else:
        pass

    for i in range(STEPS):
        # 每次选择batch_size个样本进行训练
        start = (i * batch_size) % rows_number
        end = min(start + batch_size, rows_number)
        # 通过选取的样本训练神经网络并更新参数
        _, total_cross_entropy, accuracy_new = sess.run([train_step, cross_entropy, accuracy], feed_dict={x: train_X[start:end], y_: train_y[start:end]})
        # 每1000次输出损失函数的结果
        if i % 1000 == 0:
            print("Loop: {}, loss: {}, acc_train: {}".format(i, total_cross_entropy, accuracy_new))
        if i % 5000 == 0:
            saver.save(sess, "model/")
        accuracy_test = sess.run(accuracy, feed_dict={x: test_X, y_: test_y})
    print("accuracy_test", accuracy_test)



