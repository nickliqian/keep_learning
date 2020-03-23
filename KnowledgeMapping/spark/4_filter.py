# filter.py
from pyspark import SparkContext
sc = SparkContext("local", "Filter app")
words = sc.parallelize(
    ["scala",
     "java",
     "hadoop",
     "spark",
     "akka",
     "spark vs hadoop",
     "pyspark",
     "pyspark and spark"]
)
# words_filter = words.filter(lambda x: 'spark' in x)


def g(x):
    for i in x:
        if "spark" in x:
            return i


words_filter = words.filter(g)

filtered = words_filter.collect()
print("Fitered RDD -> %s" % (filtered))