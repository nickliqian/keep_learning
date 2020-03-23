from pyspark import SparkContext
from pyspark.sql import SQLContext
from graphframes.examples import Graphs

# spark
sc = SparkContext("local", appName="mysqltest")
sqlContext = SQLContext(sc)
g = Graphs(sqlContext).friends()  # Get example graph
g.vertices.show()
g.edges.show()


# Search from "Esther" for users of age < 32.
paths = g.bfs("name = 'Esther'", "age < 32")
paths.show()
# +---------------+--------------+--------------+
# |           from|            e0|            to|
# +---------------+--------------+--------------+
# |[e, Esther, 32]|[e, d, friend]|[d, David, 29]|
# +---------------+--------------+--------------+


# Specify edge filters or max path lengths.
paths = g.bfs(toExpr="name = 'Esther'", fromExpr="age < 32", edgeFilter="relationship != 'friend'", maxPathLength=3)
paths.show()
# +---------------+--------------+--------------+--------------+----------------+
# |           from|            e0|            v1|            e1|              to|
# +---------------+--------------+--------------+--------------+----------------+
# |[e, Esther, 32]|[e, f, follow]|[f, Fanny, 36]|[f, c, follow]|[c, Charlie, 30]|
# +---------------+--------------+--------------+--------------+----------------+

