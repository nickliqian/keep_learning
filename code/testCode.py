import hashlib
import string


# 按base64规则解码
def decode_b64str(base64_str):
    base64_charset = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'

    # 对每一个base64字符取下标索引，并转换为6为二进制字符串
    base64_bytes = ['{:0>6}'.format(str(bin(base64_charset.index(s))).replace('0b', '')) for s in base64_str if
                    s != '=']
    resp = bytearray()
    nums = len(base64_bytes) // 4
    remain = len(base64_bytes) % 4
    integral_part = base64_bytes[0:4 * nums]

    while integral_part:
        # 取4个6位base64字符，作为3个字节
        tmp_unit = ''.join(integral_part[0:4])
        tmp_unit = [int(tmp_unit[x: x + 8], 2) for x in [0, 8, 16]]
        for i in tmp_unit:
            resp.append(i)
        integral_part = integral_part[4:]

    if remain:
        remain_part = ''.join(base64_bytes[nums * 4:])
        tmp_unit = [int(remain_part[i * 8:(i + 1) * 8], 2) for i in range(remain - 1)]
        for i in tmp_unit:
            resp.append(i)

    return resp


# 字符串按md5算法编码
def md5(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()


def decode_hash(url_hash):
    pswd = "jtbEijfprLaGbJ5lVW5AcR5nVAOjKZ44"
    pswd = md5(pswd)
    q = 4
    o = md5(pswd[0:16])
    n = md5(pswd[16:])
    l = url_hash[0:4]

    c = o + md5(o+l)

    url_hash = url_hash[4:]
    k = decode_b64str(url_hash)

    h = []
    for g in range(256):
        h.append(g)

    b = []
    for g in range(256):
        i = c[g % len(c)]
        b.append(ord(i))

    f = 0
    for g in range(256):
        f = (f + h[g] + b[g]) % 256
        h[g], h[f] = h[f], h[g]

    t = ""
    k = list(k)

    f = 0
    p = 0
    t = ''
    for g in range(len(k)):
        p = (p + 1) % 256
        f = (f + h[p]) % 256
        h[p], h[f] = h[f], h[p]

        ord1 = k[g]
        ord2 = (h[(h[p] + h[f]) % 256])
        ord3 = ord1 ^ ord2
        t += chr(ord3)
    print(t)


if __name__ == "__main__":
    url_hash = '41bbtgMOXof0N/aT0C29NWd3vBi6UBqPVapbhT5O34nnFKcdvXAN6r7ILrw66T2zuuH6QHHmBT' \
               '6a0Rc+FcDwXIigVODe4vOYYeyL2vsBC28OZ00sZJ7W7g'
    url = decode_hash(url_hash)

