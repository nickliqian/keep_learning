# encoding=utf-8

import tensorflow as tf

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string("job_name", " ", "指定参数服务器ps还是worker")
tf.app.flags.DEFINE_integer("task_index", 0, "指定服务器工作任务是第几个")

def main(argv):

    # 给定一个全局步数
    global_step = tf.contrib.framework.get_or_create_global_step()

    # 创建集群描述对象
    cluster = tf.train.ClusterSpec({"ps": ["192.168.87.132:2223"], "worker": ["192.168.133.27:2222"]})

    # 创建PS或者worker对应的服务，ps就只用等待，worker去指定的设备工作
    server = tf.train.Server(cluster, job_name=FLAGS.job_name, task_index=FLAGS.task_index)

    # 进行服务器种类判断
    if FLAGS.job_name == "ps":
        server.join()
    else:
        # 构造设备
        worker_device = "/job:worker/task:0/cpu:0"

        # 如果是工作服务器，那就需要进行计算等工作
        with tf.device(tf.train.replica_device_setter(
                worker_device=worker_device,
                cluster=cluster)):

            # 在此设备当中去进行模型的建立计算
            var1 = tf.Variable([[1, 2, 3, 4]], tf.float32)

            var2 = tf.Variable([[2], [2], [2], [2]], tf.float32)

            mat = tf.matmul(var1, var2)

            # 分布式会话运行，指定task0会话去进行初始化操作
            with tf.train.MonitoredTrainingSession(
                master= "grpc://192.168.133.27:2222",
                is_chief= (FLAGS.task_index == 0),
                # checkpoint_dir= "./tmp/", # 这里会出现bug
                hooks=[tf.train.StopAtStepHook(last_step=200)],
                config= tf.ConfigProto(log_device_placement=True)
            ) as mon_sess:
                while not mon_sess.should_stop():
                    print(mon_sess.run(mat))

    return None


if __name__ == "__main__":
    tf.app.run()



# 注意以下代码要在Python2的环境当中运行，安装相关依赖库
# import recsys.algorithm
# recsys.algorithm.VERBOSE = True
#
#
# from recsys.algorithm.factorize import SVD
# from recsys.datamodel.data import Data
# from recsys.evaluation.prediction import RMSE
# import os, sys
#
#
# filename="./tmp/movielens.zip"
#
#
# class RecommendSystem(object):
#     def __init__(self, filename, sep, **format):
#         # 文件信息
#         self.filename = filename
#         self.sep = sep
#         self.format = format
#
#         # 初始化矩阵分解
#         self.svd = SVD()
#
#         # 矩阵信息
#         self.k = 100 #  矩阵的隐因子睡昂
#         self.min_values = 10 #  删除评分少于10人的电影
#         self.post_normalize = False
#
#         # 设置是否加载模型标志
#         self.load_model = False
#
#         # 初始化均方误差
#         self.rmse = RMSE()
#
#     def get_data(self):
#         # 如果模型不存在，则需要加载数据
#         if not os.path.exists(filename):
#             if not os.path.exists(self.filename):
#                 sys.exit()
#             # SVD加载数据
#             # self.svd.load_data(filename=self.filename, sep=self.sep, format=self.format)
#             data = Data()
#
#             data.load(self.filename, sep=self.sep, format=self.format)
#
#             # 分割数据集
#             train, test = data.split_train_test(percent=80)
#
#             return train, test
#
#         else:
#             # 直接加载模型
#             self.svd.load_model(filename)
#
#             # 将是否加载模型设为True
#             self.load_model = True
#
#             return None,None
#
#     def train(self, train):
#         """
#         训练数据
#         :param train: 训练集
#         :return:
#         """
#         if not self.load_model:
#             # svd去获取训练数据集
#             self.svd.set_data(train)
#             # 注意传入的文件名字，不是带后缀名
#             self.svd.compute(k=self.k, min_values=self.min_values, post_normalize=self.post_normalize, savefile=filename[:-4])
#         return None
#
#     def recommend_to_user(self, userid):
#         """
#         推荐结果
#         :param usrid: 用于ID
#         :return: None
#         """
#
#         recommend_list = self.svd.recommend(userid, is_row=False)
#
#         # 打印电影的名称，和预测的评分
#
#         # 构建电影名字的列表
#         movies_list = []
#
#         for line in open("./data/ml-1m/movies.dat", "r"):
#             movies_list.append(' '.join(line.split("::")[1:2]))
#
#         # 依次取出推荐ID
#         for itemid, rating in recommend_list:
#
#             print "给你推荐的电影叫%s, 预测你对它的评分是%f" % (movies_list[itemid], rating)
#
#         return None
#
#     def rs_predict(self, userid, itemid):
#         """
#         得出评分
#         :param userid: 用户ID
#         :param itemid: 物品ID
#         :return: 评分
#         """
#         score = self.svd.predict(itemid, userid)
#
#         return score
#
#     def evaluation(self, test):
#         """
#         均方误差评估模型
#         :param test: 测试数据
#         :return: None
#         """
#         if not self.load_model:
#             # 获取测试数据中的id,rat, <rat, row(itemid), col(userid)>
#             for rating, itemid, userid in test.get():
#                 try:
#                     # rating真是值
#                     score = self.rs_predict(userid, itemid)
#
#                     # 添加所有的测试数据
#                     self.rmse.add(rating, score)
#                 except KeyError:
#                     continue
#
#             error = self.rmse.compute()
#
#         print "均方误差为：%s" % error
#
#         return None
#
#
# if __name__ == "__main__":
#
#     # 实例化类，初始化xinxi
#     rs = RecommendSystem("./data/ml-1m/ratings.dat", sep="::", row=1, col=0, value=2, ids=int)
#
#     # 读取数据训练
#     train, test = rs.get_data()
#
#     # 得出p, q，进行预测
#     rs.train(train)
#
#     rs.recommend_to_user(1)
#
#     rs.rs_predict(1, 1)
#
#     # rs.evaluation(test)