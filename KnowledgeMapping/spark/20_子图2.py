from graphframes.examples import Graphs
from pyspark import SparkContext
from pyspark.sql import SQLContext
from graphframes import GraphFrame


sc = SparkContext("local", appName="mysqltest")
sqlContext = SQLContext(sc)
g = Graphs(sqlContext).friends()  # Get example graph

# Select subgraph based on edges "e" of type "follow"
# pointing from a younger user "a" to an older user "b".
paths = g.find("(a)-[e]->(b)")\
  .filter("e.relationship = 'follow'")\
  .filter("a.age < b.age")
paths.show()
# +----------------+--------------+--------------+
# |               a|             e|             b|
# +----------------+--------------+--------------+
# | [e, Esther, 32]|[e, f, follow]|[f, Fanny, 36]|
# |[c, Charlie, 30]|[c, b, follow]|  [b, Bob, 36]|
# +----------------+--------------+--------------+

# "paths" contains vertex info. Extract the edges.
e2 = paths.select("e.src", "e.dst", "e.relationship")
e2.show()
# +---+---+------------+
# |src|dst|relationship|
# +---+---+------------+
# |  e|  f|      follow|
# |  c|  b|      follow|
# +---+---+------------+

# In Spark 1.5+, the user may simplify this call:
#  val e2 = paths.select("e.*")

# Construct the subgraph
g2 = GraphFrame(g.vertices, e2)
