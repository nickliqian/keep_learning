#!/usr/bin/python
# -*- coding: UTF-8 -*-


import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import precision_score, recall_score, accuracy_score


def dumb_columns(column_name):
    global train
    global test
    print("deal {}".format(column_name))
    all_class = list(set(train[column_name]) | set(test[column_name]))
    all_class.sort()
    class_mapping = {label: idx for idx, label in enumerate(all_class)}
    train[column_name] = train[column_name].map(class_mapping).astype(int)
    test[column_name] = test[column_name].map(class_mapping).astype(int)


def logic_standard(y):
    # 逻辑回归+标准化
    # 分割数据
    x_train, x_test, y_train, y_test = train_test_split(train, y, test_size=0.25, random_state=24)
    # 标准化
    std = StandardScaler()
    x_train = std.fit_transform(x_train)
    x_test = std.transform(x_test)
    # estimator
    logic = LogisticRegression()
    logic.fit(x_train, y_train)
    # 预测
    pre_score = logic.score(x_test, y_test)
    print("准确率（逻辑回归+降维+标准化）：{}".format(pre_score))
    print("精确率和召回率：", classification_report(y_test, logic.predict(x_test), labels=[0, 1], target_names=["非高收入", "高收入"]))
    # 输出概率
    predictions = logic.predict_proba(x_test)
    # Compute Receiver operating characteristic (ROC)
    fpr, tpr, thresholds = metrics.roc_curve(y_test, predictions[:, 1])
    auc_value = metrics.auc(fpr, tpr)
    print("auc值为：{}".format(auc_value))
    # plt.title('Receiver Operating Characteristic')
    # plt.plot(false_positive_rate, recall, 'b', label='AUC = %0.2f' % roc_auc)
    # plt.legend(loc='lower right')
    # plt.plot([0, 1], [0, 1], 'r--')
    # plt.xlim([0.0, 1.0])
    # plt.ylim([0.0, 1.0])
    # plt.ylabel('Recall')
    # plt.xlabel('Fall-out')
    # plt.show()


def logic_pca_standard(y, n):
    # 逻辑回归+降维+标准化
    pa = PCA(n_components=n)
    data = pa.fit_transform(train)
    # 分割数据
    x_train, x_test, y_train, y_test = train_test_split(data, y, test_size=0.25, random_state=24)
    # 标准化
    std = StandardScaler()
    print(std)
    x_train = std.fit_transform(x_train)
    x_test = std.transform(x_test)
    # estimator
    logic = LogisticRegression()
    logic.fit(x_train, y_train)
    # 预测
    pre_score = logic.score(x_test, y_test)
    print("准确率（逻辑回归+降维+标准化）：{}".format(pre_score))
    print("精确率和召回率：", classification_report(y_test, logic.predict(x_test), labels=[0, 1], target_names=["非高收入", "高收入"]))
    # 输出概率
    predictions = logic.predict_proba(x_test)
    # Compute Receiver operating characteristic (ROC)
    fpr, tpr, thresholds = metrics.roc_curve(y_test, predictions[:, 1])
    auc_value = metrics.auc(fpr, tpr)
    print("auc值为：{}".format(auc_value))


# 决策树
def desision(y):
    # 数据集分割
    x_train, x_test, y_train, y_test = train_test_split(train, y, test_size=0.25, random_state=24)

    # 转换为字典数据，并进行特征抽取{}
    # 特征抽取 -> 坐标形式 age pclass=1 pclass=2 pclass=3 sex=female sex=male
    dc = DictVectorizer(sparse=False)
    x_train = dc.fit_transform(x_train.to_dict(orient="records"))
    # print(dc.get_feature_names())
    x_test = dc.transform(x_test.to_dict(orient="records"))
    # estimator
    dec = DecisionTreeClassifier(max_depth=4)
    dec.fit(x_train, y_train)
    # 决策树本地保存
    export_graphviz(dec, out_file="./tree.dot",
                    feature_names=['age', 'education', 'education_time', 'gender', 'home_role', 'invest_income',
                                   'invest_loss', 'job', 'marital_status', 'nation', 'province', 'work_days',
                                   'work_type'])
    # 预测
    pre_score = dec.score(x_test, y_test)
    print("准确率（逻辑回归+降维+标准化）：{}".format(pre_score))
    print("精确率和召回率：", classification_report(y_test, dec.predict(x_test), labels=[0, 1], target_names=["非高收入", "高收入"]))
    # 输出概率
    predictions = dec.predict_proba(x_test)
    # Compute Receiver operating characteristic (ROC)
    fpr, tpr, thresholds = metrics.roc_curve(y_test, predictions[:, 1])
    auc_value = metrics.auc(fpr, tpr)
    print("auc值为：{}".format(auc_value))


