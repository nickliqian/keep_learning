from numpy import *
import operator
from os import listdir

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

def classify0(inX, dataSet, labels, k):
    # 获取样本数据数量 dataSet.shape --> (1, 1024) (行, 列)
    dataSetSize = dataSet.shape[0]

    # 矩阵运算，计算测试数据与每个样本数据对应数据项的差值
    # tile(inX, (dataSetSize,1)) 形成一个与目标集行数一致的数组，然后作差相减
    diffMat = tile(inX, (dataSetSize,1)) - dataSet

    # sqDistances 上一步骤结果平方和
    # 平方
    # array([[ 1.  ,  1.21],
    #  [ 1.  ,  1.  ],
    #  [ 0.  ,  0.  ],
    #  [ 0.  ,  0.01]])
    sqDiffMat = diffMat**2
    # 平方和 array([ 2.21,  2.  ,  0.  ,  0.01])
    sqDistances = sqDiffMat.sum(axis=1)

	# 两个点的距离 就是x,y相减后的平方和开方  ((x1-x2)^2 + (y1-y2)^2)**0.5

    # 取平方根，得到距离向量
    # array([ 1.48660687,  1.41421356,  0.        ,  0.1       ])
    distances = sqDistances**0.5

    # 按照距离从低到高排序 排序
    #  array([2, 3, 1, 0], dtype=int64)
    sortedDistIndicies = distances.argsort()  
    print('距离排序之后',sortedDistIndicies)   
    classCount={}
    print('---------')

    # 依次取出最近的样本数据
    for i in range(k):
        # 记录该样本数据所属的类别
        # [2 3 1 0] 这是按位置排序，分别对应到labels的标签去 也就是第一个是那个分类，第二个是哪个分类...
        voteIlabel = labels[sortedDistIndicies[i]]
        # dict.get(key, default=None)
        # 也就是 要从classCount里面找到这个标签对应的值，但是如果没有就赋值为0然后返回0，并且加上1.
        # 相当于计算权重的方式了，如果存在，依然加上1，并且更新这个标签
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
        # print('classCount[voteIlabel]',classCount[voteIlabel])
        # dict[key] = dict.get(key,0) + 1

    # 对类别出现的频次进行排序，从高到低
    # print(classCount.items()) 按元组把内容取出来 dict_items([('B', 2), ('A', 1)]) 按照取出的元组下标1进行排序 倒序/降序
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    print(sortedClassCount)

    # 返回出现频次最高的类别
    return sortedClassCount[0][0]


dataSet, labels = createDataSet()

print(dataSet,'\n---------\n',labels)

classify0([0,0], dataSet, labels, 3)