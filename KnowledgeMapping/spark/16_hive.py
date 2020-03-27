from pyspark.sql import HiveContext, SparkSession

_SPARK_HOST = "local"
_APP_NAME = "test"
spark_session = SparkSession.builder.master(_SPARK_HOST).appName(_APP_NAME).getOrCreate()

hive_context = HiveContext(spark_session)

# 生成查询的SQL语句，这个跟hive的查询语句一样，所以也可以加where等条件语句
hive_database = "database1"
hive_table = "test"
hive_read = "select * from  {}.{}".format(hive_database, hive_table)

# 通过SQL语句在hive中查询的数据直接是dataframe的形式
read_df = hive_context.sql(hive_read)