# 随机森林算法
def random_forest(y):
    # 数据集分割
    x_train, x_test, y_train, y_test = train_test_split(train, y, test_size=0.25, random_state=24)
    # 转换为字典数据，并进行特征抽取
    dc = DictVectorizer(sparse=False)
    x_train = dc.fit_transform(x_train.to_dict(orient="records"))
    # print(dc.get_feature_names())
    # print(x_train)
    x_test = dc.transform(x_test.to_dict(orient="records"))

    # estimator
    rf = RandomForestClassifier(n_estimators=5)
    rf.fit(x_train, y_train)

    # 预测
    pre_score = rf.score(x_test, y_test)
    print("准确率（逻辑回归+降维+标准化）：{}".format(pre_score))
    print("精确率和召回率：", classification_report(y_test, rf.predict(x_test), labels=[0, 1], target_names=["非高收入", "高收入"]))
    # 输出概率
    predictions = rf.predict_proba(x_test)
    # Compute Receiver operating characteristic (ROC)
    fpr, tpr, thresholds = metrics.roc_curve(y_test, predictions[:, 1])
    auc_value = metrics.auc(fpr, tpr)
    print("auc值为：{}".format(auc_value))


def main():
    global train
    global test
    # 查看基本信息
    print("===================前十行数据===================")
    print(train.head(10))
    print("===================基本信息====================")
    print(train.info())
    print("===================基本数据描述====================")
    print(train.describe())

    # 查看是否有缺失数据
    print("===================统计缺失数据-训练集====================")
    print(train.isnull().sum(axis=0))
    print(train.isnull().any())
    print("===================统计缺失数据-测试集====================")
    print(test.isnull().sum(axis=0))
    print(test.isnull().any())

    # 将训练集Y数据存储在y中，并删除训练集Y数据
    y = train['Y']
    del train['Y']

    # 重命名列标题
    origin = ["年龄", "工作天数", "职业类型", "投资收入", "投资损失", "省份", "教育", "家庭角色", "婚姻状况", "教育时间", "民族", "工作情况", "性别"]
    target = ["age", "work_days", "job", "invest_income", "invest_loss", "province", "education", "home_role", "marital_status", "education_time", "nation", "work_type", "gender"]
    rename_dict = dict()
    for i in range(len(origin)):
        rename_dict[origin[i]] = target[i]
    train.rename(columns=rename_dict, inplace=True)
    test.rename(columns=rename_dict, inplace=True)

    # 性别特征转为数字
    train['gender'] = train['gender'].map({'女': 0, '男': 1}).astype(int)
    test['gender'] = test['gender'].map({'女': 0, '男': 1}).astype(int)
    # 其他特征量转为数字
    dumb_columns('job')  # 职业类型
    dumb_columns('province')  # 职业类型
    dumb_columns('education')  # 教育
    dumb_columns('home_role')  # 家庭角色
    dumb_columns('marital_status')  # 婚姻状况
    dumb_columns('nation')  # 民族
    dumb_columns('work_type')  # 工作情况

    print(train.head(10))
    print(train.describe())
    print(test.head(10))
    print(test.describe())

    print("=============================")

    # 逻辑回归
    print("===逻辑回归===")
    logic_standard(y)

    # 逻辑回归 降维
    print("===逻辑回归 降维===")
    logic_pca_standard(y, 11)

    # 决策树
    print("===决策树===")
    desision(y)

    # 随机森林
    print("===随机森林===")
    random_forest(y)

    # 网格搜索
    # grid_search(y)


if __name__ == '__main__':
    # 打开文件
    train = pd.read_csv('./Train.csv')
    test = pd.read_csv('./Test.csv')
    main()
