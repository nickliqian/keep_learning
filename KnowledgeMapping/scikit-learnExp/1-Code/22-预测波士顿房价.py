#!/usr/bin/python
# -*- coding: UTF-8 -*-

from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


# 从读取的房价数据存储在boston变量中。数据分割。随机采样25%的数据构建测试样本，剩余作为训练样本。random_state是随机数种子
boston = load_boston()
X = boston.data
y = boston.target
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=33, test_size=0.25)

# 分析回归目标值的差异
print("The max target value is", np.max(boston.target))
print("The min target value is", np.min(boston.target))
print("The average target value is", np.mean(boston.target))

# 2.数据标准化处理，分别初始化对特征和目标值的标准化器
ss_X = StandardScaler()
ss_y = StandardScaler()

# 分别对训练和测试数据的特征以及目标值进行标准化处理，fit_transform前要先fit
X_train = ss_X.fit_transform(X_train)
X_test = ss_X.transform(X_test)
y_train = ss_y.fit_transform(y_train.reshape(-1, 1))
y_test = ss_y.transform(y_test.reshape(-1, 1))

# 使用线性回归模型LinearRegression和SGDRegressor分别对波士顿房价数据进行训练及预测
# LinearRegression
lr = LinearRegression()
# 使用训练数据进行参数估计
lr.fit(X_train, y_train)
# 回归预测
lr_y_predict = lr.predict(X_test)

# SGDRegressor 默认配置初始化线性回归器
sgdr = SGDRegressor()
# 使用训练数据进行参数估计
sgdr.fit(X_train, y_train)
# 对测试数据进行回归预测
sgdr_y_predict = sgdr.predict(X_test)

# 模型评估
# 使用LinearRegression模型自带的评估模块，并输出评估结果
print("lr_score:", lr.score(X_test, y_test))
# R-square,MSE,MAE评估LinearRegression回归性能


# r2_score MSE MAE # R-square,MSE,MAE评估LinearRegression回归性能 # 使用LinearRegression模型自带的评估模块，并输出评估结果
print("r2_score:", r2_score(y_test, lr_y_predict))
print("MSE:", mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(lr_y_predict)))
print("MAE:", mean_absolute_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(lr_y_predict)))

print("===========")
# r2_score MSE MAE
print("sgdr_score:", sgdr.score(X_test, y_test))
print("r2_score:", r2_score(y_test, sgdr_y_predict))
print("MSE:", mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(sgdr_y_predict)))
print("MAE:", mean_absolute_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(sgdr_y_predict)))

# 预测房价
r = np.array([[0.0063200000000000001, 18.0, 2.3100000000000001, 0.0, 0.53800000000000003, 6.5750000000000002,
               65.200000000000003, 4.0899999999999999, 1.0, 296.0, 15.300000000000001, 396.89999999999998,
               4.9800000000000004]])

r2 = ss_X.transform(r)
mydata = lr.predict(r2)
new_data = ss_y.inverse_transform(mydata[0])
print(new_data)
