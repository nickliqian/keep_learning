from sklearn.preprocessing import StandardScaler


# 预处理-特征处理
# 标准化 公式 异常点影响较小
# API：from scikit-learnExp.preprocessing import StandardScaler
# 样本多的情况下稳定，适合嘈杂的大数据场景
def sdcaler():
    std = StandardScaler()
    data = std.fit_transform([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    new_data = std.inverse_transform(data)
    print(data)
    print(new_data)


if __name__ == "__main__":
    sdcaler()
