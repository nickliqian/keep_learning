from pyspark import SparkContext

sc = SparkContext("local", "First App")
logFile = "abc.txt"
logData = sc.textFile(logFile).cache()
numAs = logData.filter(lambda s: 'a' in s).count()
numBs = logData.filter(lambda s: 'b' in s).count()
print("Line with a:%i,line with b:%i" % (numAs, numBs))
