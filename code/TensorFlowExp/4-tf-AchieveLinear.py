import tensorflow as tf
import os


def achieve_linear():

    with tf.variable_scope("data"):
        # 1. 准备真实的数据
        x_data = tf.Variable(tf.random_normal([100, 1], mean=0.0, stddev=1.0), name="x_data")

        # 得出真实的目标值 -> 实际应用场景如何得到？
        y_true = tf.matmul(x_data, tf.constant([[0.7]])) + 0.8
        print("目标模型： y = 0.7x + 0.8")

    with tf.variable_scope("model"):
        # 2. 建立模型，随机指定一些权重和偏置值，得出预测结果
        # 权重
        weights = tf.Variable(tf.random_normal([1, 1], mean=1.0, stddev=1.0), name="weight")
        # 偏置值
        bias = tf.Variable(0.0)
        # 预测得到的目标值
        y_predict = tf.matmul(x_data, weights) + bias

    with tf.variable_scope("train"):
        # 3. 训练，梯度下降API -> 减少损失：学习率，均方误差
        loss = tf.reduce_mean(tf.square(y_true - y_predict))
        # 训练操作，设置学习率和损失公式
        train_op = tf.train.GradientDescentOptimizer(0.2).minimize(loss)

    # 收集变量
    tf.summary.scalar("loss", loss)
    tf.summary.scalar("bias", bias)

    # 收集权重
    tf.summary.histogram("weights", weights)

    # 初始化变量
    init_op = tf.global_variables_initializer()

    # 合并变量
    merged = tf.summary.merge_all()

    # 创建一个保存实例
    save = tf.train.Saver()

    # 开启会话
    with tf.Session() as sess:

        # 初始化变量op
        sess.run(init_op)

        # 添加事件文件
        filewriter = tf.summary.FileWriter('/home/nick/Desktop/gitProject/ralph_doc_to_chinese/code/TensorFlowExp/board'
                                           , graph=sess.graph)

        # 判断是否有模型文件，如果有就直接加载模型
        if os.path.exists("/home/nick/Desktop/gitProject/ralph_doc_to_chinese/code/TensorFlowExp/modelsave/checkpoint"):
            save.restore(sess, "/home/nick/Desktop/gitProject/ralph_doc_to_chinese/code/TensorFlowExp/modelsave/")

        # 打印初始模型
        a = weights.eval()
        b = bias.eval()
        print("初始模型： y = %fx + %f " % (weights.eval(), bias.eval()))
        print("初始参数： 权重=%f 偏置值=%f " % (weights.eval(), bias.eval()))

        for i in range(20):

            # 运行训练op
            sess.run(train_op)
            summ = sess.run(merged)
            filewriter.add_summary(summ, i)
            print("第%d次训练参数： 权重=%f 偏置值=%f" % (i+1, weights.eval(), bias.eval()))

        print('-------------Report----------------------------')
        print("目标模型： y = 0.7x + 0.8")
        print("初始模型： 权重=%f 偏置值=%f" % (a, b))
        print("训练20次后模型： 权重=%f 偏置值=%f" % (weights.eval(), bias.eval()))
        print('--------------End------------------------------')

        # 保存模型
        save.save(sess, "/home/nick/Desktop/gitProject/ralph_doc_to_chinese/code/TensorFlowExp/modelsave/")


if __name__ == "__main__":
    achieve_linear()
