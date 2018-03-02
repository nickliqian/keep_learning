import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def mail(mail_sub, mail_content):
    """
    发送邮件
    :param mail_sub: str
    :param mail_content: str
    :return: None
    """
    my_sender = "nickliqianvt@sina.com"  # 发件人邮箱账号
    my_pass = "nickliqian2017"  # 发件人邮箱密码
    my_user = "419845955@qq.com"  # 收件人邮箱账号，我这边发送给自己

    msg = MIMEText(mail_content, 'plain', 'utf-8')
    msg['From'] = formataddr(["FromSpiderSystem", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
    msg['Subject'] = mail_sub  # 邮件的主题，也可以说是标题

    server = smtplib.SMTP_SSL("smtp.sina.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
    server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
    server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
    server.quit()  # 关闭连接
    return None


def info_by_mail(mail_sub, mail_content):
    """
    发送邮件
    :param mail_sub: str 邮件主题
    :param mail_content: str 邮件内容
    :return: None
    """
    mail(mail_sub, mail_content)
    print("邮件发送成功")


if __name__ == '__main__':
    info_by_mail("a", "b")
