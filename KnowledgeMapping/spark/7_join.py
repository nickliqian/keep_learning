from pyspark import SparkContext


sc = SparkContext("local", "Join app")
x = sc.parallelize([("spark", 1), ("hadoop", 4), ("python", 4)])
y = sc.parallelize([("spark", 2), ("hadoop", 5)])
print("x =>", x.collect())
print("y =>", y.collect())
joined = x.join(y)
final = joined.collect()
print( "Join RDD -> %s" % (final))
