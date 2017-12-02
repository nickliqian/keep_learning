import base64
import string


base64_charset = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'


def decode_b64str(base64_str):

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


bs = 'UzpAswnfyFLFIbg1OV0HbZ9g+k8NipTZLQJTDCn//8+D7kkQJ2oAnBDrmdVn5JElu6z8HFikEw+QnHDJ4w58AbT5q7n/Ls0h0CfvZmpO42yOEEUPoQ'


print(decode_b64str(bs))
print(decode_b64str(bs)[3])

print(type(decode_b64str(bs)))

