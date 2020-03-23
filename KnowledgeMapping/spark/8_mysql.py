from pyspark import SparkContext
from pyspark.sql import SQLContext


sc = SparkContext("local", appName="mysqltest")
sqlContext = SQLContext(sc)
df = sqlContext.read.format("jdbc").options(
    url="jdbc:mysql://localhost:3306/mydata?user=root&password=mysql&"
        "useUnicode=true&characterEncoding=utf-8&useJDBCCompliantTimezoneShift=true&"
        "useLegacyDatetimeCode=false&serverTimezone=UTC", dbtable="detail_data").load()
df.printSchema()
df.show(n=5)

sc.stop()
