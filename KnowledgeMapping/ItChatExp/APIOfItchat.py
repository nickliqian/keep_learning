import itchat

# 给filehelper发送一条消息
itchat.auto_login()
itchat.send('Hello!', toUserName='filehelper')


# 回复发送给自己的消息
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    return msg.text


# 通过如下代码，微信已经可以就日常的各种信息进行获取与回复
import itchat, time
from itchat.content import *


# 收到文本/地图等消息类型 -> 回复：类型+内容
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    msg.user.send('%s: %s' % (msg.type, msg.text))


# 收到多媒体文件类型
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg.download(msg.fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    return '@%s@%s' % (typeSymbol, msg.fileName)


# 收到好友请求消息：添加+回复
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    msg.user.send('Nice to meet you!')


# 收到群组消息，如果消息是@类型，就回复消息
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg.isAt:
        msg.user.send(u'@%s\u2005I received: %s' % (
            msg.actualNickName, msg.text))


itchat.auto_login(True)
itchat.run(True)


# 退出后暂存登录状态
itchat.auto_login(hotReload=True)


# 附件下载与发送
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg.download(msg.fileName)
    itchat.send('@%s@%s' % (
        'img' if msg['Type'] == 'Picture' else 'fil', msg['FileName']),
        msg['FromUserName'])
    return '%s received' % msg['Type']


# 退出时调用特定方法
def lc():
    print('finish login')
def ec():
    print('exit')


itchat.auto_login(loginCallback=lc, exitCallback=ec)
time.sleep(3)
itchat.logout()