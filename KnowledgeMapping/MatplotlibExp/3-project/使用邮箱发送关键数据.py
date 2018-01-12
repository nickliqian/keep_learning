import pandas as pd
import numpy as np
import time


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


get_info()
