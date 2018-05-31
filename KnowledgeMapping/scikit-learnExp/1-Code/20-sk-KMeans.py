from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# 订单与商品
prior = pd.read_csv('/home/nick/Desktop/kaggleData/order_products__prior.csv')
# 商品购买信息
product = pd.read_csv('/home/nick/Desktop/kaggleData/products.csv')
# 用户与订单信息
order = pd.read_csv('/home/nick/Desktop/kaggleData/orders.csv')
# 商品与类别
aisles = pd.read_csv('/home/nick/Desktop/kaggleData/aisles.csv')
# 合并数据
pp = pd.merge(prior, product, on=['product_id', 'product_id'])
po = pd.merge(pp, order, on=['order_id', 'order_id'])
res = pd.merge(po, aisles, on=['aisle_id', 'aisle_id'])
# 删除冗余数据
data = pd.crosstab(res['order_id'], res['aisle_id'])
# PCA算法降维
pca = PCA(n_components=6)
pca_samples = pca.fit_transform(data)


# kmean算法
km = KMeans(n_clusters=4)
mean = km.fit(pca_samples)
predict = mean.predict(pca_samples)
plt.figure(figsize=(8,8))
colored = ["red", "orange", "green", "blue"]
col = [colored[k] for k in predict]
plt.scatter(pca_samples[:, 0], pca_samples[:, 4], color=col)
plt.xlabel("降维特征1")
plt.ylabel("降维特征2")
plt.show()

# 轮廓系数
print("轮廓系数", silhouette_score(pca_samples, predict))
