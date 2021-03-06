from ctypes import *
from io import BytesIO
import chardet

# dll = CDLL("ocr.dll")
dll = windll.LoadLibrary("ocr.dll")
dll.init()
ocr = dll.ocr
ocr.argtypes = [c_char_p, c_int]
ocr.restype = c_char_p
with open("./upwj.bmp", "rb") as f:
    content = f.read()
content = content
print(list(content))
print(type(content))
print(len(content))
r = dll.ocr(content, len(content))

print(chardet.detect(r))

print(r)
print(r.decode("gbk"))
print(r.decode("utf-8"))
# print(r.encode().decode("utf-8"))
# print(r.encode().decode("gbk"))
# print(r.encode().decode("gb18030"))

'''
\xff \xd8  \xff  \xe0  \x00  \x10  JFIF        \x00  \x01\x01\x00\x00\x01\x00\x01\x00\x00\xff
255   216  255    224  0     16    74,70,73,70   0    1,1,0,0,1,0,1,0,0,255,219,0,67,0,8,6,6,7,6
'''