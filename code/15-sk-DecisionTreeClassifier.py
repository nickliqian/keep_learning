'''
    决策树对泰坦尼克号生存分析
    1. pd读取数据
    2. 选择有影响的特征，去掉没有影响的特征
    3. 处理缺失值（年龄），可以使用平均值填充
    4. 类别名称可以转为编码
    5. 特征工程，pd转换字典，特征凑趣
    6. 决策树估计器流程
'''

import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz


def desision():

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
    print(dc.get_feature_names())
    print(x_train)
    x_test = dc.transform(x_test.to_dict(orient="records"))

    # estimator
    dec = DecisionTreeClassifier(max_depth=4)
    dec.fit(x_train, y_train)
    print("准确率：", dec.score(x_test, y_test))

    # 决策树本地保存
    export_graphviz(dec, out_file="./tree.dot",
                    feature_names=['age', 'pclass=1st', 'pclass=2nd', 'pclass=3rd', 'sex=female', 'sex=male'])


if __name__ == "__main__":
    desision()