
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer


# In[2]:


# 读取数据集
df_train = pd.read_csv("./train_set.csv")
df_test = pd.read_csv("./test_set.csv")


# In[3]:


from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(df_train['word_seg'], df_train['class'], test_size=0.25, random_state=24)


# In[5]:


# 特征工程, 转换为词条矩阵（数字向量）
vectorizer = CountVectorizer(ngram_range=(1, 2), min_df=3, max_df=0.9, max_features=100000, stop_words=None)


# In[6]:


# fit 统一的转换的规则  transform 转为特征向量
vectorizer.fit(x_train)
x_train = vectorizer.transform(x_train)
x_test = vectorizer.transform(x_test)
y_train = y_train - 1


# In[7]:


# 逻辑回归训练
lg = LogisticRegression(C=4, dual=True)
lg.fit(x_train, y_train)
print("训练完成")


# In[10]:


import matplotlib.pyplot as plt
from sklearn import metrics
# 预测
# 输出概率
predictions = lg.predict_proba(x_test)
# 计算auc
fpr, tpr, thresholds = metrics.roc_curve(y_test, predictions[:, 1])
auc_value = metrics.auc(fpr, tpr)
print("auc值为：{}".format(auc_value))
model_list.append({"model": logic, "auc": auc_value})
# 绘图
plt.title('LogisticRegression AUC')
plt.plot(fpr, tpr, 'r', label='AUC_LOGIC = %0.3f' % auc_value)
plt.legend(loc='lower right')
plt.plot([0, 1], [0, 1], 'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.ylabel('tpr')
plt.xlabel('fpr')


# In[ ]:


# 预测
y_test = lg.predict(x_test)


# In[ ]:


# 转换为指定格式
df_test["class"] = y_test.tolist()
df_test["class"] = df_test["class"] + 1
df_result = df_test.loc[:, ["id", "class"]]
df_result.to_csv("./result/cvect_lr_result.csv", index=False)

