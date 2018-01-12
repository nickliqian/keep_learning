import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import smtplib
from email.mime.text import MIMEText
import time


def send_email(con="你好！"):
    _user = "15999543812@163.com"
    _pwd = "nickliqian2017"
    _to = "419845955@qq.com"

    # 使用MIMEText构造符合smtp协议的header及body
    msg = MIMEText(con)
    subject = "以下是今天的报表，请查收！--" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # # msgRoot['From'] = Header("菜鸟教程", 'utf-8')
    msg["Subject"] = subject
    msg["From"] = _user
    msg["To"] = _to

    s = smtplib.SMTP("smtpExp.163.com", timeout=30)  # 连接smtp邮件服务器,端口默认是25
    s.login(_user, _pwd)  # 登陆服务器
    s.sendmail(_user, _to, msg.as_string())  # 发送邮件
    s.close()


def deal_data():
    # time作为列内容
    df = pd.read_csv("./count.csv", names=["time", "total"], dtype={"total": np.int64}, parse_dates=[0], encoding="utf-8")

    df60 = df[-60:]
    increment = df60['total'].diff()
    df60["increment"] = increment
    # print(df)

    df.plot(figsize=(12, 8))

    # plt.figure('data & model')
    # plt.plot(df["time"], df["total"], 'k', lw=3)
    # # plt.savefig('result.png')
    # plt.show()


def check():
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
    print(s)



if __name__ == '__main__':
    main()
