from OpenSSL.crypto import PKey
from OpenSSL.crypto import TYPE_RSA, FILETYPE_PEM
from OpenSSL.crypto import dump_privatekey, dump_publickey

"""
产生密钥对
利用PKey对象可以方便快速产生密钥对，然后dump_函数可以把PKey对象转成字节码方便写入文件，或者进行base64编码后进行网络传输。
"""

pk = PKey()
print(pk)
pk.generate_key(TYPE_RSA, 1024)
dpub = dump_publickey(FILETYPE_PEM, pk)
print(dpub)
dpri = dump_privatekey(FILETYPE_PEM, pk)
print(dpri)

