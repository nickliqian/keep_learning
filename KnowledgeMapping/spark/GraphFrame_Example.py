from pyspark.context import SparkContext, SparkConf
from pyspark.sql import SQLContext
from graphframes import GraphFrame
from graphframes.examples import Graphs


print(SparkConf)
# 连接Spark集群，开启SparkSQL
conf = SparkConf().setMaster("local[*]").setAppName("GF-Example")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

same_g = Graphs(sqlContext).friends()
print(same_g)

