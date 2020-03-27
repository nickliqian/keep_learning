# foreach.py
from pyspark import SparkContext
sc = SparkContext("local", "ForEach app")

accum = sc.accumulator(0)
data = [1, 2, 3, 4, 5]
rdd = sc.parallelize(data)


def increment_counter(x):
    print(x)
    accum.add(x)


s = rdd.foreach(increment_counter)
print(s)  # None
print("Counter value: ", accum)
