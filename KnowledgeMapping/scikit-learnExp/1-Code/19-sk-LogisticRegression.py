from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, classification_report
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np


# 逻辑回归
def logistic():

    # 导入数据
    column_names = ['Sample codedir number', 'Clump Thickness', 'Uniformity of Cell Size', 'Uniformity of Cell Shape',
                    'Marginal Adhesion', 'Single Epithelial Cell Size', 'Bare Nuclei', 'Bland Chromatin',
                    'Normal Nucleoli', 'Mitoses', 'Class']
    data = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/"
                       "breast-cancer-wisconsin.data", names=column_names)

    # 处理缺失值
    data = data.replace(to_replace="?", value=np.nan)
    data = data.dropna()

    # 分割数据
    x_train, x_test, y_train, y_test = train_test_split(data[column_names[1:10]], data[column_names[10]], test_size=0.25)

    # 标准化
    std = StandardScaler()
    x_train = std.fit_transform(x_train)
    x_test = std.transform(x_test)

    # estimator
    logic = LogisticRegression()
    logic.fit(x_train, y_train)

    # 预测
    print("准确率：", logic.score(x_test, y_test))
    log_predict = logic.predict(x_test)
    print(log_predict)
    print("精确率和召回率：", classification_report(y_test, log_predict, labels=[2, 4], target_names=["良性", "恶性"]))


if __name__ == "__main__":
    logistic()