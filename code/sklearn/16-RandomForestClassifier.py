from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
import pandas as pd


# 随机森林算法
def random_forest():

    # 读取数据
    titan = pd.read_csv('D:/A/data/titanic.txt')
    x = titan[["pclass", "age", "sex"]]
    y = titan[["survived"]]

    # 填充缺失值
    x["age"].fillna(x["age"].mean(), inplace=True)
    # print(x)

    # 数据集分割
    x_train, x_test, y_train, y_test = train_test_split(x, y)

    # 转换为字典数据，并进行特征抽取{}
    # 特征抽取 -> 坐标形式 age pclass=1 pclass=2 pclass=3 sex=female sex=male
    dc = DictVectorizer(sparse=False)
    x_train = dc.fit_transform(x_train.to_dict(orient="records"))
    # print(dc.get_feature_names())
    # print(x_train)
    x_test = dc.transform(x_test.to_dict(orient="records"))

    # estimator
    rf = RandomForestClassifier(n_estimators=5)
    rf.fit(x_train, y_train)
    print(rf.score(x_test, y_test))

if __name__ == "__main__":
    random_forest()