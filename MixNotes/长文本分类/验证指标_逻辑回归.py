import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer


# 读取数据集
df_train = pd.read_csv("./train_set.csv")
df_test = pd.read_csv("./test_set.csv")

# drop不相关的列，训练集保留 word_seg 和 class，测试集保留 word_seg
# inplace：基于源 DataFrame 调整数据
df_train.drop(columns=['article', 'id'], inplace=True)
df_test.drop(columns=['article'], inplace=True)

# 特征工程, 转换为词条矩阵（数字向量）
# CountVectorizer 考虑每种词汇在该训练文本中出现的频率和次数
# CountVectorizer ngram_range: 最大向量包含的词数和最小向量包含的词数
#                 min_df：      最少在n（这里是3）个文档中出现过的词才保留
#                 max_df：      忽略在90%以上的文本中出现过的词
#                 max_features: 选择词频最高的指定个数的特征转为向量
#                 stop_words:   停用词，这里暂不考虑
# TfidfVectorizer 考量词汇在当前训练文本中出现的频率和词汇的其它训练文本出现次数的倒数
vectorizer = CountVectorizer(ngram_range=(1, 2), min_df=3, max_df=0.9, max_features=100000, stop_words=None)

# fit 统一的转换的规则  transform 转为特征向量
vectorizer.fit(df_train['word_seg'])
x_train = vectorizer.transform(df_train['word_seg'])
x_test = vectorizer.transform(df_test['word_seg'])
y_train = df_train['class'] - 1

# 逻辑回归
# C：正则化系数λ的倒数，像SVM一样，越小的数值表示越强的正则化。
# dual：对偶或原始方法，对偶方法只用在求解线性多核(liblinear)的L2惩罚项上。当样本数量>样本特征的时候，dual通常设置为False。
lg = LogisticRegression(C=4, dual=True)
# 训练
lg.fit(x_train, y_train)

# 预测
y_test = lg.predict(x_test)

# 转换为指定格式
df_test["class"] = y_test.tolist()
df_test["class"] = df_test["class"] + 1
df_result = df_test.loc[:, ["id", "class"]]
df_result.to_csv("./result/cvect_lr_result.csv", index=False)