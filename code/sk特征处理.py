from sklearn.preprocessing import MinMaxScaler, StandardScaler


# 归一化 公式 精确小数据场景
# API：sklearn.preprocessing import MinMaxScaler
# 距离公式
def mmscaler():
    # feature_range 映射到指定范围
    maxmin = MinMaxScaler(feature_range=[2,3])
    data = maxmin.fit_transform([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(data)


# 标准化 公式 异常点影响较小
# API：from sklearn.preprocessing import StandardScaler
# 样本多的情况下稳定，适合嘈杂的大数据场景
def sdcaler():
    std = StandardScaler()
    data = std.fit_transform([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(data)


if __name__ == "__main__":
    sdcaler()
