# coding=utf-8
from numpy import *


def loadDataSet(fileName):
    """
    加载数据集
    :param fileName:str, 数据集文件路径
    :return:list, like array
    """
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float, curLine)
        dataMat.append(list(fltLine))
    return dataMat


# 计算两个向量的距离，用的是欧几里得距离
def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))


# 随机生成初始的质心（ng的课说的初始方式是随机选K个点）
def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k, n)))
    for j in range(n):
        minJ = min(dataSet[:, j])
        rangeJ = float(max(array(dataSet)[:, j]) - minJ)
        centroids[:, j] = minJ + rangeJ * random.rand(k, 1)
    return centroids


def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    """
    聚类算法
    :param dataSet:matrixlib.defmatrix.matrix, 数据集矩阵
    :param k:int, k参数, 聚类的类型数量
    :param distMeas:function, 计算两个向量的距离，用的是欧几里得距离
    :param createCent:function, # 随机生成初始的质心
    :return:
    """
    # shape(dataSet) 矩阵的尺寸为 (100, 3)
    m = shape(dataSet)[0]
    # 生成一个0元素矩阵 (100，2)
    clusterAssment = mat(zeros((m, 2)))  # create mat to assign data points
    # print(clusterAssment)
    # to a centroid, also holds SE of each point
    centroids = createCent(dataSet, k)  # 随机指定聚类类型的中心
    # print(centroids)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        # 为每个数据点分配最接近的质心 for each data point assign it to the closest centroid
        # 遍历数据总列数 100
        for i in range(m):
            # inf表示一个无限大的正数
            minDist = inf
            minIndex = -1
            # 遍历k值 分别计算到几个质心的距离并且记录索引值
            for j in range(k):
                # 计算每个质点和不同质心的距离
                # print("{} -- {}".format(centroids[j, :], dataSet[i, :]))
                distJI = distMeas(centroids[j, :], dataSet[i, :])
                if distJI < minDist:
                    minDist = distJI
                    minIndex = j
            print("--------")
            print("{} {} 【{}】 {}".format(minDist, minIndex, i, clusterAssment[i, 0]))
            # 0矩阵每一行的第一列的数字不等于指定的质心序号
            if clusterAssment[i, 0] != minIndex:
                print("fff")
                clusterChanged = True
            # 0矩阵 赋值为 质心序号，最小距离的平方
            clusterAssment[i, :] = minIndex, minDist ** 2
        # print(centroids)
        for cent in range(k):  # recalculate centroids
            ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A == cent)[0]]  # get all the point in this cluster
            centroids[cent, :] = mean(ptsInClust, axis=0)  # assign centroid to mean
    return centroids, clusterAssment


def show(dataSet, k, centroids, clusterAssment):
    from matplotlib import pyplot as plt
    numSamples, dim = dataSet.shape
    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    for i in range(numSamples):
        markIndex = int(clusterAssment[i, 0])
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])
    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
    for i in range(k):
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize=12)
    # plt.show()


def main():
    # 把列表数据转换为矩阵
    k = 4
    dataMat = mat(loadDataSet('testSet.txt'))
    myCentroids, clustAssing = kMeans(dataMat, k)
    # print(myCentroids)
    show(dataMat, k, myCentroids, clustAssing)


if __name__ == '__main__':
    main()
