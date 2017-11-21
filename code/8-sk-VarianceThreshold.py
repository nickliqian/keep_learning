from sklearn.feature_selection import VarianceThreshold


# 特征选择 删除底方差特征
# 重合度高的特征 离平均值很近
def varriance():
    # threshold：临界值
    van = VarianceThreshold(threshold=0.0)
    data = van.fit_transform([[0, 2, 0, 3], [0, 1, 4, 3], [0, 1, 1, 3]])
    print(data)


if __name__ == "__main__":
    varriance()
