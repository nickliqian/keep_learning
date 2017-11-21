from sklearn.feature_extraction.text import CountVectorizer


# 文本特征抽取
def count_vect():
    cv = CountVectorizer()
    data = cv.fit_transform(["life is is short,i like pyt hon", "life is too long,i dislike python"])
    print(cv.get_feature_names())
    print(data)
    print(data.toarray())


if __name__ == "__main__":
    count_vect()