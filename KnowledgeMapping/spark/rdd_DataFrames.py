from pyspark.sql import SparkSession, Row, SQLContext
from pyspark import SparkContext, SparkConf
from graphframes import GraphFrame

# rdd to DataFrame
conf = SparkConf().setAppName("test")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

rdd = sc.parallelize([('Alice', 1)])
rdd_node1 = sqlContext.createDataFrame(rdd, ['name', 'age'])
print(rdd_node1.collect())

# list to DataFrame
l = [ ("a", "Alice", 34),
      ("b", "Bob", 36),
      ("c", "Charlie", 30),
      ("d", "David", 29),
      ("e", "Esther", 32),
      ("f", "Fanny", 36),
      ("g", "Gabby", 60)]

vertices = sqlContext.createDataFrame(l, ["id", "name", "age"])
print("------CreateGF-------")
vertices.show()