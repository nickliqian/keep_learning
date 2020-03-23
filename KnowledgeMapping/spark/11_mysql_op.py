from pyspark import SparkContext
from pyspark.sql import SQLContext
import pyspark.sql.functions as F


sc = SparkContext("local", appName="mysqltest")
sqlContext = SQLContext(sc)
df = sqlContext.read.format("jdbc").options(
    url="jdbc:mysql://localhost:3306/mydata?user=root&password=mysql&"
        "useUnicode=true&characterEncoding=utf-8&useJDBCCompliantTimezoneShift=true&"
        "useLegacyDatetimeCode=false&serverTimezone=UTC", dbtable="detail_data").load()

df.printSchema()
# root
#  |-- id: integer (nullable = true)
#  |-- 省份: string (nullable = true)

df.show(n=5)
# +----+------+------+------+------+
# |  id|  省份|  城市|  区县|  区域|
# +----+------+------+------+------
# |2557|广东省|深圳市|罗湖区|春风路

print(df.count())
# 47104

df_g1 = df.groupby("区县").count()
df_g1.show()
# +--------+-----+
# |    区县|count|
# +--------+-----+
# |  龙华区| 4217|


print(df.columns)
# ['id', '省份', '城市', '区县', '区域', '小区', '源地址',
print(df.dtypes)
# [('id', 'int'), ('省份', 'string'), ('城市', 'string'),

df.select('城市', '区县', '区域', '小区').show()
# +------+------+------+--------------+
# |  城市|  区县|  区域|          小区|
# +------+------+------+--------------+
# |深圳市|罗湖区|春风路|      凯悦华庭|
# |深圳市|罗湖区|春风路|      置地逸轩|

df.select(df.id.alias('id_value'), '小区').show()
# +--------+--------------+
# |id_value|          小区|
# +--------+--------------+
# |    2557|      凯悦华庭|
# |    2558|      置地逸轩|

df.select(df["城市"].alias('city'), '小区').show()
# +------+--------------+
# |  city|          小区|
# +------+--------------+
# |深圳市|      凯悦华庭|
# |深圳市|      置地逸轩|

df.select('城市', '区县', '区域', '小区').filter(df["小区"] == '凯悦华庭').show()
# +------+------+------+--------+
# |  城市|  区县|  区域|    小区|
# +------+------+------+--------+
# |深圳市|罗湖区|春风路|凯悦华庭|

df.select('城市', '区县', '区域', '小区').filter((df["城市"] == '深圳市') & (df["区县"] == '南山区')).show()
# +------+------+------+----------------+
# |  城市|  区县|  区域|            小区|
# +------+------+------+----------------+
# |深圳市|南山区|白石洲|中海深圳湾畔花园|
# |深圳市|南山区|白石洲|    侨城豪苑二期|
# ...

df.select(df["城市"] + 1, '城市', '小区').show()
# +----------+------+--------------+
# |(城市 + 1)|  城市|          小区|
# +----------+------+--------------+
# |      null|深圳市|      凯悦华庭|

df.select(F.lit("test").alias('城市plus'), '城市', '小区').show()
# +--------+------+--------------+
# |城市plus|  城市|          小区|
# +--------+------+--------------+
# |    test|深圳市|      凯悦华庭|


# 取出一行
df2 = df.limit(1)
print(df2)

# 增加行
print(df.count())  # 47104
print(df.unionAll(df2).count())  # 47105

# 删除重复记录
print(df.drop_duplicates().count())  # 47104

# 删除列
print(df.drop('id').columns)
# ['省份', '城市', '区县', '区域', '小区', '源地址',...

# 删除指定字段中存在缺失的记录
print("删除存在缺失的记录")
print(df.dropna().count())
print("删除指定字段中存在缺失的记录")
print(df.dropna(subset=['省份', '城市']).count())

# 填充缺失值
print(df.fillna({'省份': "广东省", '城市': '深圳市'}))

# 分组计算
df.groupby('区县').agg(F.max(df['总价'])).show()
# +--------+----------+
# |    区县| max(总价)|
# +--------+----------+
# |  龙华区|5200.00000|
# |  福田区|8300.00000|
# |  罗湖区|7000.00000|
# |  坪山区|1588.00000|
# |  南山区|9800.00000|
# |  龙岗区|4000.00000|
# |  盐田区|5500.00000|
# |  光明区|5200.00000|
# |大鹏新区|3500.00000|
# |  宝安区|8800.00000|
# +--------+----------+

# 函数计算
df.select(F.max(df["总价"])).show()  # 最大值
df.select(F.min(df["总价"])).show()  # 最小值
df.select(F.avg(df["总价"])).show()  # 平均值
df.select(F.countDistinct(df["总价"])).show()  # 去重后再统计
df.select(F.count(df["总价"])).show()  # 去掉缺失值会再统计
# +----------+
# | max(总价)|
# +----------+
# |9800.00000|
# +----------+
#
# +---------+
# |min(总价)|
# +---------+
# |  1.10000|
# +---------+
#
# +-------------+
# |    avg(总价)|
# +-------------+
# |577.736916000|
# +-------------+
#
#  |count(DISTINCT 总价)|
# +--------------------+
# |                1219|
# +--------------------+
#
# +-----------+
# |count(总价)|
# +-----------+
# |      47104|
# +-----------+

# 'lit': 'Creates a :class:`Column` of literal value.',
# 'col': 'Returns a :class:`Column` based on the given column name.',
# 'column': 'Returns a :class:`Column` based on the given column name.',
# 'asc': 'Returns a sort expression based on the ascending order of the given column name.',
# 'desc': 'Returns a sort expression based on the descending order of the given column name.',
#
# 'upper': 'Converts a string expression to upper case.',
# 'lower': 'Converts a string expression to upper case.',
# 'sqrt': 'Computes the square root of the specified float value.',
# 'abs': 'Computes the absolutle value.',
#
# 'max': 'Aggregate function: returns the maximum value of the expression in a group.',
# 'min': 'Aggregate function: returns the minimum value of the expression in a group.',
# 'first': 'Aggregate function: returns the first value in a group.',
# 'last': 'Aggregate function: returns the last value in a group.',
# 'count': 'Aggregate function: returns the number of items in a group.',
# 'sum': 'Aggregate function: returns the sum of all values in the expression.',
# 'avg': 'Aggregate function: returns the average of the values in a group.',
# 'mean': 'Aggregate function: returns the average of the values in a group.',
# 'sumDistinct': 'Aggregate function: returns the sum of distinct values in the expression.',

df.describe("总价").show()
# +-------+-----------------+
# |summary|             总价|
# +-------+-----------------+
# |  count|            47104|
# |   mean|    577.736916000|
# | stddev|544.7605196104298|
# |    min|          1.10000|
# |    max|       9800.00000|
# +-------+-----------------+

print(df)
print(type(df))


df.select('id', '城市', '区县', '区域', '小区').filter("id = 5000").show()

sc.stop()


