from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import jieba


# 分词后的字符串结果
def cut_word():
    # 将内容进行分词,返回的是包含分词结果的迭代器
    content1 = jieba.cut('今天很残酷，明天更残酷，后天很美好，但绝对大部分是死在明天晚上，所以每个人不要放弃今天。')
    content2 = jieba.cut('我们看到的从很远星系来的光是在几百万年之前发出的，这样当我们看到宇宙时，我们是在看它的过去。')
    content3 = jieba.cut('如果只用一种方式了解某样事物，你就不会真正了解它。了解事物真正含义的秘密取决于如何将其与我们所了解的事物相联系。')

    # 取出迭代器数据
    con1, con2, con3 = list(map(list, [content1, content2, content3]))
    # 将列表转换成字符串
    c1, c2, c3 = list(map(' '.join, [con1, con2, con3]))

    # 返回一个元组，包含三句话的分词结果
    return c1, c2, c3


# 输入一个字符串或一个字符串列表,返回按照原先条目分词结果的列表
def cut(strings):
    str_list = []
    if isinstance(strings, (list, tuple)):
        str_list = strings
    elif isinstance(strings, str):
        str_list.append(strings)
    else:
        raise TypeError("Pls give data of list/tuple/str type.")

    result = []
    for s in str_list:
        gen_result = jieba.cut(str(s))
        list_result = list(gen_result)
        string_space = ' '.join(list_result)
        result += string_space
    return result


# 文本特征抽取 TF-IDF 得出词的重要性
def tfidf_vect():
    tf = TfidfVectorizer()
    # 调用分词分割中文文章
    c1, c2, c3 = cut_word()

    print("分词结果：", c1, c2, c3)

    # 实例化
    tf = TfidfVectorizer(stop_words=['一种', '不会'])

    data = tf.fit_transform([c1, c2, c3])

    print(tf.get_feature_names())
    print(data.toarray())

    return None


# 中文特征值化,文本特征抽取
def countvec():
    # 调用分词分割中文文章
    c1, c2, c3 = cut_word()

    print("分词结果：", c1, c2, c3)

    # 实例化
    cv = CountVectorizer()
    data = cv.fit_transform([c1, c2, c3])

    print(cv.get_feature_names())
    print(data.toarray())


if __name__ == "__main__":
    tfidf_vect()
    print('----------------count vect 分词结果--------------------------------')
    countvec()
