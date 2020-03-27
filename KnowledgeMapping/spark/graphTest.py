from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext
from graphframes import *

spark = SparkSession.builder.master("local").appName("graphframe.test").getOrCreate()

def create_graph():
    node_fields = [StructField("id", StringType(), True),
                   StructField("latitude", FloatType(), True),
                   StructField("longitude", FloatType(), True),
                   StructField("population", IntegerType(), True)]
    nodes = spark.read.csv("data/transport-nodes.csv",header=True,schema=StructType(node_fields))
    rels = spark.read.csv("data/transport-relationships.csv",header=True)
    reversed_rels = (rels.withColumn("newSrc", rels.dst).withColumn("newDst", rels.src).drop("dst","src").
                     withColumnRenamed("newSrc","src").withColumnRenamed("newDst","dst").select("src", "dst", "relationship", "cost"))
    relationships = rels.union(reversed_rels)
    return GraphFrame(nodes, relationships)

if __name__ == "__main__":
    g = create_graph()
    g.vertices.show()
    g.edges.show(100)