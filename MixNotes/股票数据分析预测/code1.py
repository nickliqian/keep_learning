from matplotlib import pyplot as plt
import requests_cache
# 忽略不必要的警告
import warnings
warnings.filterwarnings('ignore')
import pandas_datareader.data as web
import pandas as pd
import datetime


# 设定缓存及过期时间
expire_after = datetime.timedelta(days=3)
session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)

end = datetime.datetime.now() # 指定结束时间
start = end - 10 * datetime.timedelta(days=365) # 10 年前

# 获取股票交易代码为 000001.SZ 的数据
df = web.DataReader('000001.SZ', 'yahoo', start, end, session=session)

print("null count:", df.isnull().values.sum())

close = df.Close

close.plot(figsize=(16, 9))