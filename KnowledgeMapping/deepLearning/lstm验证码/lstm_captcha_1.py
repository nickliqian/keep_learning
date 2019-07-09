# -*- coding:utf-8 -*
import tensorflow as tf
import os
import random
import numpy as np
from PIL import Image


def computational_graph_lstm(x, y, batch_size=64):
    # weights and biases of appropriate shape to accomplish above task
    out_weights = tf.Variable(tf.random_normal([num_units, n_classes]), name='out_weight')
    out_bias = tf.Variable(tf.random_normal([n_classes]), name='out_bias')

    # 构建网络
    lstm_layer = [tf.nn.rnn_cell.LSTMCell(num_units, state_is_tuple=True) for _ in range(layer_num)]  # 创建两层的lstm
    mlstm_cell = tf.nn.rnn_cell.MultiRNNCell(lstm_layer, state_is_tuple=True)  # 将lstm连接在一起

    init_state = mlstm_cell.zero_state(batch_size, tf.float32)  # cell的初始状态

    outputs = list()  # 每个cell的输出
    state = init_state
    with tf.variable_scope('RNN'):
        for timestep in range(time_steps):
            if timestep > 0:
                tf.get_variable_scope().reuse_variables()
            (cell_output, state) = mlstm_cell(x[:, timestep, :], state)  # 这里的state保存了每一层 LSTM 的状态
            outputs.append(cell_output)
    # h_state = outputs[-1] #取最后一个cell输出

    # 计算输出层的第一个元素
    prediction_1 = tf.nn.softmax(tf.matmul(outputs[-4], out_weights) + out_bias)  # 获取最后time-step的输出，使用全连接, 得到第一个验证码输出结果
    # 计算输出层的第二个元素
    prediction_2 = tf.nn.softmax(tf.matmul(outputs[-3], out_weights) + out_bias)  # 输出第二个验证码预测结果
    # 计算输出层的第三个元素
    prediction_3 = tf.nn.softmax(tf.matmul(outputs[-2], out_weights) + out_bias)  # 输出第三个验证码预测结果
    # 计算输出层的第四个元素
    prediction_4 = tf.nn.softmax(tf.matmul(outputs[-1], out_weights) + out_bias)  # 输出第四个验证码预测结果,size:[batch,num_class]
    # 输出连接
    prediction_all = tf.concat([prediction_1, prediction_2, prediction_3, prediction_4],
                               1)  # 4 * [batch, num_class] => [batch, 4 * num_class]
    prediction_all = tf.reshape(prediction_all, [batch_size, captcha_num, n_classes],
                                name='prediction_merge')  # [4, batch, num_class] => [batch, 4, num_class]

    # loss_function
    loss = -tf.reduce_mean(y * tf.log(prediction_all), name='loss')
    # loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction_all,labels=y))
    # optimization
    opt = tf.train.AdamOptimizer(learning_rate=learning_rate, name='opt').minimize(loss)
    # model evaluation
    pre_arg = tf.argmax(prediction_all, 2, name='predict')
    y_arg = tf.argmax(y, 2)
    correct_prediction = tf.equal(pre_arg, y_arg)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name='accuracy')

    return opt, loss, accuracy, pre_arg, y_arg


# 获取bacth_size数据集
def get_batch(data_path=None, is_training=True):
    target_file_list = os.listdir(data_path)  # 读取路径下的所有文件名

    batch = batch_size if is_training else len(target_file_list)  # 确认batch 大小
    batch_x = np.zeros([batch, time_steps, n_input])  # batch 数据
    batch_y = np.zeros([batch, captcha_num, n_classes])  # batch 标签

    for i in range(batch):
        file_name = random.choice(target_file_list) if is_training else target_file_list[i]  # 确认要打开的文件名
        img = Image.open(data_path + '/' + file_name)  # 打开图片
        img = np.array(img)
        if len(img.shape) > 2:  # 彩色图
            img = np.mean(img, -1)  # 转换成灰度图像:(26,80,3) =>(26,80)
            img = img / 255  # 标准化，为了防止训练集的方差过大而导致的收敛过慢问题。
            # img = np.reshape(img,[time_steps,n_input])  #转换格式：(2080,) => (26,80)
        batch_x[i] = img

        label = np.zeros(captcha_num * n_classes)
        for num, char in enumerate(file_name.split('.')[0]):
            index = num * n_classes + char2index(char)
            label[index] = 1
        label = np.reshape(label, [captcha_num, n_classes])
        batch_y[i] = label
    return batch_x, batch_y


# 字符转换成000100
def char2index(c):
    k = ord(c)
    index = -1
    if k >= 48 and k <= 57:  # 数字索引
        index = k - 48
    if k >= 65 and k <= 90:  # 大写字母索引
        index = k - 55
    if k >= 97 and k <= 122:  # 小写字母索引
        index = k - 61
    if index == -1:
        raise ValueError('No Map')
    return index


# 000100转换成字符
def index2char(k):
    # k = chr(num)
    index = -1
    if k >= 0 and k < 10:  # 数字索引
        index = k + 48
    if k >= 10 and k < 36:  # 大写字母索引
        index = k + 55
    if k >= 36 and k < 62:  # 小写字母索引
        index = k + 61
    if index == -1:
        raise ValueError('No Map')
    return chr(index)


