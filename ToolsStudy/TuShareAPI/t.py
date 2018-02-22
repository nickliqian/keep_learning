import tushare as ts

a = ts.get_hist_data('600848') #一次性获取全部日k线数据

# print(a)
print(type(a))