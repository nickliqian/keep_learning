from pyspark import SparkContext
from pyspark.sql import SQLContext
from graphframes import GraphFrame
from graphframes.examples import Graphs

# spark
sc = SparkContext("local", appName="mysqltest")
sc.setCheckpointDir("./ccpoint")
sqlContext = SQLContext(sc)

g = Graphs(sqlContext).friends()

results = g.pageRank(resetProbability=0.15, tol=0.01)

results.vertices.select("id", "pagerank").show()
results.edges.select("src", "dst", "weight").show()

results2 = g.pageRank(resetProbability=0.15, maxIter=10)

results3 = g.pageRank(resetProbability=0.15, maxIter=10, sourceId="a")

results4 = g.parallelPersonalizedPageRank(resetProbability=0.15, sourceIds=["a", "b", "c", "d"], maxIter=10)

