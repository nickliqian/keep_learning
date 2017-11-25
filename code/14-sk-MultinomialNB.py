from sklearn.datasets import fetch_20newsgroups
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


def mlt():
    # 读取数据和分割数据
    news = fetch_20newsgroups(subset='all')
    print(news.data)
    print(type(news.data))
    print(len(news.data))
    print(news.data[0])

    print(news.target)
    print(type(news.target))
    print(news.target.shape)
    '''
        如果是中文需要提前分好词。
        data: -> x 特征值
        [strA-already cut,
        strB-already cut,
        strC-already cut,
        strD-already cut,] -> list
        target: -> y 目标值
        [typeA typeB typeC typeC ...] -> list
        or
        [typeA,typeB,typeC,typeC ...] -> numpy.ndarray
    '''

    x_train, x_test, y_train, y_test = train_test_split(news.data, news.target, test_size=0.25)
    # 类型不变，仅仅分割
    print('x_train:', type(x_train))
    print('y_train:', type(y_train))
    # 特征抽取
    tf = TfidfVectorizer()
    # 词频率重要性
    x_train = tf.fit_transform(x_train)
    x_test = tf.transform(x_test)

    # esimator
    mnb = MultinomialNB(alpha=1.0)
    mnb.fit(x_train, y_train)

    # 预测数据的类别/结果
    y_predict = mnb.predict(x_test)
    print(y_predict)

    score = mnb.score(x_test, y_test)
    print(score)

if __name__ == "__main__":
    mlt()