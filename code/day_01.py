# @Time    : 2017/9/27 上午8:50
# @File    : day_01.py
# @Software: PyCharm


# 导入包
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, Imputer
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA
import jieba
import numpy as np

# # 实例化CountVectorizer
#
# vector = CountVectorizer()
#
# # 调用fit_transform输入并转换数据
#
# res = vector.fit_transform(["life is short,i like python","life is too long,i dislike python"])
#
# # 打印结果
# print(vector.get_feature_names())
#
# print(res.toarray())


# def dictvec():
#     """
#     字典的数据抽取
#     :return: None
#     """
#     # 实例化字典API
#     dc = DictVectorizer(sparse=False)
#
#     # 调用fit_transform
#     data = dc.fit_transform([{'city': '北京','temperature':100},{'city': '上海','temperature':60},{'city': '深圳','temperature':30}])
#
#     # 返回类别名称
#     print(dc.get_feature_names())
#
#     print(data)
#
#
#     return None


# def countvec():
#     """
#     文本特征抽取
#     :return: None
#     """
#     # 实例化
#     cv = CountVectorizer()
#
#     data = cv.fit_transform(["life is is short,i like pyt hon", "li fe is too long,i dislike python"])
#
#     print(cv.get_feature_names())
#     print(data.toarray())
#
#     return None

#
# def cutword():
#     """
#     分词后的字符串结果
#     :return: c1,c2,c3
#     """
#     # 将内容进行分词
#     content1 = jieba.cut('今天很残酷，明天更残酷，后天很美好，但绝对大部分是死在明天晚上，所以每个人不要放弃今天。')
#
#     content2 = jieba.cut('我们看到的从很远星系来的光是在几百万年之前发出的，这样当我们看到宇宙时，我们是在看它的过去。')
#
#     content3 = jieba.cut('如果只用一种方式了解某样事物，你就不会真正了解它。了解事物真正含义的秘密取决于如何将其与我们所了解的事物相联系。')
#
#     # 建立列表取出迭代器数据
#     con1 = []
#     con2 = []
#     con3 = []
#
#     for word in content1:
#         con1.append(word)
#
#     for word in content2:
#         con2.append(word)
#
#     for word in content3:
#         con3.append(word)
#
#     # 将列表转换成字符串
#     c1 = ' '.join(con1)
#     c2 = ' '.join(con2)
#     c3 = ' '.join(con3)
#
#     return c1, c2, c3
#
#
#
#
# # 中文特征值化
# def countvec():
#     """
#     文本特征抽取
#     :return: None
#     """
#     # 调用分词分割中文文章
#     c1, c2, c3 = cutword()
#
#     print("分词结果：",c1, c2, c3)
#
#     # 实例化
#     cv = CountVectorizer()
#
#     data = cv.fit_transform([c1, c2, c3])
#
#     print(cv.get_feature_names())
#     print(data.toarray())
#
#     return None
#
#
# # 中文特征值化tf-idf
# def tfidfvec():
#     """
#     文本特征抽取
#     :return: None
#     """
#     # 调用分词分割中文文章
#     c1, c2, c3 = cutword()
#
#     print("分词结果：",c1, c2, c3)
#
#     # 实例化
#     tf = TfidfVectorizer(stop_words=['一种', '不会'])
#
#     data = tf.fit_transform([c1, c2, c3])
#
#     print(tf.get_feature_names())
#     print(data.toarray())
#
#     return None

# def mm():
#     """
#     归一化
#     :return: None
#     """
#     maxmin = MinMaxScaler(feature_range=(2,3))
#
#     data = maxmin.fit_transform([[90,2,10,40], [60,4,15,45], [75,3,13,46]])
#
#     print(data)
#
#     return None


# def standard():
#     """
#     标准化
#     :return: None
#     """
#     std = StandardScaler()
#
#     data = std.fit_transform([[ 1., -1., 3.],[ 2., 4., 2.],[ 4., 6., -1.]])
#
#     print(data)
#
#     return None
#
# def im():
#     """
#     填补缺失值
#     :return: None
#     """
#
#     imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
#
#     data = imp.fit_transform([[1, 2], [np.nan, 3], [7, 6]])
#
#     print(data)
#
#     return None

# def varriance():
#     """
#     填补缺失值
#     :return: None
#     """
#
#     van = VarianceThreshold(threshold=0.0)
#
#     data = van.fit_transform([[0, 2, 0, 3], [0, 1, 4, 3], [0, 1, 1, 3]])
#
#     print(data)
#
#     return None



def pca():
    """
    填补缺失值
    :return: None
    """

    pa = PCA(n_components=3)

    data = pa.fit_transform([[2,8,4,5],[6,3,0,8],[5,4,9,1]])

    print(data)

    return None


if __name__ == "__main__":
    pca()