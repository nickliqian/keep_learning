import pandas as pd


# https://www.cnblogs.com/chaosimple/p/4153083.html

FILE_PATH = "/home/nick/Desktop/DA/speedFile/count.csv"


df = pd.read_csv(FILE_PATH, header=None, index_col=0)
df.index = pd.to_datetime(df.index)
ts = df[1]
print(ts.head())
print("-------------------")
print(ts.head().index)
