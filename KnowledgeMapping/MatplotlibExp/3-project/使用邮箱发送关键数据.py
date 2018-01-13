import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt


def get_info():
    df = pd.read_csv("/home/nick/Desktop/DA/speedFile/count.csv", index_col=None, names=["total"],
                     parse_dates=True, dtype={"total": np.int64}, encoding="utf-8")


    # 获取今天零点的时间字符串
    end_day = str(time.strftime("%Y-%m-%d 00:00:00", time.localtime()))

    # 获取总数
    total = df.iat[-1, -1]
    print("---------")
    s1 = "---------"
    print("截自目前采集总数为：%d 条" % total)
    s2 = "\n截自目前采集总数为：%d 条\n\n" % total

    # 获得近10分钟的采集速度
    increment = df['total'].diff()
    recent_status = pd.DataFrame({"Crawl Speed": increment}, index=df.index)
    print("---------近10分钟采集速度 (条)")
    print(recent_status[-10:])
    s00 = "---------近10分钟采集速度 (条)\n"
    s0 = str(recent_status[-10:]) + "\n"

    # 获取今日之前每日的采集量
    df_standard = df.loc["2018-01-03 00:00:00":end_day]

    # 生成每分钟速度DF
    increment = df_standard['total'].diff()
    df_speed_of_min = pd.DataFrame({"Crawl Speed": increment}, index=df_standard.index)

    # 构造不同精度DF
    each_day_speed_sum = df_speed_of_min.resample('1D').sum()
    each_day_speed_sum["Crawl Speed"] = each_day_speed_sum["Crawl Speed"].astype(np.int64)
    each_day_speed_sum = each_day_speed_sum.sort_index(axis=0)

    each_day_speed_mean = df_speed_of_min.resample('1D').mean()
    each_day_speed_mean["Crawl Speed"] = each_day_speed_mean["Crawl Speed"].astype(np.float32)

    # 控制台打印时显示两位小数
    pd.set_option('precision', 2)

    print("---------每日采集数据条数 (条)")
    print(each_day_speed_sum)
    print("---------每日采集平均速度 (条/分钟)")
    print(each_day_speed_mean)

    s3 = "---------每日采集数据条数 (条)\n"
    s4 = str(each_day_speed_sum) + "\n"
    s5 = "---------每日采集平均速度 (条/分钟)\n"
    s6 = str(each_day_speed_mean) + "\n"

    s = s1 + s2 + s00 + s0 + s3 + s4 + s5 + s6

    print(s)


def get_pic():
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

get_info()
