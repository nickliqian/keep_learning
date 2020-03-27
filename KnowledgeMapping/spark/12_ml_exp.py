from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, SparkSession
from pyspark.ml.regression import LinearRegression
from pyspark.ml.linalg import Vector
from pyspark.ml.feature import VectorAssembler

sc = SparkContext("local", appName="app")
sqlContext = SQLContext(sc)

data = sqlContext.read.format("com.databricks.spark.csv").options(header="true", inferschema="true").load("Boston_housing.csv")
vec_assmebler = VectorAssembler(inputCols=["CRIM", "ZN", "INDUS", "CHAS", "NOX",
                                         "RM", "AGE", "DIS", "RAD", "TAX", "PIRATIO",
                                         "B", "LSTAT"], outputCol='features') # 转换，这里相对将多元一次方程中的各变量存放到一个向量中
features_df = vec_assmebler.transform(data)
data = features_df.select("features", "MEDV")

train_df, test_df = data.randomSplit([0.7, 0.3])
print((train_df.count(), len(train_df.columns)))
print((test_df.count(), len(test_df.columns)))

lr = LinearRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8, labelCol="MEDV")
lr_model = lr.fit(train_df)


print('{}{}'.format('方程截距:',lr_model.intercept))         # intercept 线性方程的截距。

print('{}{}'.format('方程参数系数:',lr_model.coefficients))  # 回归方程中的，变量参数 ,这里分别对应var_1,var_2,var_3,var_4,var_5

training_predictions=lr_model.evaluate(train_df)            # 查看预测数据

print('{}{}'.format('误差差值平方:',training_predictions.meanSquaredError))            # 误差值差值平方

print('{}{}'.format('判定系数：',training_predictions.r2 ))  # r2 判定系数,用来判定，构建的模型是否能够准确的预测,越大说明预测的准确率越高

# 7-使用预测数据,用已经到构建好的预测模型 lr_model
test_results=lr_model.evaluate(test_df)

# spark = SparkSession.builder.appName("LinearRegressionWithElasticNet").getOrCreate()
# training = spark.read.format("libsvm").load("data/mllib/sample_linear_regression_data.txt")
# df = sqlContext.createDataFrame(data, ["LSTAT", "MEDV"])
# df.show()
