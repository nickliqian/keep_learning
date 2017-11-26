from sklearn.datasets import fetch_20newsgroups
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


def mlt():
    # 读取数据和分割数据
    news = fetch_20newsgroups(subset='all')
    # print(news.data)
    # print(type(news.data))
    # print(len(news.data))
    # print(news.data[0])
    #
    # print(news.target)
    # print(type(news.target))
    # print(news.target.shape)
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

    # 特征抽取
    tf = TfidfVectorizer()
    # 词频率重要性

    # 特征转换
    x_train = tf.fit_transform(x_train)
    x_test = tf.transform(x_test)
    with open('D:/A/data/20newsbydate/20news-bydate-test/alt.atheism/53068') as f:
        one_article = str(f.read())
    one_article_list = []
    one_article_list.append(one_article)
    one_article_list_tran = tf.transform(one_article_list)

    # esimator
    mnb = MultinomialNB(alpha=1.0)
    mnb.fit(x_train, y_train)

    # 预测数据的类别/结果
    y_predict = mnb.predict(x_test)
    print(type(x_test))
    print('预测结果是：', y_predict)
    one_article_type = mnb.predict(one_article_list_tran)
    print('单个预测结果：', one_article_type)

    score = mnb.score(x_test, y_test)
    print('准确率是：', score)

if __name__ == "__main__":
    mlt()