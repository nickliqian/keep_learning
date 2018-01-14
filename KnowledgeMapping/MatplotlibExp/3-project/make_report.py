import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib.dates as mdate
import os
import sys
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MakeMaterial(object):

    def __init__(self):
        # 定义初始量
        self.recent_status_mean = ''
        self.today_hour_speed_mean = ''
        self.hour_speed_mean = ''

        end_day = str(time.strftime("%Y-%m-%d 00:00:00", time.localtime()))
        now_hour = str(time.localtime().tm_hour)
        # 所有数据
        self.df = pd.read_csv("./count.csv", index_col=None, names=["total"],
                         parse_dates=True, dtype={"total": np.int64}, encoding="utf-8")
        # 去掉今天的不完整数据
        self.df_std = self.df.loc["2018-01-03 00:00:00":end_day]
        increment = self.df['total'].diff()
        # 所有每分钟速度数据
        self.dif = pd.DataFrame({"Crawl Speed": increment}, index=self.df.index)
        self.dif_std = self.dif.loc["2018-01-03 00:00:00":end_day]
        self.dif_today = self.dif.loc[end_day:]
        self.save_dir = "./resultPIC"
        if not os.path.exists(self.save_dir):
            os.mkdir(self.save_dir)
        total = self.df.iat[-1, -1]
        today_total = self.dif_today.sum()
        today_total = today_total.iat[-1]
        self.total_count = """
                            <h3>截自今天%s时,数据总量为:
                                <p style='text-decoration:underline'> %s 条</p>
                            </h3>
                            <h3>今日已采集条数为:
                                <p style='text-decoration:underline'> %s 条</p>
                            </h3>
                            <br>
                            """ % (now_hour, str(total), str(int(today_total)))

    @staticmethod
    def data_li(s):
        st = ""
        for i in str(s).split("\n")[1:]:
            a = "<li>" + i + "</li>"
            st += a
        return st

    def create_mimeimg(self, func_name):
        name = os.path.join(self.save_dir, func_name + ".png")
        plt.savefig(name)
        with open(name, "rb") as f:
            msgImage = MIMEImage(f.read())
        return msgImage

    # 生成近一小时每分钟采集的数量
    def recent_data(self):
        # 生成数据
        recent_status = self.dif[-60:]
        self.recent_status_mean = recent_status["Crawl Speed"].mean()
        # 设置画布和画布大小
        fig, ax = plt.subplots()
        fig.set_size_inches(12, 6)
        # 指定数据
        ax.plot_date(recent_status.index.to_pydatetime(), recent_status["Crawl Speed"], 'o-')
        ax.xaxis.grid(True)
        ax.yaxis.grid(True)
        ax.xaxis.set_major_locator(mdate.MinuteLocator(interval=10))
        ax.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))
        plt.title('1 Hour Crawl Speed recently - Unit: row/hour', color='#123456')
        plt.xlabel("DateTime")
        plt.ylabel("Crawl Quantity(row)")
        # 平均值线
        ax.axhline(self.recent_status_mean, ls="-", color="red")
        # plt.show()
        return self.create_mimeimg(sys._getframe().f_code.co_name)

    # 生成整体采集的趋势
    def total_trend(self):
        # 设置画布和画布大小
        fig, ax = plt.subplots()
        fig.set_size_inches(12, 6)
        # 指定数据
        ax.plot_date(self.df.index.to_pydatetime(), self.df["total"], '')
        ax.xaxis.set_major_locator(mdate.DayLocator())
        ax.xaxis.set_major_formatter(mdate.DateFormatter('%m-%d'))
        plt.title('Total Data Row - Unit: row', color='#123456')
        plt.xlabel("DateTime")
        plt.ylabel("Crawl Quantity(row)")
        # plt.show()
        return self.create_mimeimg(sys._getframe().f_code.co_name)

    # 生成每天采集的数量
    def each_day_count(self):
        # 生成数据
        each_counts = self.dif_std.resample('1D').sum()
        # 设置画布和画布大小
        fig, ax = plt.subplots()
        fig.set_size_inches(12, 6)
        # 指定数据
        ax.bar(each_counts.index.to_pydatetime(), each_counts["Crawl Speed"])
        ax.xaxis.set_major_locator(mdate.DayLocator())
        ax.xaxis.set_major_formatter(mdate.DateFormatter('%m-%d'))
        plt.title('Each Day Counts - Unit: row/day', color='#123456')
        plt.xlabel("DateTime")
        plt.ylabel("Crawl Quantity(row)")
        # plt.show()
        return self.create_mimeimg(sys._getframe().f_code.co_name)
        
    # 生成每天采集的速度
    def each_day_speed(self):
        # 生成数据
        each_speed = self.dif.resample('1D').mean()
        # 设置画布和画布大小
        fig, ax = plt.subplots()
        fig.set_size_inches(12, 6)
        # 指定数据
        ax.bar(each_speed.index.to_pydatetime(), each_speed["Crawl Speed"])
        ax.xaxis.set_major_locator(mdate.DayLocator())
        ax.xaxis.set_major_formatter(mdate.DateFormatter('%m-%d'))
        plt.title('Each Day Speed - Unit: row/day', color='#123456')
        plt.xlabel("DateTime")
        plt.ylabel("Crawl Quantity(row)")
        # plt.show()
        return self.create_mimeimg(sys._getframe().f_code.co_name)
    
    # 每小时的采集速度    
    def each_hour_speed(self):
        hour_speed = self.dif.resample('1H').sum()[:-1]
        self.hour_speed_mean = hour_speed["Crawl Speed"].mean()
        # 设置画布和画布大小
        fig, ax = plt.subplots()
        fig.set_size_inches(12, 6)
        # 指定数据
        ax.plot_date(hour_speed.index.to_pydatetime(), hour_speed["Crawl Speed"], '')

        # 次要x轴标签
        ax.xaxis.set_minor_locator(mdate.DayLocator())
        ax.xaxis.set_minor_formatter(mdate.DateFormatter('\n%m-%d'))
        # 网格线
        # ax.xaxis.grid(True, which="minor")
        ax.yaxis.grid()
        # 主要x轴标签
        ax.xaxis.set_major_locator(mdate.MinuteLocator(interval=720))
        ax.xaxis.set_major_formatter(mdate.DateFormatter('%HH'))
        # 平均值线
        ax.axhline(self.hour_speed_mean, ls="-", color="red")

        plt.title('Each Day Speed - Unit: row/min', color='#123456')
        plt.xlabel("DateTime")
        plt.ylabel("Crawl Quantity(row)")
        # plt.show()
        return self.create_mimeimg(sys._getframe().f_code.co_name)

    # 今天每小时的采集速度
    def today_hour_speed(self):
        # 生成数据
        today_hour_speed = self.dif_today.resample('1H').sum()[:-1]
        self.today_hour_speed_mean = today_hour_speed["Crawl Speed"].mean()
        # 设置画布和画布大小
        fig, ax = plt.subplots()
        fig.set_size_inches(12, 6)
        # 指定数据
        ax.plot_date(today_hour_speed.index.to_pydatetime(), today_hour_speed["Crawl Speed"], '')

        # 主要x轴标签
        ax.xaxis.set_major_locator(mdate.HourLocator(interval=1))
        ax.xaxis.set_major_formatter(mdate.DateFormatter('%H'))
        # 平均值线
        ax.axhline(self.today_hour_speed_mean, ls="-", color="red")

        plt.title('Today Speed Each Hour - Unit: row', color='#123456')
        plt.xlabel("DateTime")
        plt.ylabel("Crawl Quantity(row)")
        # plt.show()
        return self.create_mimeimg(sys._getframe().f_code.co_name)

    # 保存所有图片
    def save_img(self):
        item = {}
        item['recent_data'] = self.recent_data()
        item['total_trend'] = self.total_trend()
        item['each_day_count'] = self.each_day_count()
        item['each_day_speed'] = self.each_day_speed()
        item['each_hour_speed'] = self.each_hour_speed()
        item['today_hour_speed'] = self.today_hour_speed()

        content = """
            <h3>最近一小时采集速度如下</h3>
            <p>其中分钟平均速度为 %s 条/分钟</p>
            <p><img src="cid:recent_data"></p>
            <h3>今日采集速度</h3>
            <p>其中小时平均速度为 %s 条/小时</p>
            <p><img src="cid:today_hour_speed"></p>
            <h3>项目采集总量趋势</h3>
            <p><img src="cid:total_trend"></p>
            <h3>项目每日采集数量统计</h3>
            <p><img src="cid:each_day_count"></p>
            <h3>项目每日采集平均速度统计</h3>
            <p><img src="cid:each_day_speed"></p>
            <h3>项目每小时采集量变化</h3>
            <p>平均速度为 %s 条/小时</p>
            <p><img src="cid:each_hour_speed"></p>
        """ % (str(int(self.recent_status_mean)), str(int(self.today_hour_speed_mean)), str(int(self.hour_speed_mean)))

        return item, content

    def send_email(self):

        item, content = self.save_img()

        _user = "nickliqianvt@sina.com"
        _pwd = "nickliqian2017"
        _to = "419845955@qq.com"

        # 使用MIMEText构造符合smtp协议的header及body
        msg = MIMEMultipart('related')
        subject = "以下是今天的报表，请查收！--" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # # msgRoot['From'] = Header("菜鸟教程", 'utf-8')
        msg["Subject"] = subject
        msg["From"] = _user
        msg["To"] = _to

        # 可供选择的内容
        msgAlternative = MIMEMultipart('alternative')
        msg.attach(msgAlternative)
        # html数据
        con = self.total_count + content
        msgAlternative.attach(MIMEText(con, 'html', 'utf-8'))

        # 定义图片 ID，在 HTML 文本中引用
        for dic in item.items():
            img = dic[1]
            img.add_header('Content-ID', dic[0])
            msg.attach(img)

        s = smtplib.SMTP("smtp.sina.com", 25, timeout=30)  # 连接smtp邮件服务器,端口默认是25
        s.login(_user, _pwd)  # 登陆服务器
        s.sendmail(_user, _to, msg.as_string())  # 发送邮件
        s.close()


m = MakeMaterial()
m.send_email()
