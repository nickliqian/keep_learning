# 网格搜索
def grid_search(y):
    # 数据集分割
    # 特征值训练集/测试集 目标值训练集/测试集
    x_train, x_test, y_train, y_test = train_test_split(train, y, test_size=0.25, random_state=24)

    # 特征值数据集标准化
    std = StandardScaler()
    x_train = std.fit_transform(x_train)
    # 测试集 只用转换就可以了
    x_test = std.transform(x_test)

    # 进入estimator流程
    logic = LogisticRegression()
    # 训练集 打上标签
    logic.fit(x_train, y_train)
    # 使用这个（带有标签的）测试集来计算分数
    score = logic.score(x_test, y_test)

    print(score)

    # 通过网格搜索进行预测
    # param = {"n_neighbors": [1, 3, 5]}
    gc = GridSearchCV(logic, param_grid=param, cv=2)
    gc.fit(x_train, y_train)

    print('准确率：', gc.score(x_test, y_test))
    print('交叉验证集中最好结果：', gc.best_score_)
    print('最好参数：', gc.best_params_)
    print('最好模型：', gc.best_estimator_)
    print('交叉验证过程：', gc.cv_results_)