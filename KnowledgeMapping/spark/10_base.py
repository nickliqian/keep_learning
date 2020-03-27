from pyspark import SparkContext, SparkConf


conf = SparkConf().setAppName("first").setMaster("local")
sc = SparkContext(conf=conf)

# data = [1, 2, 3, 4, 5]
# distData = sc.parallelize(data)
# distData.reduce(lambda a, b: a + b)

# distData = sc.textFile("README.md", minPartitions=2)

# rdd = sc.parallelize(range(1, 4)).map(lambda x: (x, "a" * x))
# rdd.saveAsSequenceFile("./tmp/data")

# rdd = sc.sequenceFile("./tmp/data")
# result = sorted(rdd.collect())
# print(result)

# conf = {"es.resource": "index/type"}
# rdd = sc.newAPIHadoopRDD("org.elasticsearch.hadoop.mr.EsInputFormat",
#                          "org.apache.hadoop.io.NullWritable",
#                          "org.elasticsearch.hadoop.mr.LinkedMapWritable",
#                          conf=conf)
# print(rdd.first())

# lines = sc.textFile("README.md")
# lineLengths = lines.map(lambda s: len(s))
# totalLength = lineLengths.reduce(lambda a, b: a + b)
# lineLengths.persist()
# print(totalLength)

