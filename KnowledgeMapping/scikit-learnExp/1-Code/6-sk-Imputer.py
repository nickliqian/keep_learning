from sklearn.preprocessing import Imputer
import numpy as np


# 填补缺失值
def im():
    # missing_values 缺失值形式
    # strategy 填补策略
    # axis 坐标
    imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
    data = imp.fit_transform([[1, 2], [np.nan, 3], [7, 6]])
    print(data)


if __name__ == "__main__":
    im()