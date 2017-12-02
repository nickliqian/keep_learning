from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression, SGDRegressor, Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np


# 线性回归（正规方程和梯度下降）分析波士顿房价数据
def linear():
    # 获取数据，分割数据
    lb = load_boston()
    x_train, x_test, y_train, y_test = train_test_split(lb.data, lb.target, test_size=0.25, random_state=24)

    # 标准化处理，对特征值和目标值都进行处理
    std_x = StandardScaler()
    x_train = std_x.fit_transform(x_train)
    x_test = std_x.transform(x_test)
    # 目标值先转为二位数组，并且转置，然后标准化
    y_train = np.array([y_train])
    y_test = np.array([y_test])
    std_y = StandardScaler()
    # 每一行的元素需要个数一致
    y_train = std_y.fit_transform(y_train.T)
    y_test = std_y.transform(y_test.T)

    print('--------正规方程--------')
    # 应用线性回归分析-正规方程
    lr = LinearRegression()
    lr.fit(x_train, y_train)

    # 标准化之前的数据大小!!!!!!
    # lr_predict = std_y.inverse_transform(lr.predict(x_test))

    # print("预测结果：", lr.predict(x_test))
    # print("真实结果：", y_test)
    # print("参数/系数：", lr.coef_)
    print("测试集准确率：", lr.score(x_test, y_test))

    # 如果目标值集合不标准化使用下面这一句
    # print("正规方程的均方误差：", mean_squared_error(y_test, lr.predict(x_test)))

    # 目标值集合标准化需要把标准化之前的真实数据算出来
    # 标准化之前的数据大小!!!!!!
    lr_predict = std_y.inverse_transform(lr.predict(x_test))
    print("正规方程的均方误差：", mean_squared_error(std_y.inverse_transform(y_test), lr_predict))

    print('--------SGD梯度下降--------')
    # SGD梯度下降
    sgd = SGDRegressor()
    sgd.fit(x_train, y_train)
    print("测试集准确率：", sgd.score(x_test, y_test))
    print("参数/系数：", sgd.coef_)
    # 均方误差
    sgd_predict = std_y.inverse_transform(sgd.predict(x_test))
    print("梯度下降的均方误差：", mean_squared_error(std_y.inverse_transform(y_test), sgd_predict))

    print('--------岭回归分析--------')
    # 岭回归分析
    r = Ridge(alpha=3.0)
    r.fit(x_train, y_train)
    print("测试集准确率：", r.score(x_test, y_test))
    print("参数/系数：", r.coef_)
    # 均方误差
    r_predict = std_y.inverse_transform(r.predict(x_test))
    print("岭回归的均方误差：", mean_squared_error(std_y.inverse_transform(y_test), r_predict))


if __name__ == "__main__":
    linear()
