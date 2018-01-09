import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import time

# sender = 'from@runoob.com'
# receivers = ['429240967@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
#
# msgRoot = MIMEMultipart('related')
# msgRoot['From'] = Header("菜鸟教程", 'utf-8')
# msgRoot['To'] = Header("测试", 'utf-8')
# subject = 'Python SMTP 邮件测试'
# msgRoot['Subject'] = Header(subject, 'utf-8')
#
# msgAlternative = MIMEMultipart('alternative')
# msgRoot.attach(msgAlternative)
#
# mail_msg = """
# <p>Python 邮件发送测试...</p>
# <p><a href="http://www.runoob.com">菜鸟教程链接</a></p>
# <p>图片演示：</p>
# <p><img src="cid:image1"></p>
# """
# msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))
#
# # 指定图片为当前目录
# fp = open('result.png', 'rb')
# msgImage = MIMEImage(fp.read())
# fp.close()
#
# # 定义图片 ID，在 HTML 文本中引用
# msgImage.add_header('Content-ID', '<image1>')
# msgRoot.attach(msgImage)
#
# try:
#     smtpObj = smtplib.SMTP('localhost')
#     smtpObj.sendmail(sender, receivers, msgRoot.as_string())
#     print("邮件发送成功")
# except smtplib.SMTPException:
#     print("Error: 无法发送邮件")



_user = "15999543812@163.com"
_pwd = "nickliqian2017"
_to = "419845955@qq.com"

# 使用MIMEText构造符合smtp协议的header及body
msg = MIMEMultipart('related')
subject = "以下是今天的报表，请查收！--" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
msg["Subject"] = subject
msg["From"] = _user
msg["To"] = _to

msgAlternative = MIMEMultipart('alternative')
msg.attach(msgAlternative)

mail_msg = """
<p>Python 邮件发送测试...</p>
<p><a href="http://www.runoob.com">菜鸟教程链接</a></p>
<p>图片演示：</p>
<p><img src="cid:image1"></p>
"""
msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

# 指定图片为当前目录
fp = open('result.png', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()

# 定义图片 ID，在 HTML 文本中引用
msgImage.add_header('Content-ID', '<image1>')
msg.attach(msgImage)

s = smtplib.SMTP("smtp.163.com", timeout=30)  # 连接smtp邮件服务器,端口默认是25
s.login(_user, _pwd)  # 登陆服务器
s.sendmail(_user, _to, msg.as_string())  # 发送邮件
s.close()