from sklearn.decomposition import PCA


# 降维 寻找保留最好数据的系数
# 去除嘈杂的特征，尽可能降低原数据的维数（复杂度），损失少量信息
# 削减回归分析或者聚类分析中的少量特征
def pca():
    # n_components 降低到多少维度
    pa = PCA(n_components=3)
    data = pa.fit_transform([[2, 8, 4, 5], [6, 3, 0, 8], [5, 4, 9, 1]])
    print(data)
    print(type(data))


if __name__ == "__main__":
    pca()
