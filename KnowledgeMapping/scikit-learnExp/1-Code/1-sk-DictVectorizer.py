from sklearn.feature_extraction import DictVectorizer


# 预处理-特征抽取
def dict_vect():

    # 实例化
    # sparse是一种数据类型，按照布尔值坐标区分了文本信息，默认情况下sparse=True
    dc = DictVectorizer(sparse=True)
    # 以下可以看到onehot编码
    # dc = DictVectorizer(sparse=False)
    raw_data = [
        {"city": "北京", "temperature": "100"},
        {"city": "上海", "temperature": "60"},
        {"city": "广州", "temperature": "30"},
    ]

    data = dc.fit_transform(raw_data)
    # 类别名称
    print(dc.get_feature_names())
    # 抽取后的数据
    print(data)


if __name__ == "__main__":
    dict_vect()
