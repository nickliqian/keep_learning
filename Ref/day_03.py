# @Time    : 2017/9/29 上午9:05
# @File    : day_03.py
# @Software: PyCharm

from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression, SGDRegressor, Ridge, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, classification_report
import pandas as pd
import numpy as np


# def linear():
#     """
#     线性回归(正规方程和梯度下降)分析波士顿房价数据
#     :return: None
#     """
#     # 获取数据集分割
#     lb = load_boston()
#
#     x_train, x_test, y_train, y_test = train_test_split(lb.data, lb.target, test_size=0.25)
#
#     # 标准化处理,对特征值和目标值同样都进行处理
#     std_x = StandardScaler()
#     x_train = std_x.fit_transform(x_train)
#     x_test = std_x.transform(x_test)
#
#     std_y = StandardScaler()
#     y_train = std_y.fit_transform(y_train)
#     y_test = std_y.transform(y_test)
#
#     # 应用线性回归-正规方程回归分析
#     lr = LinearRegression()
#
#     lr.fit(x_train, y_train)
#
#     # print("预测结果：",lr.predict(x_test))
#     #
#     # print("真是结果：", y_test)!
#
#     # 标准化之前的数据大小!!!!!!
#     lr_predict = std_y.inverse_transform(lr.predict(x_test))
#
#     print(lr.coef_)
#
#     print("正规方程的均方误差：",mean_squared_error(std_y.inverse_transform(y_test), lr_predict))
#
#     # SGD梯度下降
#     sgd = SGDRegressor()
#
#     sgd.fit(x_train, y_train)
#
#     print(sgd.coef_)
#
#     sgd_predict = std_y.inverse_transform(sgd.predict(x_test))
#
#     print("梯度下降的均方误差：", mean_squared_error(std_y.inverse_transform(y_test), sgd_predict))
#
#     # 岭回归分析
#     r = Ridge(alpha=3.0)
#
#     r.fit(x_train, y_train)
#
#     print(r.coef_)
#
#     r_predict = std_y.inverse_transform(r.predict(x_test))
#
#     print("岭回归的均方误差：", mean_squared_error(std_y.inverse_transform(y_test), r_predict))
#
#     return None

#
# def logistic():
#     """
#     逻辑回归对肿瘤数据分类
#     :return: None
#     """
#     column_names = ['Sample code number','Clump Thickness', 'Uniformity of Cell Size','Uniformity of Cell Shape','Marginal Adhesion',
#                 'Single Epithelial Cell Size','Bare Nuclei','Bland Chromatin','Normal Nucleoli','Mitoses','Class']
#
#     # 获取数据，处理缺失值
#     data = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data", names=column_names)
#
#
#     data = data.replace(to_replace='?', value=np.nan)
#
#     data = data.dropna()
#
#     # 分割数据，进行标准化
#     x_train, x_test, y_train, y_test = train_test_split(data[column_names[1:10]], data[column_names[10]], test_size=0.25)
#
#
#     std = StandardScaler()
#
#     x_train = std.fit_transform(x_train)
#
#     x_test = std.transform(x_test)
#
#     # estimator
#     logic = LogisticRegression()
#
#     logic.fit(x_train, y_train)
#
#     log_predict = logic.predict(x_test)
#
#     print("准确率：", logic.score(x_test, y_test))
#
#     print("精确率和召回率：", classification_report(y_test, log_predict, labels=[2, 4], target_names=["良性", "恶性"]))
#
#     return None

#
# if __name__ == "__main__":
#     logistic()




# 总结
# 回归
    # 线性回归               模型+ 策略+ 优化
    # 均方误差，优化： 正规方程，梯度下降

    # 过拟合与欠拟合
    # 欠拟合：增加特征数量
    # 过拟合：特征选择，正则化，    x1 x2  x1^3  x1^4       神经网络

    # 带有L2正则化的Ridge回归

    # 逻辑回归  转换成概率值，   sigmoid     召回率

    # 非监督学习：聚类  k-means     轮廓系数















































