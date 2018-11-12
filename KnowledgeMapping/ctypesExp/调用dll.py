# coding=gbk
# 第一行注释不能省，指定编码声明以支持中文
# 本代码文件在32位的python 3.4.3版测试通过
import urllib
import time
import string
import ctypes
from ctypes import *

dll = ctypes.windll.LoadLibrary('WmCode.dll')
# 如果dll不在当前目录，那么需要指定全路径


if (dll.UseUnicodeString(1, 1)):  # 这个函数用来向DLL说明传入的文本使用unicode格式
    print('SetInUnicode Success:')  # UseUnicodeString调用一次即可，无需重复调用
else:
    print('etInUnicode Fail!')  # 注意缩进格式

if (dll.LoadWmFromFile('D:\网易论坛.dat', '163')):  # 使用绝对路径
    print('Loaddat Success:')  # LoadWmFromFile调用一次即可，无需重复调用
    Str = create_string_buffer(20)  # 创建文本缓冲区
    if (dll.GetImageFromFile('D:\wylt.JPG', Str)):  # 使用绝对路径
        # 如果验证码图像不在当前目录，那么需要指定全路径
        print('GetVcode Success:', Str.raw.decode("gbk"))
        # 返回的文本自行处理口口口问题
    else:
        print('GetVcode Fail!')


else:
    print('Loaddat Fail!')  # 注意缩进格式


"""
from ctypes import *


# 加载动态链接库文件
testlib = CDLL("libtest.dll")
# testlib = cdll.LoadLibrary("libtest.so")  # 或者这种形式
add = testlib.add  # 传递方法
add.argtypes = [c_int, c_int]  # 定义参数类型 int对应ctypes的c_int类型
add.restype = c_int  # 定义返回值类型
s = add(3, 6)
print(s)

"""