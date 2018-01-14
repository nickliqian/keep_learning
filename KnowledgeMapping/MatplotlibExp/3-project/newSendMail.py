import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time


def send_email(con="你好！"):
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

    mail_msg1 = '<p><img src="cid:image1"></p>'
    mail_msg2 = '<p><img src="cid:image2"></p>'
    mail_msg3 = '<p><img src="cid:image3"></p>'
    mail_msg4 = '<p><img src="cid:image4"></p>'

    mail_msg = mail_msg1 + mail_msg2 + mail_msg3 + mail_msg4
    msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))
    # 指定图片为当前目录

    with open("pic1.png", "rb") as f:
        msgImage1 = MIMEImage(f.read())

    with open("pic2.png", "rb") as f:
        msgImage2 = MIMEImage(f.read())

    with open("pic3.png", "rb") as f:
        msgImage3 = MIMEImage(f.read())

    with open("pic4.png", "rb") as f:
        msgImage4 = MIMEImage(f.read())

    # 定义图片 ID，在 HTML 文本中引用
    msgImage1.add_header('Content-ID', '<image1>')
    msgImage2.add_header('Content-ID', '<image2>')
    msgImage3.add_header('Content-ID', '<image3>')
    msgImage4.add_header('Content-ID', '<image4>')
    msg.attach(msgImage1)
    msg.attach(msgImage2)
    msg.attach(msgImage3)
    msg.attach(msgImage4)

    s = smtplib.SMTP("smtp.sina.com", 25, timeout=30)  # 连接smtp邮件服务器,端口默认是25
    s.login(_user, _pwd)  # 登陆服务器
    s.sendmail(_user, _to, msg.as_string())  # 发送邮件
    s.close()

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


def data_li(s):
    st = ""
    for i in str(s).split("\n")[1:]:
        a = "<li>" + i + "</li>"
        st += a
    return st


def deal_data():
    df = pd.read_csv("./count.csv", index_col=None, names=["total"],
                     parse_dates=True, dtype={"total": np.int64}, encoding="utf-8")

    # 获取今天零点的时间字符串
    end_day = str(time.strftime("%Y-%m-%d 00:00:00", time.localtime()))

    # 获取总数
    total = df.iat[-1, -1]
    s1 = "<li>以下是近期的采集数据报告</li>"
    s2 = "<li>截自目前采集总数为：%d 条</li>" % total

    # 获得近10分钟的采集速度
    increment = df['total'].diff()
    recent_status = pd.DataFrame({"Crawl Speed": increment}, index=df.index)
    s3 = "<li>近10分钟采集速度 (条)</li>"
    s4 = str(recent_status[-10:])
    s4 = data_li(s4)

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

    s5 = "<li>每日采集数据条数 (条)</li>"
    s6= str(each_day_speed_sum)
    s6 = data_li(s6)
    s7 = "<li>每日采集平均速度 (条/分钟)</li>"
    s8 = str(each_day_speed_mean)
    s8 = data_li(s8)

    s = s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8

    print(s)

    return s


def check():
    get_pic()
    df = deal_data()
    while True:
        try:
            send_email(con=df)
            break
        except smtplib.SMTPDataError as e:
            if isinstance(e, smtplib.SMTPSenderRefused):
                pass
            elif isinstance(e, smtplib.SMTPDataError):
                pass
            else:
                raise e
        time.sleep(20)


def main():
    s = deal_data()
    send_email(s)


if __name__ == '__main__':
    deal_data()
