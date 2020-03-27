from pyspark import SparkContext
from pyspark.sql import SQLContext
from graphframes import GraphFrame
from graphframes.examples import Graphs

# spark
sc = SparkContext("local", appName="mysqltest")
sc.setCheckpointDir("./ccpoint")
sqlContext = SQLContext(sc)

# g = Graphs(sqlContext).friends()  # Get example graph

# 读取数据
links_df = sqlContext.read.csv("links.csv")
# 修改列名称
links_df = links_df.withColumnRenamed("_c0", "src")\
                   .withColumnRenamed("_c1", "dst")\
                   .withColumnRenamed("_c2", "relationship")
# 修改列类型
links_df = links_df.withColumn("src", links_df["src"].astype("int"))\
                   .withColumn("dst", links_df["dst"].astype("int"))
links_df.show()

# 读取数据
nodes_df = sqlContext.read.csv("people.csv")
# 修改列名称
nodes_df = nodes_df.withColumnRenamed("_c0", "id")\
                   .withColumnRenamed("_c1", "name")\
                   .withColumnRenamed("_c2", "age")
# 修改列类型
nodes_df = nodes_df.withColumn("id", nodes_df["id"].astype("int"))\
                   .withColumn("age", nodes_df["age"].astype("int"))
nodes_df.show()


g = GraphFrame(nodes_df, links_df)

# g.vertices.show()
# g.edges.show()

result = g.connectedComponents()
result.select("id", "component").orderBy("component").show()

result = g.stronglyConnectedComponents(maxIter=10)
result.select("id", "component").orderBy("component").show()
