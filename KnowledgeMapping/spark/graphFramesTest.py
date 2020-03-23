from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from graphframes import *

conf = SparkConf().setAppName("test")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
nodes = sqlContext.createDataFrame([("a", "Alice", 34), ("b", "Bob", 36), ("c", "Charlie", 30)], ["id", "name", "age"])
rels = sqlContext.createDataFrame([("a", "b", "friends"), ("b", "c", "follow"), ("c", "b", "follow")], ["src", "dst", "relationship"])
graph = GraphFrame(nodes, rels)
graph.inDegrees.show()
graph.vertices.show()
graph.vertices.filter("age > 30").show()
