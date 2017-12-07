from sklearn.datasets import load_iris, fetch_20newsgroups, load_boston
from sklearn.model_selection import train_test_split


# 导入 iris 数据集
iris_data = load_iris()
# print(iris_data.data)  # 特征值
# print(iris_data.feature_names)  # 特征名称 ['sepal length (cm)','sepal width (cm)','petal length (cm)','petal width (cm)']
# print(iris_data.target)  # 目标值
# print(iris_data.target_names)  # 目标名称 ['setosa' 'versicolor' 'virginica']
# print(iris_data.DESCR)

# 数据集的分割: 训练集/测试集 特征值/目标值
# test_size 测试集大小 random_state 随机数种子（如果不设置，每次分割的顺序都不一样）
x_train, x_test, y_train, y_test = train_test_split(iris_data.data, iris_data.target, test_size=0.25, random_state=24)


# 导入新闻数据集
news = fetch_20newsgroups(subset='all')
print(news.data)


# 导入波士顿房价
lb = load_boston()
print(lb.data)
print(lb.target)

