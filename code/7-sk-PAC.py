from sklearn.decomposition import PCA


# 填补缺失值
def pca():
    # n_components
    pa = PCA(n_components=3)
    data = pa.fit_transform([[2, 8, 4, 5], [6, 3, 0, 8], [5, 4, 9, 1]])
    print(data)


if __name__ == "__main__":
    pca()
