#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ctypes import *


dll = CDLL("ocr.dll")
print(dll.init())
print(dll.ocr())


from ctypes import *

# dll = CDLL("ocr.dll")
dll = windll.LoadLibrary("ocr.dll")
dll.init()
ocr = dll.ocr
ocr.argtypes = [c_char_p, c_int]
ocr.restype = c_wchar_p
with open("./upwj.bmp", "rb") as f:
    content = f.read()
print(list(content))
print(len(content))
r = dll.ocr(list(content), len(content))

print(r)

'''
\xff \xd8  \xff  \xe0  \x00  \x10  JFIF        \x00  \x01\x01\x00\x00\x01\x00\x01\x00\x00\xff
255   216  255    224  0     16    74,70,73,70   0    1,1,0,0,1,0,1,0,0,255,219,0,67,0,8,6,6,7,6
'''

bytes([255,16])
list("\xff\xd8")