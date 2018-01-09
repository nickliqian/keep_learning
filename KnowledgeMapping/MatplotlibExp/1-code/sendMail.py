import smtplib
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase


def send_email(con="你好！"):
    _user = "15999543812@163.com"
    _pwd = "nickliqian2017"
    _to = "419845955@qq.com"

    # 使用MIMEText构造符合smtp协议的header及body
    msg = MIMEText(con)
    subject = "以下是今天的报表，请查收！--" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    msg["Subject"] = subject
    msg["From"] = _user
    msg["To"] = _to

    with open("result.png", 'rb') as f:
        # 设置附件的MIME和文件名，这里是png类型:
        mime = MIMEBase('image', 'jpg', filename="result.png")
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename="result.png")
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码:
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        msg.attach(mime)
        # msg.attach(MIMEText('<html><body><h1>Hello</h1><p><img src="cid:' + str(i) + '"></p></body></html>', 'html', 'utf-8'))


    s = smtplib.SMTP("smtp.163.com", timeout=30)  # 连接smtp邮件服务器,端口默认是25
    s.login(_user, _pwd)  # 登陆服务器
    s.sendmail(_user, _to, msg.as_string())  # 发送邮件
    s.close()


def deal_data():
    df = pd.read_csv("./count.csv", names=["time", "total"], encoding="utf-8")
    df = df[-60:]
    tx = np.array(df['time'])
    ty = np.array(df['total'])
    # 两个图画一起
    plt.figure('data & model')
    plt.plot(tx, ty, 'k', lw=3)
    # 将当前figure的图保存到文件result.png
    plt.savefig('result.png')
    # 一定要加上这句才能让画好的图显示在屏幕上
    plt.show()
    return str(df)


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
    deal_data()
    send_email(con="你好！")


if __name__ == '__main__':
    main()
