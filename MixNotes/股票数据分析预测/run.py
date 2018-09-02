import quandl

# 获取苹果公司股票数据
# r = quandl.get('WIKI/AAPL')


import warnings
warnings.filterwarnings('ignore')
import pandas_datareader.data as web
import pandas as pd
import datetime


start = datetime.datetime(2018, 1, 1) # 指定开始时间
end = datetime.datetime.now() # 指定结束时间

# 获取股票交易代码为 000001.SZ 的数据
SZ000001 = web.DataReader('000001.SZ', 'yahoo', start, end)
print(type(SZ000001))
print(SZ000001.shape)


