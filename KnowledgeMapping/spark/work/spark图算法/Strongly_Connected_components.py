from pyspark import SparkContext
from pyspark.sql import SQLContext
from graphframes import GraphFrame
from graphframes.examples import Graphs

# spark
sc = SparkContext("local", appName="mysqltest")
sc.setCheckpointDir("./ccpoint")
sqlContext = SQLContext(sc)

g = Graphs(sqlContext).friends()

result = g.stronglyConnectedComponents(maxIter=10)
result.select("id", "component").orderBy("component").show()
