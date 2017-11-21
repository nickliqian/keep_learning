# @Time    : 2017/9/28 上午9:04
# @File    : day_02.py
# @Software: PyCharm

from sklearn.datasets import load_iris, fetch_20newsgroups, load_boston
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.ensemble import RandomForestClassifier

# li = load_iris()
# # print(li.data)
# # print(li.target)
# # print(li.feature_names)
# # print(li.target_names)
# # print(li.DESCR)
#
# # 数据集的分割，x_train,x_test,     y_train,y_test
# x_train, x_test, y_train, y_test = train_test_split(li.data, li.target, test_size=0.25, random_state=24)
#
#
# x_train1, x_test1, y_train1, y_test1 = train_test_split(li.data, li.target, test_size=0.25)
#
# # print(x_train==x_train1)
# # print(x_train)
#
# # 新闻数据集
# news = fetch_20newsgroups(subset='all')
#
# # print(news.data)
#
# lb = load_boston()
#
# print(lb.data)
# print(lb.target)

#  预测入住位置
# 1、数据量太大，缩小坐标范围
# 2、对于时间数据，得进行转换
# 3、类别太多，按照指定条件较少类别
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np


# # pd去读取数据
# data = pd.read_csv("./data/FBlocation/train.csv")
# # 缩小给定的数据集，x,y范围，多条件的查询
# data = data.query("x > 1.0 & x < 1.25 & y > 2.5 & y < 2.75")
# # 处理时间日期
# time_value = pd.to_datetime(data['time'], unit='s')
# # 将日期变为字典形式
# time_value = pd.DatetimeIndex(time_value)
# # 将新的特征加入到我们的数据集
# data['year'] = time_value.year
# data['month'] = time_value.month
# data['weekday'] = time_value.weekday
# data['day'] = time_value.day
# data['hour'] = time_value.hour
# # 去除掉没用的特征
# data = data.drop(['time', 'year', 'month'], axis=1)
# place_count = data.groupby('place_id').aggregate(np.count_nonzero)
# rf = place_count[place_count.row_id > 3].reset_index()
# data = data[data['place_id'].isin(rf.place_id)]
#
# # 筛选特征值和目标值
# y = data['place_id']
# x = data.drop(['place_id'], axis=1)
#
# print(x)
#
# # 数据集的分割
# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
#
# # 进行数据的标准化
# std = StandardScaler()
#
# x_train = std.fit_transform(x_train)
# x_test = std.transform(x_test)
#
# # 进入estimator流程
# knn = KNeighborsClassifier()
#
# # estimator本身测试
#
# # knn.fit(x_train, y_train)
# #
# # y_predict = knn.predict(x_test)
#
# # 通过网格搜索进行预测
#
# param = {"n_neighbors":[1, 3, 5]}
#
# gc = GridSearchCV(knn, param_grid=param, cv=2)
#
# gc.fit(x_train, y_train)
#
# print("在测试集上面的准确率：", gc.score(x_test, y_test))
#
# print("在交叉验证中验证集的最好结果：", gc.best_score_)
#
# print("使用的最好的模型：", gc.best_estimator_)
#
# print("交叉验证的过程：", gc.cv_results_)




# def naviebayes():
#     """
#     朴素贝叶斯算法的新闻分类
#     :return: None
#     """
#     # 读取数据进行分割
#     news = fetch_20newsgroups(subset='all')
#
#     x_train, x_test, y_train, y_test = train_test_split(news.data, news.target, test_size=0.25)
#
#     # 特征抽取
#     tf = TfidfVectorizer()
#
#     x_train = tf.fit_transform(x_train)
#     x_test = tf.transform(x_test)
#     # x_test = tf.fit_transform(x_test)
#
#     # estimator
#     mnb = MultinomialNB(alpha=1.0)
#
#     mnb.fit(x_train, y_train)
#
#     y_predict = mnb.predict(x_test)
#
#     print("预测的文章类别是：", y_predict)
#
#     score = mnb.score(x_test, y_test)
#
#     print("准确率：", score)
#
#     return None


def decision():
    """
    决策树对泰坦尼克号生存分析
    :return: None
    """
    # 读取数据，并提取重要的一些特征，目标值
    titan = pd.read_csv("http://biostat.mc.vanderbilt.edu/wiki/pub/Main/DataSets/titanic.txt")

    x = titan[["pclass", "age", "sex"]]

    y = titan[["survived"]]

    # 填充缺失值
    x["age"].fillna(x["age"].mean(), inplace=True)

    # print(x)

    # 进行数据集的分割
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    # 转换字典数据并进行特征抽取{"pclass=1","pclass=2","pclass=3", "age","sex"}
    dc = DictVectorizer(sparse=False)

    x_train = dc.fit_transform(x_train.to_dict(orient="records"))
    x_test = dc.transform(x_test.to_dict(orient="records"))

    # print(dc.get_feature_names())

    # print(x_train, x_test)

    # estimator
    # dec = DecisionTreeClassifier()
    #
    # dec.fit(x_train, y_train)
    #
    # print("准确率：", dec.score(x_test, y_test))
    #
    # export_graphviz(dec, out_file="./tree.dot", feature_names=['年龄', 'pclass=1st', 'pclass=2nd', 'pclass=3rd', '女性', '男性'])

    rf = RandomForestClassifier(n_estimators=5)

    rf.fit(x_train, y_train)

    print(rf.score(x_test, y_test))

    return None


if __name__ == "__main__":
    decision()





