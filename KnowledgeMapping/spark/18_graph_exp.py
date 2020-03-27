from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import col, lit, when
from pyspark.sql.types import IntegerType
from graphframes.examples import Graphs
from functools import reduce


sc = SparkContext("local", appName="mysqltest")
sqlContext = SQLContext(sc)


g = Graphs(sqlContext).friends()  # Get example graph

chain4 = g.find("(a)-[ab]->(b); (b)-[bc]->(c); (c)-[cd]->(d)")

# Query on sequence, with state (cnt)
#  (a) Define method for updating state given the next element of the motif.
# 给定主题的下一个元素，定义用于更新状态的方法。
# 如果关系为friend则cnt+1
sumFriends = lambda cnt, relationship: when(relationship == "friend", cnt+1).otherwise(cnt)

#  (b) Use sequence operation to apply method to sequence of elements in motif.
# （b）使用序列运算将方法应用于主题中的元素序列。
#      In this case, the elements are the 3 edges.
#  在这种情况下，元素是3个边。
condition =reduce(lambda cnt, e: sumFriends(cnt, col(e).relationship), ["ab", "bc", "cd"], lit(0))

#  (c) Apply filter to DataFrame.
chainWith2Friends2 = chain4.where(condition >= 2)
chainWith2Friends2.show()


g.find("(a)-[ab]->(b); (b)-[bc]->(c); (c)-[cd]->(d)").show()

