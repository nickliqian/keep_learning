from pyspark import SparkContext
from pyspark.sql import SQLContext


sc = SparkContext("local", appName="mysqltest")
sqlContext = SQLContext(sc)
df = sqlContext.read.format("jdbc").options(
    url="jdbc:neo4j://192.168.10.74:7687?password=123456&"
        "useUnicode=true&characterEncoding=utf-8&useJDBCCompliantTimezoneShift=true&"
        "useLegacyDatetimeCode=false&serverTimezone=UTC").load()
df.show(n=5)
sc.stop()