# 训练
def train():
    # defining placeholders
    x = tf.placeholder("float", [None, time_steps, n_input], name="x")  # input image placeholder
    y = tf.placeholder("float", [None, captcha_num, n_classes], name="y")  # input label placeholder

    # computational graph
    opt, loss, accuracy, pre_arg, y_arg = computational_graph_lstm(x, y)

    saver = tf.train.Saver()  # 创建训练模型保存类
    init = tf.global_variables_initializer()  # 初始化变量值

    with tf.Session() as sess:  # 创建tensorflow session
        sess.run(init)
        iter = 1
        while iter < iteration:
            batch_x, batch_y = get_batch()
            sess.run(opt, feed_dict={x: batch_x, y: batch_y})  # 只运行优化迭代计算图
            if iter % 100 == 0:
                los, acc, parg, yarg = sess.run([loss, accuracy, pre_arg, y_arg], feed_dict={x: batch_x, y: batch_y})
                print("For iter ", iter)
                print("Accuracy ", acc)
                print("Loss ", los)
                if iter % 1000 == 0:
                    print("predict arg:", parg[0:10])
                    print("yarg :", yarg[0:10])
                print("__________________")
                # if acc > 0.95:
                #     print("training complete, accuracy:", acc)
                #     break
            if iter % 1000 == 0:  # 保存模型
                saver.save(sess, model_path, global_step=iter)
            iter += 1
        # 计算验证集准确率
        valid_x, valid_y = get_batch(data_path=validation_path, is_training=False)
        print("Validation Accuracy:", sess.run(accuracy, feed_dict={x: valid_x, y: valid_y}))


# 获取测试集
def get_test_set():
    target_file_list = os.listdir(test_data_path)  # 获取测试集路径下的所有文件
    print("预测的验证码文件:", len(target_file_list))

    # 判断条件
    flag = len(target_file_list) // batch_size  # 计算待检测验证码个数能被batch size 整除的次数
    batch_len = flag if flag > 0 else 1  # 共有多少个batch
    flag2 = len(target_file_list) % batch_size  # 计算验证码被batch size整除后的取余
    batch_len = batch_len if flag2 == 0 else batch_len + 1  # 若不能整除，则batch数量加1

    print("共生成batch数:", batch_len)
    print("验证码根据batch取余:", flag2)

    batch = np.zeros([batch_len * batch_size, time_steps, n_input])
    for i, file in enumerate(target_file_list):
        batch[i] = open_iamge(file)
    batch = batch.reshape([batch_len, batch_size, time_steps, n_input])
    return batch, target_file_list  # batch_file_name


# 打开图像
def open_iamge(file):
    img = Image.open(test_data_path + '/' + file)  # 打开图片
    img = np.array(img)
    if len(img.shape) > 2:
        img = np.mean(img, -1)  # 转换成灰度图像:(26,80,3) =>(26,80)
        img = img / 255
    return img


# 预测
def predict():
    with tf.Session() as sess:
        saver = tf.train.import_meta_graph(path + "/model/" + "model.ckpt-5000.meta")
        saver.restore(sess, tf.train.latest_checkpoint(path + "/model/"))  # 读取已训练模型

        graph = tf.get_default_graph()  # 获取原始计算图，并读取其中的tensor
        x = graph.get_tensor_by_name("x:0")
        y = graph.get_tensor_by_name("y:0")
        pre_arg = graph.get_tensor_by_name("predict:0")

        test_x, file_list = get_test_set()  # 获取测试集
        predict_result = []
        for i in range(len(test_x)):
            batch_test_x = test_x[i]
            batch_test_y = np.zeros([batch_size, captcha_num, n_classes])  # 创建空的y输入
            test_predict = sess.run([pre_arg], feed_dict={x: batch_test_x, y: batch_test_y})
            # print(test_predict)
            # predict_result.extend(test_predict)

            for line in test_predict[0]:  # 将预测结果转换为字符
                character = ""
                for each in line:
                    character += index2char(each)
                predict_result.append(character)

        predict_result = predict_result[:len(file_list)]  # 预测结果
        write_to_file(predict_result, file_list)  # 保存到文件


# 写入文档
def write_to_file(predict_list, file_list):
    with open(output_path, 'a') as f:
        for i, res in enumerate(predict_list):
            if i == 0:
                f.write("id\tfile\tresult\n")
            f.write(str(i) + "\t" + file_list[i] + "\t" + res + "\n")
    print("预测结果保存在：", output_path)


if __name__ == '__main__':
    path = os.getcwd()  # 项目所在路径

    captcha_path = path + '/train_data'  # 训练集-验证码所在路径
    validation_path = path + '/validation_data'  # 验证集-验证码所在路径
    test_data_path = path + '/test_data'  # 测试集-验证码文件存放路径
    output_path = path + '/result/result.txt'  # 测试结果存放路径
    model_path = path + '/model/model.ckpt'  # 模型存放路径

    # 要识别的字符
    number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z']
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']

    batch_size = 64  # size of batch
    time_steps = 26  # unrolled through 28 time steps #每个time_step是图像的一行像素 height
    n_input = 80  # rows of 28 pixels  #width
    image_channels = 1  # 图像的通道数
    captcha_num = 4  # 验证码中字符个数
    n_classes = len(number) + len(ALPHABET)  # 类别分类

    learning_rate = 0.001  # learning rate for adam
    num_units = 128  # hidden LSTM units
    layer_num = 2  # 网络层数
    iteration = 10000  # 训练迭代次数

    # 训练
    train()

    # 预测
    predict()