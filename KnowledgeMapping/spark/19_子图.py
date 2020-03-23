from graphframes.examples import Graphs
from pyspark import SparkContext
from pyspark.sql import SQLContext


sc = SparkContext("local", appName="mysqltest")
sqlContext = SQLContext(sc)
g = Graphs(sqlContext).friends()  # Get example graph

# 创建子图
# Select subgraph of users older than 30, and relationships of type "friend".
# Drop isolated vertices (users) which are not contained in any edges (relationships).
g1 = g.filterVertices("age > 30").filterEdges("relationship = 'friend'")
g1.vertices.show()
# +---+------+---+
# | id|  name|age|
# +---+------+---+
# |  a| Alice| 34|
# |  b|   Bob| 36|
# |  e|Esther| 32|
# |  f| Fanny| 36|
# +---+------+---+

g1 = g.filterVertices("age > 30").filterEdges("relationship = 'friend'").dropIsolatedVertices()
g1.vertices.show()
# +---+-----+---+
# | id| name|age|
# +---+-----+---+
# |  b|  Bob| 36|
# |  a|Alice| 34|
# +---+-----+---+
