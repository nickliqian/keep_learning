#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ctypes import *

"""
编译动态链接库生成 libtest.so文件（DLL）

gcc -fPIC -shared test.c -o libtest.so
"""

# 加载动态链接库文件
testlib = CDLL("libtest.so")
# testlib = cdll.LoadLibrary("libtest.so")  # 或者这种形式
add = testlib.add  # 传递方法
add.argtypes = [c_int, c_int]  # 定义参数类型 int对应ctypes的c_int类型
add.restype = c_int  # 定义返回值类型
s = add(3, 6)
print(s)
