#!/usr/bin/python
# -*- coding: UTF-8 -*-

from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt


# 1. 读取数据，数据分割
boston = load_boston()
X = boston.data
y = boston.target
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=33, test_size=0.25)

# 2.数据标准化处理
ss_X = StandardScaler()
ss_y = StandardScaler()
X_train = ss_X.fit_transform(X_train)
X_test = ss_X.transform(X_test)
y_train = ss_y.fit_transform(y_train.reshape(-1, 1))
y_test = ss_y.transform(y_test.reshape(-1, 1))

# SGDRegressor 默认配置初始化线性回归器 参数估计
sgdr = SGDRegressor()
sgdr.fit(X_train, y_train)
sgdr_y_predict = sgdr.predict(X_test)


# 模型评估 r2_score MSE MAE
print(">>> >>> >>> 性能评估 <<< <<< <<<")
print("sgdr_score:", sgdr.score(X_test, y_test))
print("r2_score:", r2_score(y_test, sgdr_y_predict))
print("均方误差 MSE:", mean_squared_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(sgdr_y_predict)))
print("平均绝对误差 MAE:", mean_absolute_error(ss_y.inverse_transform(y_test), ss_y.inverse_transform(sgdr_y_predict)))
print("系数 coef:", sgdr.coef_)

# 预测房价
print(">>> >>> >>> 房价预测 <<< <<< <<<")
raw = [0.0063200000000000001, 18.0, 2.3100000000000001, 0.0, 0.53800000000000003, 6.5750000000000002,
       65.200000000000003, 4.0899999999999999, 1.0, 296.0, 15.300000000000001, 396.89999999999998, 4.9800000000000004]

raw_data = np.array([raw])
std_data = ss_X.transform(raw_data)
std_result = sgdr.predict(std_data)
new_data = ss_y.inverse_transform(std_result)
print("预测的房价为: {}".format(new_data))


# 使用pyplot画图
plt.scatter(X_test[:, 1], y_test.reshape(1, -1), color='black')
plt.plot(X_test[:, 1], sgdr.predict(X_test).reshape(1, -1)[0], color='blue', linewidth=3)
plt.xticks()
plt.yticks()
plt.show()
