import tushare as ts
import matplotlib.pyplot as plt


result = ts.get_hist_data('002716')  # 一次性获取全部日k线数据

print(result)

plt.boxplot(result["close"])
plt.show()


