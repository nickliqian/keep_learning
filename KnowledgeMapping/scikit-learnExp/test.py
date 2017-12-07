from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression, SGDRegressor, Ridge, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, classification_report
import pandas as pd
import numpy as np


# 获取数据集分割
lb = load_boston()

x_train, x_test, y_train, y_test = train_test_split(lb.data, lb.target, test_size=0.25)

# 标准化处理,对特征值和目标值同样都进行处理
std_x = StandardScaler()
x_train = std_x.fit_transform(x_train)
x_test = std_x.transform(x_test)

std_y = StandardScaler()
y_train = std_y.fit_transform(y_train)
y_test = std_y.transform(y_test)