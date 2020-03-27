from pyspark import SparkContext
from pyspark.sql import SQLContext
from graphframes import GraphFrame


sc = SparkContext("local", appName="mysqltest")
sqlContext = SQLContext(sc)

vertices = sqlContext.createDataFrame([
  ("a", "Alice", 34),
  ("b", "Bob", 36),
  ("c", "Charlie", 30),
  ("d", "David", 29),
  ("e", "Esther", 32),
  ("f", "Fanny", 36),
  ("g", "Gabby", 60)], ["id", "name", "age"])

edges = sqlContext.createDataFrame([
  ("a", "b", "friend"),
  ("b", "c", "follow"),
  ("c", "b", "follow"),
  ("f", "c", "follow"),
  ("e", "f", "follow"),
  ("e", "d", "friend"),
  ("d", "a", "friend"),
  ("a", "e", "friend")
], ["src", "dst", "relationship"])

# 生成图
g = GraphFrame(vertices, edges)
print(g)
# GraphFrame(v:[id: string, name: string ... 1 more field], e:[src: string, dst: string ... 1 more field])
print(type(g))
# <class 'graphframes.graphframe.GraphFrame'>

# 展示顶点和边的数据
g.vertices.show()
# +---+-------+---+
# | id|   name|age|
# +---+-------+---+
# |  a|  Alice| 34|
# |  b|    Bob| 36|
# |  c|Charlie| 30|
# |  d|  David| 29|
# |  e| Esther| 32|
# |  f|  Fanny| 36|
# |  g|  Gabby| 60|
# +---+-------+---+

g.edges.show()
# +---+---+------------+
# |src|dst|relationship|
# +---+---+------------+
# |  a|  b|      friend|
# |  b|  c|      follow|
# |  c|  b|      follow|
# |  f|  c|      follow|
# |  e|  f|      follow|
# |  e|  d|      friend|
# |  d|  a|      friend|
# |  a|  e|      friend|
# +---+---+------------+


# 展示节点入度数、出度数和入度出度的和
g.inDegrees.sort("id").show()
# +---+--------+
# | id|inDegree|
# +---+--------+
# |  a|       1|
# |  b|       2|
# |  c|       2|
# |  d|       1|
# |  e|       1|
# |  f|       1|
# +---+--------+

g.outDegrees.sort("id").show()
# +---+---------+
# | id|outDegree|
# +---+---------+
# |  a|        2|
# |  b|        1|
# |  c|        1|
# |  d|        1|
# |  e|        2|
# |  f|        1|
# +---+---------+

g.degrees.sort("id").show()
# +---+------+
# | id|degree|
# +---+------+
# |  a|     3|
# |  b|     3|
# |  c|     3|
# |  d|     2|
# |  e|     3|
# |  f|     2|
# +---+------+


# 对边和顶点的数据进行分析
agelist = g.vertices.groupBy().min("age").show()
# +--------+
# |min(age)|
# +--------+
# |      29|
# +--------+

youngest = g.vertices.filter("age < 30").show()
# +---+-----+---+
# | id| name|age|
# +---+-----+---+
# |  d|David| 29|
# +---+-----+---+

numFollows = g.edges.filter("relationship = 'follow'").count()
print(numFollows)
# 4


# 搜索指定结构
motif = g.find("(start)-[pass]->(end)")
motif.show()
# +----------------+--------------+----------------+
# |           start|          pass|             end|
# +----------------+--------------+----------------+
# | [e, Esther, 32]|[e, f, follow]|  [f, Fanny, 36]|
# |  [a, Alice, 34]|[a, e, friend]| [e, Esther, 32]|
# | [e, Esther, 32]|[e, d, friend]|  [d, David, 29]|
# |  [f, Fanny, 36]|[f, c, follow]|[c, Charlie, 30]|
# |    [b, Bob, 36]|[b, c, follow]|[c, Charlie, 30]|
# |[c, Charlie, 30]|[c, b, follow]|    [b, Bob, 36]|
# |  [a, Alice, 34]|[a, b, friend]|    [b, Bob, 36]|
# |  [d, David, 29]|[d, a, friend]|  [a, Alice, 34]|
# +----------------+--------------+----------------+

# 在搜索的结果上进行过滤
motif.filter("start.age > 33 and end.age > 33").show()
# +--------------+--------------+------------+
# |         start|          pass|         end|
# +--------------+--------------+------------+
# |[a, Alice, 34]|[a, b, friend]|[b, Bob, 36]|
# +--------------+--------------+------------+

# 多个路径条件
motif = g.find("(a)-[e]->(b); (b)-[e2]->(a)")
motif.show()
# +----------------+--------------+----------------+--------------+
# |               a|             e|               b|            e2|
# +----------------+--------------+----------------+--------------+
# |[c, Charlie, 30]|[c, b, follow]|    [b, Bob, 36]|[b, c, follow]|
# |    [b, Bob, 36]|[b, c, follow]|[c, Charlie, 30]|[c, b, follow]|
# +----------------+--------------+----------------+--------------+
# 注意，上述条件中，a和b可以指代相同的顶点，如果需要限制为不同的顶点，需要在返回结果中使用过滤器


# 不需要返回路径中的元素时，可以使用匿名顶点和边
motif = g.find("(start)-[]->()")
motif.show()
# +----------------+
# |           start|
# +----------------+
# |  [f, Fanny, 36]|
# | [e, Esther, 32]|
# | [e, Esther, 32]|
# |  [d, David, 29]|
# |[c, Charlie, 30]|
# |    [b, Bob, 36]|
# |  [a, Alice, 34]|
# |  [a, Alice, 34]|
# +----------------+

# 设置路径不存在的条件
motif = g.find("(a)-[]->(b); !(b)-[]->(a)")
motif.show()
# +---------------+----------------+
# |              a|               b|
# +---------------+----------------+
# | [a, Alice, 34]| [e, Esther, 32]|
# |[e, Esther, 32]|  [d, David, 29]|
# |[e, Esther, 32]|  [f, Fanny, 36]|
# | [a, Alice, 34]|    [b, Bob, 36]|
# | [f, Fanny, 36]|[c, Charlie, 30]|
# | [d, David, 29]|  [a, Alice, 34]|
# +---------------+----------------+


