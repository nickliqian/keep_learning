import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib.dates as mdate




df = pd.read_csv("./count.csv", index_col=None, names=["total"],
                 parse_dates=True, dtype={"total": np.int64}, encoding="utf-8")


class MakeMaterial(object):

    def __init__(self):
        end_day = str(time.strftime("%Y-%m-%d 00:00:00", time.localtime()))
        self.df = pd.read_csv("./count.csv", index_col=None, names=["total"],
                         parse_dates=True, dtype={"total": np.int64}, encoding="utf-8")
        self.df_std = df.loc["2018-01-03 00:00:00":end_day]

    @staticmethod
    def data_li(s):
        st = ""
        for i in str(s).split("\n")[1:]:
            a = "<li>" + i + "</li>"
            st += a
        return st

    def recent_data(self):
        # 生成数据
        increment = self.df['total'].diff()
        recent_status = pd.DataFrame({"Crawl Speed": increment}, index=df.index)[-60:]
        # 设置画布和画布大小
        fig, ax = plt.subplots()
        fig.set_size_inches(12, 6)
        # 指定数据
        ax.plot_date(recent_status.index.to_pydatetime(), recent_status["Crawl Speed"], 'o-')
        ax.xaxis.grid(True)
        ax.yaxis.grid(True)
        ax.xaxis.set_major_locator(mdate.MinuteLocator(interval=10))
        ax.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))
        plt.title('1 Hour Crawl Speed recently', color='#123456')
        plt.xlabel("DateTime")
        plt.ylabel("Crawl Quantity(row)")
        plt.show()

    def total_trend(self):
        # 设置画布和画布大小
        fig, ax = plt.subplots()
        fig.set_size_inches(12, 6)
        # 指定数据
        ax.plot_date(self.df.index.to_pydatetime(), self.df["total"], '')
        ax.xaxis.set_major_locator(mdate.DayLocator())
        ax.xaxis.set_major_formatter(mdate.DateFormatter('%m-%d'))
        plt.title('Total Data Row', color='#123456')
        plt.xlabel("DateTime")
        plt.ylabel("Crawl Quantity(row)")
        plt.show()


m = MakeMaterial()
m.total_trend()


# # 显示总量变化 采样频率为1分钟
# df.plot()
# plt.title('Total counts change each minute', color='#123456')
# plt.savefig("pic1.png")
# # plt.show()
#
# # 降低采样频率 以一小时为单位显示总量变化
# a = df.resample('1H').mean()
# # 绘图
# a.plot()  # marker="v" 点的形状
# plt.title('Total counts change each hour', color='#123456')
# plt.savefig("pic2.png")
# # plt.show()
#
# # 以一小时为单位显示采集速度
# increment = df['total'].diff()
# dif = pd.DataFrame({"crawl speed": increment}, index=df.index)
# b = dif.resample('1H').sum()
# # 绘图
# b.plot()
# plt.title('Crawl speed each day', color='#123456')
# plt.savefig("pic3.png")
# # plt.show()
#
# # 显示每天采集的量
# c = dif.resample('1D').sum()
# # 绘图
# c.plot(kind="bar", figsize=(10, 6))
# plt.title('Crawl Data Quantity Of HLJ Spider Each Day', color='#123456')
# plt.xlabel("DateTime")
# plt.ylabel("Data Total(row)")
# plt.ylim(0, 130000)
# plt.grid(True)
# plt.text(2, 100000, r'$mu=100, sigma=15$')
#
# plt.savefig("pic4.png")
# # plt.axis([40, 160, 0, 0.03])
# # plt.show()