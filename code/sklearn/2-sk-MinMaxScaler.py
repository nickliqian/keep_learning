from sklearn.preprocessing import MinMaxScaler, StandardScaler


# 预处理-特征处理
# 归一化 公式 精确小数据场景
# API：sklearn.preprocessing import MinMaxScaler
# 距离公式
def mmscaler():
    # feature_range 映射到指定范围
    maxmin = MinMaxScaler(feature_range=[2,3])
    data = maxmin.fit_transform([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(data)


if __name__ == "__main__":
    mmscaler()
