#!/usr/bin/python
# -*- coding: UTF-8 -*-


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
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
    print("---")
    print(test.head(3))

    # =====================逻辑回归===================
    # 分割数据
    x_train, x_test, y_train, y_test = train_test_split(train, y, test_size=0.25, random_state=24)
    # estimator
    logic = LogisticRegression()

    # 通过网格搜索调参
    penaltys = ['l1', 'l2']
    Cs = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 100, 1000]
    class_weight = [{0: 0.5, 1: 0.5}, {0: 0.4, 1: 0.6}, {0: 0.6, 1: 0.4}]
    tol = [1e-4, 1e-6]
    print(">>> 正在进行交叉验证，请等待...")
    tuned_parameters = dict(penalty=penaltys, C=Cs, class_weight=class_weight, tol=tol)
    gc_logic = GridSearchCV(logic, param_grid=tuned_parameters, cv=3)
    gc_logic.fit(x_train, y_train)
    print('准确率：', gc_logic.score(x_test, y_test))
    print('交叉验证集中最好结果：', gc_logic.best_score_)
    print('最好参数：', gc_logic.best_params_)
    print('最好模型：', gc_logic.best_estimator_)
    # print('交叉验证过程：', gc.cv_results_)

    model = gc_logic.best_estimator_
    # 评估
    print("精确率和召回率（逻辑回归）：", classification_report(y_test, model.predict(x_test), labels=[0, 1], target_names=["非高收入", "高收入"]))
    pre_score = model.score(x_test, y_test)
    print("准确率（逻辑回归）：{}".format(pre_score))
    # 输出概率
    predictions = model.predict_proba(x_test)
    # 计算auc
    fpr, tpr, thresholds = metrics.roc_curve(y_test, predictions[:, 1])
    auc_value = metrics.auc(fpr, tpr)
    print("auc值为：{}".format(auc_value))

    # 绘图
    plt.title('LogisticRegression AUC')
    plt.plot(fpr, tpr, 'b', label='AUC_LOGIC = %0.3f' % auc_value)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.ylabel('tpr')
    plt.xlabel('fpr')
    plt.savefig("./LogisticRegression_auc.png")

    # 预测
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
