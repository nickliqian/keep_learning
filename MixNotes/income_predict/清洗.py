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
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import VarianceThreshold


def dumb_columns(column_name):
    global train
    global test
    all_class = list(set(train[column_name]) | set(test[column_name]))
    all_class.sort()
    class_mapping = {label: idx for idx, label in enumerate(all_class)}
    train[column_name] = train[column_name].map(class_mapping).astype(int)
    test[column_name] = test[column_name].map(class_mapping).astype(int)


def main():
    global train
    global test
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

    full_data = [train, test]

    # 性别特征转为数字
    for dataset in full_data:
        dataset['gender'] = dataset['gender'].map({'女': 0, '男': 1}).astype(int)

    # 投资收益
    for dataset in full_data:
        dataset['invest'] = dataset['invest_income'] - dataset['invest_loss']

    for dataset in full_data:
        dataset.loc[dataset['invest'] < 0, 'invest'] = 0
        dataset.loc[dataset['invest'] == 0, 'invest'] = 1
        dataset.loc[(dataset['invest'] > 0) & (dataset['invest'] <= 5000), 'invest'] = 2
        dataset.loc[(dataset['invest'] > 5000) & (dataset['invest'] <= 10000), 'invest'] = 3
        dataset.loc[dataset['invest'] > 10000, 'invest'] = 4

    # 省份
    for dataset in full_data:
        province_list = []
        for province_name in dataset['province']:
            province_list.append(int(province_name.replace("省份", ""))/2)
        dataset['province'] = np.array(province_list)

    # 分类特征转为哑变量
    dumb_columns('job')  # 职业类型
    dumb_columns('education')  # 教育
    dumb_columns('nation')  # 民族
    dumb_columns('home_role')  # 家庭角色
    dumb_columns('marital_status')  # 婚姻状况
    dumb_columns('work_type')  # 工作情况

    # 年龄分类
    for dataset in full_data:
        # Mapping Age
        dataset.loc[dataset['age'] <= 22, 'age'] = 0
        dataset.loc[(dataset['age'] > 22) & (dataset['age'] <= 32), 'age'] = 1
        dataset.loc[(dataset['age'] > 32) & (dataset['age'] <= 48), 'age'] = 2
        dataset.loc[(dataset['age'] > 48) & (dataset['age'] <= 64), 'age'] = 3
        dataset.loc[dataset['age'] > 64, 'age'] = 4

    # 工作天数
    for dataset in full_data:
        dataset['work_days'] = dataset['work_days']/10

    drop_elements = ['invest_income', 'invest_loss', 'education']
    train = train.drop(drop_elements, axis=1)
    test = test.drop(drop_elements, axis=1)

    print(train.head(3))
    print("===")
    print(test.head(3))


    # 逻辑回归===================
    # 分割数据
    x_train, x_test, y_train, y_test = train_test_split(train, y, test_size=0.25, random_state=24)

    # 标准化
    std = StandardScaler()
    x_train = std.fit_transform(x_train)
    x_test = std.transform(x_test)

    # estimator
    # 'class_weight': {"education_time": np.array([0.1,0.2])}
    logic = LogisticRegression()
    logic.fit(x_train, y_train)

    # 预测
    print("精确率和召回率：", classification_report(y_test, logic.predict(x_test), labels=[0, 1], target_names=["非高收入", "高收入"]))
    pre_score = logic.score(x_test, y_test)
    print("准确率（逻辑回归）：{}".format(pre_score))

    # 输出概率
    predictions = logic.predict_proba(x_test)
    # 计算auc
    fpr, tpr, thresholds = metrics.roc_curve(y_test, predictions[:, 1])
    auc_value = metrics.auc(fpr, tpr)
    print("auc值为：{}".format(auc_value))

    # 通过网格搜索调参
    param = {
        'penalty': ['l1', 'l2'],
    }
    gc = GridSearchCV(logic, param_grid=param, cv=3)
    gc.fit(x_train, y_train)
    print('准确率：', gc.score(x_test, y_test))
    print('最好参数：', gc.best_params_)


    # 决策树===========
    # 数据集分割
    x_train, x_test, y_train, y_test = train_test_split(train, y, test_size=0.25, random_state=24)

    # 转换为字典数据，并进行特征抽取{}
    # 特征抽取 -> 坐标形式 age pclass=1 pclass=2 pclass=3 sex=female sex=male
    dc = DictVectorizer(sparse=False)
    x_train = dc.fit_transform(x_train.to_dict(orient="records"))
    features= dc.get_feature_names()
    x_test = dc.transform(x_test.to_dict(orient="records"))
    # estimator
    dec = DecisionTreeClassifier(max_depth=4)
    dec.fit(x_train, y_train)
    # 决策树本地保存
    export_graphviz(dec, out_file="./tree.dot", feature_names=features)
    # 预测
    print("精确率和召回率：", classification_report(y_test, dec.predict(x_test), labels=[0, 1], target_names=["非高收入", "高收入"]))
    pre_score = dec.score(x_test, y_test)
    print("准确率（决策树）：{}".format(pre_score))

    # 输出概率
    predictions = dec.predict_proba(x_test)
    # 计算auc
    fpr, tpr, thresholds = metrics.roc_curve(y_test, predictions[:, 1])
    auc_value = metrics.auc(fpr, tpr)
    print("auc值为：{}".format(auc_value))


    # 随机森林==============
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
    print("精确率和召回率：", classification_report(y_test, rf.predict(x_test), labels=[0, 1], target_names=["非高收入", "高收入"]))
    pre_score = rf.score(x_test, y_test)
    print("准确率（随机森林）：{}".format(pre_score))
    # 输出概率
    predictions = rf.predict_proba(x_test)
    # 计算auc
    fpr, tpr, thresholds = metrics.roc_curve(y_test, predictions[:, 1])
    auc_value = metrics.auc(fpr, tpr)
    print("auc值为：{}".format(auc_value))


if __name__ == '__main__':
    # 打开文件
    train = pd.read_csv('./Train.csv')
    test = pd.read_csv('./Test.csv')
    main()
