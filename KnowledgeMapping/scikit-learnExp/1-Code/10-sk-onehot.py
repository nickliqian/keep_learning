from sklearn import preprocessing


def onehot():
    enc = preprocessing.OneHotEncoder(sparse=False)
    data = enc.fit_transform([[0, 0, 3], [1, 1, 0], [0, 2, 1], [1, 0, 2]])
    print(data)


if __name__ == "__main__":
    onehot()