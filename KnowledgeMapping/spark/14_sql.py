from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import IntegerType
import pyspark


sc = SparkContext("local", appName="mysqltest")
spark = SQLContext(sc)

a = [('Alice', 1)]
rdd = sc.parallelize(a)
df = spark.createDataFrame(rdd, ['name', 'age'])  # DataFrame[name: string, age: bigint]

rdd.collect()

a = [('Alice', 1)]
output = spark.createDataFrame(a).collect()
output = spark.createDataFrame(a, ['name', 'age']).collect()
print(output)
output = spark.createDataFrame(a, ['name', 'age'])


# [Row(name='Alice', age=1)]

print(type(rdd))
print(type(df))

print(isinstance(df, pyspark.rdd.RDD))
print(isinstance(df, pyspark.sql.dataframe.DataFrame))


spark.createDataFrame(a).show()
# +-----+---+
# |   _1| _2|
# +-----+---+
# |Alice|  1|
# +-----+---+

spark.createDataFrame(a, ['name', 'age']).show()
# +-----+---+
# | name|age|
# +-----+---+
# |Alice|  1|
# +-----+---+



# d = [{'name': 'Alice', 'age': 1}]
# output = spark.createDataFrame(d).collect()
# print(output)
#
# # [Row(age=1, name='Alice')]


# rdd = sc.parallelize(a)
# output = spark.createDataFrame(rdd).collect()
# print(output)
# output = spark.createDataFrame(rdd, ["name", "age"]).collect()
# print(output)
#
# # [Row(_1='Alice', _2=1)]
# # [Row(name='Alice', age=1)]


# from pyspark.sql import Row
# rdd = sc.parallelize(a)
# Person = Row("name", "age")
# person = rdd.map(lambda r: Person(*r))
# output = spark.createDataFrame(person).collect()
# print(output)
#
# # [Row(name='Alice', age=1)]


# from pyspark.sql.types import *
# schema = StructType(
#     [
#         StructField("name", StringType(), True),
#         StructField("age", IntegerType(), True)
#     ]
# )
# output = spark.createDataFrame(rdd, schema).collect()
# print(output)
#
# # [Row(name='Alice', age=1)]


# df = spark.createDataFrame(rdd, ['name', 'age'])  # DataFrame[name: string, age: bigint]
# print(df)
# output = spark.createDataFrame(df.toPandas())  # DataFrame[name: string, age: bigint]
# print(output)
# output = spark.createDataFrame(df.toPandas()).collect()  # [Row(name='Alice', age=1)]
# print(output)
#
# print(df.toPandas())
# print(type(df.toPandas()))

# output = spark.createDataFrame(rdd, "a: string, b: int").collect()
# print(output)  # [Row(a='Alice', b=1)]
# rdd = rdd.map(lambda row: row[1])
# print(rdd)  # PythonRDD[7] at RDD at PythonRDD.scala:53
# output = spark.createDataFrame(rdd, "int").collect()
# print(output)   # [Row(value=1)]
# output = spark.createDataFrame(rdd, "boolean").collect()
# # TypeError: field value: BooleanType can not accept object 1 in type <class 'int'>

# spark.registerDataFrameAsTable(df, "table1")
# spark.dropTempTable("table1")


# print(spark.getConf("spark.sql.shuffle.partitions"))
# print(spark.getConf("spark.sql.shuffle.partitions", u"10"))
# print(spark.setConf("spark.sql.shuffle.partitions", u"50"))
# print(spark.getConf("spark.sql.shuffle.partitions", u"10"))
#
#
# output = spark.range(1, 7, 2).collect()
# print(output)
#
# output = spark.range(3).collect()
# print(output)


# text_sdf = spark.readStream.text(tempfile.mkdtemp())
# text_sdf.isStreaming

# spark.registerFunction("stringLengthString", lambda x: len(x))
# output = spark.sql("SELECT stringLengthString('test')").collect()
# print(output)
#
# spark.registerFunction("stringLengthString", lambda x: len(x), IntegerType())
# output = spark.sql("SELECT stringLengthString('test')").collect()
# print(output)
#
# spark.udf.register("stringLengthInt", lambda x: len(x), IntegerType())
# output = spark.sql("SELECT stringLengthInt('test')").collect()
# print(output)


# spark.registerDataFrameAsTable(df, "table1")
# df2 = spark.table("table1")
# a = sorted(df.collect()) == sorted(df2.collect())
# b = df.collect() == df2.collect()
# print(a, b)
#
# print(df.collect())
# print(sorted(df.collect()))


spark.registerDataFrameAsTable(df, "table1")
print(spark.tableNames())
print(spark.tables())

print("table1" in spark.tableNames())
print("table1" in spark.tableNames("default"))


spark.registerDataFrameAsTable(df, "table1")
df2 = spark.tables()
df2.filter("tableName = 'table1'").first()
print(df2)


