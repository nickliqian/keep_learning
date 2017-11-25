from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def main():
    # 导入数据集
    data = pd.read_csv("D://A//data//FBlocation//train.csv")

    # 缩小给定数据集，缩小x/y范围，多条件查询
    data = data.query("x > 1.0 & x < 1.25 & y > 2.5 & y < 2.75")

    # 格式化日期字段
    date_value = pd.to_datetime(data['time'], unit='s')

    # 日期变为字典形式，并整理后加入数据集
    time_value = pd.DatetimeIndex(date_value)
    data['year'] = time_value.year
    data['month'] = time_value.month
    data['weekday'] = time_value.weekday
    data['day'] = time_value.day
    data['hour'] = time_value.hour

    # 去掉不需要的字段
    data = data.drop(['time', 'year', 'month'], axis=1)

    # 按不同的 place_id 聚合。也就是把 place_id 相同的列的其他属性聚合到一起
    place_count = data.groupby('place_id').aggregate(np.count_nonzero)

    # 去掉 row_id 次数小于3次的 place_id
    rf = place_count[place_count.row_id > 3].reset_index()

    # 整理数据到原始数据中
    data = data[data['place_id'].isin(rf['place_id'])]

    # 目标值
    y = data['place_id']
    # 特征值
    x = data.drop(['place_id'], axis=1)

    # 数据集分割
    # 特征值训练集/测试集 目标值训练集/测试集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    # 特征值数据集标准化
    std = StandardScaler()
    x_train = std.fit_transform(x_train)
    # 测试集 只用转换就可以了
    x_test = std.transform(x_test)

    # 进入estimator流程
    knn = KNeighborsClassifier(n_neighbors=5)
    # 训练集 打上标签
    knn.fit(x_train, y_train)
    # 使用这个（带有标签的）测试集来计算分数
    score = knn.score(x_test, y_test)

    print(score)


if __name__ == "__main__":
    main()