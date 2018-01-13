import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time


df = pd.read_csv("./count.csv", index_col=None, names=["total"],
                 parse_dates=True, dtype={"total": np.int64}, encoding="utf-8")
end_day = str(time.strftime("%Y-%m-%d 00:00:00", time.localtime()))
df = df.loc["2018-01-03 00:00:00":end_day]


# plt.figure(1)

# 显示总量变化 采样频率为1分钟
# 绘图
df.plot()
plt.title('Total counts change each minute', color='#123456')
plt.savefig("pic1.png")
# plt.show()


# 降低采样频率 以一小时为单位显示总量变化
a = df.resample('1H').mean()
# 绘图
a.plot()  # marker="v" 点的形状
plt.title('Total counts change each hour', color='#123456')
plt.savefig("pic2.png")
# plt.show()


# 以一小时为单位显示采集速度
increment = df['total'].diff()
dif = pd.DataFrame({"crawl speed": increment}, index=df.index)
b = dif.resample('1H').sum()
# 绘图
b.plot()
plt.title('Crawl speed each day', color='#123456')
plt.savefig("pic3.png")
# plt.show()


# 显示每天采集的量
c = dif.resample('1D').sum()
# 绘图
c.plot(kind="bar", figsize=(10, 6))
plt.title('Crawl Data Quantity Of HLJ Spider Each Day', color='#123456')
plt.xlabel("DateTime")
plt.ylabel("Data Total(row)")
plt.ylim(0, 130000)
plt.grid(True)
plt.text(2, 100000, r'$mu=100, sigma=15$')

plt.savefig("pic4.png")
# plt.axis([40, 160, 0, 0.03])
# plt.show()
