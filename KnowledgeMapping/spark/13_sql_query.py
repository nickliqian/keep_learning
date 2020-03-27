from pyspark import SparkContext
from pyspark.sql import SQLContext


sc = SparkContext("local", appName="mysqltest")
sqlContext = SQLContext(sc)
df = sqlContext.read.format("jdbc").options(
    url="jdbc:mysql://localhost:3306/mydata?user=root&password=mysql&"
        "useUnicode=true&characterEncoding=utf-8&useJDBCCompliantTimezoneShift=true&"
        "useLegacyDatetimeCode=false&serverTimezone=UTC", dbtable="(SELECT * FROM detail_data limit 5) tmp").load()

df.show()
sc.stop()
