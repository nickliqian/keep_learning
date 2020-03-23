# -*-coding: utf-8 -*-
from pyspark.sql import SparkSession, Row, SQLContext
from pyspark.context import SparkContext
from pyspark.context import SparkConf
from graphframes import GraphFrame

# CreateGF
spark = SparkSession.builder.master("local[*]").appName("CreateGF").getOrCreate()
l = [ ("a", "Alice", 34),
      ("b", "Bob", 36),
      ("c", "Charlie", 30),
      ("d", "David", 29),
      ("e", "Esther", 32),
      ("f", "Fanny", 36),
      ("g", "Gabby", 60)]

vertices = spark.createDataFrame(l, ["id", "name", "age"])
print("------CreateGF-------")
vertices.show()






