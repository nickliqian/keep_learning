from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler


iris = load_iris()
data = iris.data
target = iris.target

# 分割数据
x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.25, random_state=24)

# 继续标准化
# std = StandardScaler()
# x_train = std.fit_transform(x_train)
# x_test = std.transform(x_test)

# KNN流程
knn = KNeighborsClassifier(n_neighbors=5)
# 计算训练集 特征值/目标值
knn.fit(x_train, y_train)

score = knn.score(x_test, y_test)
# predict预测提供的数据的类标签
pre = knn.predict(x_test)
# 返回测试数据X属于某一类别的概率估计
proba = knn.predict_proba(x_test)
print(pre)
print(score)  # 直接使用自带的数据: 97%
print(proba)