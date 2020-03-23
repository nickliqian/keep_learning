from pyspark import SparkConf
from pyspark.sql import SparkSession
import traceback
import os

os.environ["PYSPARK_PYTHON"] = "/usr/bin/python3"  # 集群上pyspark的python版本指向python3
appname = "test"  # 任务名称
master = "spark://192.168.10.204:7337"  # "spark://host:port"
'''
standalone模式:spark://host:port,Spark会自己负责资源的管理调度
mesos模式:mesos://host:port
yarn模式:由于很多时候我们需要和mapreduce使用同一个集群，所以都采用Yarn来管理资源调度，这也是生产环境大多采用yarn模式的原因。yarn模式又分为yarn cluster模式和yarn client模式：
yarn cluster: 这个就是生产环境常用的模式，所有的资源调度和计算都在集群环境上运行。
yarn client: 这个是说Spark Driver和ApplicationMaster进程均在本机运行，而计算任务在cluster上。
'''
spark_driver_host = "192.168.10.87"  # 本地主机ip

conf = SparkConf().setAppName(appname).setMaster(master).set("spark.driver.host", spark_driver_host)
spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext
try:
    words = sc.parallelize(
        ["scala",
         "java",
         "hadoop",
         "spark",
         "akka",
         "spark vs hadoop",
         "pyspark",
         "pyspark and spark"
         ])
    counts = words.count()
    print("Number of elements in RDD is %i" % counts)
    sc.stop()
    print('计算成功！')
except:
    sc.stop()
    traceback.print_exc()  # 返回出错信息
    print('连接出错！')