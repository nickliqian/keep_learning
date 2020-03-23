# reduce.py
from pyspark import SparkContext
from operator import add


sc = SparkContext("local", "Reduce app")

nums = sc.parallelize([1, 2, 3, 4, 5])
print(type(nums))

adding = nums.reduce(add)
print(type(adding))
print("Adding all the elements -> %i" % (adding))
