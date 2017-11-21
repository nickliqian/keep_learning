import numpy as np
import pandas as pd
from sklearn.decomposition import PCA


def main():
    # 导入数据
    # 订单与商品
    prior = pd.read_csv('D://A//data//instacart//order_products__prior.csv')
    # 商品购买信息
    product = pd.read_csv('D://A//data//instacart//products.csv')
    # 用户与订单信息
    order = pd.read_csv('D://A//data//instacart//orders.csv')
    # 商品与类别
    aisles = pd.read_csv('D://A//data//instacart//aisles.csv')

    # 合并/联结表格
    pp = pd.merge(prior, product, on=['product_id', 'product_id'])
    po = pd.merge(pp, order, on=['order_id', 'order_id'])
    res = pd.merge(po, aisles, on=['aisle_id', 'aisle_id'])

    # 导入选定列数据
    data = pd.crosstab(res['order_id'], res['aisle_id'])
    # 查看前10列数据
    # print(data.head(10))

    # 降维操作 设置维度为6
    pca = PCA(n_components=6)
    p_data = pca.fit_transform(data)
    print(p_data)
    print(type(p_data))

    np.savetxt('./InstacartAfterPCA', p_data)
    # np.loadtxt(fname)

if __name__ == "__main__":
    main()
