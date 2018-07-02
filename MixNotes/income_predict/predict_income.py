#!/usr/bin/python
# -*- coding: UTF-8 -*-


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics
from sklearn.linear_model.logistic import LogisticRegression


def dumb_columns(column_name):
    global train
    global test
    # 获得训练集和测试集的所有分类并排序，保持每次运行程序时哑变量数字代表的类型一致
    all_class = list(set(train[column_name]) | set(test[column_name]))
    all_class.sort()
    class_mapping = {label: idx for idx, label in enumerate(all_class)}
    # 数字映射到每一个类型
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

    # 查看是否有缺失数据
    print("===================统计缺失数据-训练集====================")
    print(train.isnull().sum(axis=0))
    print(train.isnull().any())
    print("===================统计缺失数据-测试集====================")
    print(test.isnull().sum(axis=0))
    print(test.isnull().any())

    full_data = [train, test]
    # 性别特征转为数字
    for dataset in full_data:
        dataset['gender'] = dataset['gender'].map({'女': 0, '男': 1}).astype(int)

    # 处理投资收益，分为五类
    for dataset in full_data:
        dataset['invest'] = dataset['invest_income'] - dataset['invest_loss']
    for dataset in full_data:
        dataset.loc[dataset['invest'] < 0, 'invest'] = 0
        dataset.loc[dataset['invest'] == 0, 'invest'] = 1
        dataset.loc[(dataset['invest'] > 0) & (dataset['invest'] <= 5000), 'invest'] = 2
        dataset.loc[(dataset['invest'] > 5000) & (dataset['invest'] <= 10000), 'invest'] = 3
        dataset.loc[dataset['invest'] > 10000, 'invest'] = 4

    # 处理省份为数字
    for dataset in full_data:
        province_list = []
        for province_name in dataset['province']:
            province_list.append(int(province_name.replace("省份", ""))/2)
        dataset['province'] = np.array(province_list)

    # 分类特征转为哑变量（数字分类）
    dumb_columns('job')  # 职业类型
    dumb_columns('education')  # 教育
    dumb_columns('nation')  # 民族
    dumb_columns('home_role')  # 家庭角色
    dumb_columns('marital_status')  # 婚姻状况
    dumb_columns('work_type')  # 工作情况

    # 年龄分类-五类
    for dataset in full_data:
        # Mapping Age
        dataset.loc[dataset['age'] <= 22, 'age'] = 0
        dataset.loc[(dataset['age'] > 22) & (dataset['age'] <= 32), 'age'] = 1
        dataset.loc[(dataset['age'] > 32) & (dataset['age'] <= 48), 'age'] = 2
        dataset.loc[(dataset['age'] > 48) & (dataset['age'] <= 64), 'age'] = 3
        dataset.loc[dataset['age'] > 64, 'age'] = 4

    # 工作天数-按比例缩小，防止维度之间差异过大
    for dataset in full_data:
        dataset['work_days'] = dataset['work_days']/10

    # 删除不必要的列
    drop_elements = ['invest_income', 'invest_loss', 'education']
    train = train.drop(drop_elements, axis=1)
    test = test.drop(drop_elements, axis=1)

    # 显示训练集和测试集特征
    print(train.head(3))
    print("===")
    print(test.head(3))

    # 模型列表
    model_list = []

    # =====================逻辑回归===================
    # 分割数据
    x_train, x_test, y_train, y_test = train_test_split(train, y, test_size=0.25, random_state=24)
    # estimator
    logic = LogisticRegression()
    logic.fit(x_train, y_train)
    # 预测
    print("精确率和召回率（逻辑回归）：", classification_report(y_test, logic.predict(x_test), labels=[0, 1], target_names=["非高收入", "高收入"]))
    pre_score = logic.score(x_test, y_test)
    print("准确率（逻辑回归）：{}".format(pre_score))
    # 输出概率
    predictions = logic.predict_proba(x_test)
    # 计算auc
    fpr, tpr, thresholds = metrics.roc_curve(y_test, predictions[:, 1])
    auc_value = metrics.auc(fpr, tpr)
    print("auc值为：{}".format(auc_value))
    model_list.append({"model": logic, "auc": auc_value})
    # 绘图
    plt.title('LogisticRegression AUC')
    plt.plot(fpr, tpr, 'b', label='AUC_LOGIC = %0.3f' % auc_value)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.ylabel('tpr')
    plt.xlabel('fpr')
    # plt.savefig("./LogisticRegression_auc.png")

    # ==============决策树===========
    # 数据集分割
    x_train, x_test, y_train, y_test = train_test_split(train, y, test_size=0.25, random_state=24)
    # 转换为字典数据，并进行特征抽取
    dc = DictVectorizer(sparse=False)
    x_train = dc.fit_transform(x_train.to_dict(orient="records"))
    features = dc.get_feature_names()
    x_test = dc.transform(x_test.to_dict(orient="records"))
    # estimator
    dec = DecisionTreeClassifier(max_depth=4)
    dec.fit(x_train, y_train)
    # 决策树本地保存
    # dot -Tpng -o tree.png tree.dot
    export_graphviz(dec, out_file="./tree.dot", feature_names=features)
    # 预测
    print("精确率和召回率（决策树）：", classification_report(y_test, dec.predict(x_test), labels=[0, 1], target_names=["非高收入", "高收入"]))
    pre_score = dec.score(x_test, y_test)
    print("准确率（决策树）：{}".format(pre_score))
    # 输出概率
    predictions = dec.predict_proba(x_test)
    # 计算auc
    fpr, tpr, thresholds = metrics.roc_curve(y_test, predictions[:, 1])
    auc_value = metrics.auc(fpr, tpr)
    print("auc值为：{}".format(auc_value))
    model_list.append({"model": dec, "auc": auc_value})
    # 绘图
    plt.title('DecisionTreeClassifier AUC')
    plt.plot(fpr, tpr, 'b', label='AUC_DTC = %0.3f' % auc_value)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.ylabel('tpr')
    plt.xlabel('fpr')
    # plt.savefig("./DecisionTreeClassifier_auc.png")

    # =============随机森林==============
    # 数据集分割
    x_train, x_test, y_train, y_test = train_test_split(train, y, test_size=0.25, random_state=24)
    # 转换为字典数据，并进行特征抽取
    dc = DictVectorizer(sparse=False)
    x_train = dc.fit_transform(x_train.to_dict(orient="records"))
    # print(dc.get_feature_names())
    x_test = dc.transform(x_test.to_dict(orient="records"))
    # estimator
    rf = RandomForestClassifier(n_estimators=5)
    rf.fit(x_train, y_train)
    # 预测
    print("精确率和召回率（随机森林）：", classification_report(y_test, rf.predict(x_test), labels=[0, 1], target_names=["非高收入", "高收入"]))
    pre_score = rf.score(x_test, y_test)
    print("准确率（随机森林）：{}".format(pre_score))
    # 输出概率
    predictions = rf.predict_proba(x_test)
    # 计算auc
    fpr, tpr, thresholds = metrics.roc_curve(y_test, predictions[:, 1])
    auc_value = metrics.auc(fpr, tpr)
    print("auc值为：{}".format(auc_value))
    model_list.append({"model": rf, "auc": auc_value})
    # 绘图
    plt.title('RandomForestClassifier AUC')
    plt.plot(fpr, tpr, 'b', label='AUC_RF = %0.3f' % auc_value)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.ylabel('tpr')
    plt.xlabel('fpr')
    plt.savefig("./count_auc.png")

    # 模型对比，选择auc值最大的模型进行预测
    sorted_key_list = sorted(model_list, key=lambda x: x['auc'], reverse=True)
    model = sorted_key_list[0]['model']
    auc_v = sorted_key_list[0]['auc']

    print("选择模型 {}".format(model))
    print("AUC值为 {}".format(auc_v))
    pre_data = model.predict_proba(test)
    # 保存目标值
    test['Y'] = pre_data[:, 0]
    test['Y'].to_csv('Results_1.csv', encoding='utf-8', index=False, header=False)
    # 保存完整版本
    test_origin['Y'] = pre_data[:, 0]
    test_origin.to_csv("./my_results.csv", encoding='utf-8', index=False)


if __name__ == '__main__':
    # 打开文件
    train = pd.read_csv('./Train.csv')
    test = pd.read_csv('./Test.csv')
    test_origin = pd.read_csv('./Test.csv')
    main()
