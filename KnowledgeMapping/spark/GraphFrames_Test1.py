from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.functions import col, lit, when
from graphframes import GraphFrame

# conf = SparkConf().setMaster("local[*]").setAppName("Create GF")
# sc = SparkContext(conf=conf)

sc = SparkContext("local", appName="mysqltest")
sqlContext = SQLContext(sc)

vertices = sqlContext.createDataFrame([
  ("a", "Alice", 34),
  ("b", "Bob", 36),
  ("c", "Charlie", 30),
  ("d", "David", 29),
  ("e", "Esther", 32),
  ("f", "Fanny", 36),
  ("g", "Gabby", 60)], ["id", "name", "age"])

edges = sqlContext.createDataFrame([
  ("a", "b", "friend"),
  ("b", "c", "follow"),
  ("c", "b", "follow"),
  ("f", "c", "follow"),
  ("e", "f", "follow"),
  ("e", "d", "friend"),
  ("d", "a", "friend"),
  ("a", "e", "friend")
], ["src", "dst", "relationship"])

g = GraphFrame(vertices, edges)
print("\n")
g.vertices.show()
print("\n")
g.edges.show()

# Simple Queries, node degree
g.inDegrees.sort("id").show()
g.outDegrees.sort("id").show()
g.degrees.sort("id").show()

# vertices DataFrame in the graph
agelist = g.vertices.groupBy().min("age").show()
youngest = g.vertices.filter("age < 30").show()
numFollows = g.edges.filter("relationship = 'follow'").count()
print(numFollows)

# find the pairs of vertices with edges in both directions between them
motif = g.find("(a)-[e]->(b); (b)-[e2]->(a)")
motif.filter("b.age > 30 or a.age >30").show()

# find chains of 4 vertices
# chain4 = g.find("(a)-[ab]->(b); (b)-[bc]->(c); (c)-[cd]->(d)")
# chain4.show()
# def cumFriends(cnt, edge):
#     relationship = col(edge)["relationship"]
#     return when(relationship == "friend", cnt + 1).otherwise(cnt)
#
# edges1 = ["ab", "bc", "cd"]
# numFriends = reduce(cumFriends, edges, lit(0))
#
# chainWith2Friends2 = chain4.withColumn("num_friends", numFriends).where(numFriends >=2).show()

# subgraphs
# - filtering on edges and vertices
# - only includes people who are more than 30 years old and hava friends who are more than 30 years old
g2 = g.filterEdges("relationship = 'friend'").filterVertices("age > 30").dropIsolatedVertices()
g2.vertices.sort("id").show()

# standard graph algorithms
# 1. breadth-first search BFS
#    search from "Esther" for users of age < 32

paths = g.bfs("name = 'Esther'", "age < 32")


