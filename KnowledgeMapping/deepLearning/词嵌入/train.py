import sys
import multiprocessing

from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

"""
start train: python trainword2vec.py ./corpus_seg.txt ./model/*
LineSentence(inp)：把word2vec训练模型的磁盘存储文件
转换成所需要的格式,如：[[“sentence1”],[”sentence1”]]
size：是每个词的向量维度
window：是词向量训练时的上下文扫描窗口大小，窗口为5就是考虑前5个词和后5个词
min-count：设置最低频率，默认是5，如果一个词语在文档中出现的次数小于5，那么就会丢弃
方法：
inp:分词后的文本
save(outp1):保存模型
"""

if __name__ == '__main__':

    if len(sys.argv) < 3:
      sys.exit(1)

    # inp表示语料库(分词)，outp：模型
    inp, outp = sys.argv[1:3]

    model = Word2Vec(LineSentence(inp), size=400, window=5, min_count=5, workers=multiprocessing.cpu_count())

    model.save(outp)