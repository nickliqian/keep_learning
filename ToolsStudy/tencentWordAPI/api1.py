import requests
import os
import time
import random
from Signature import signature


# 请求API
def req_api():
    # 请求方式
    method = "GET"
    url = "https://wenzhi.api.qcloud.com/v2/index.php"
    # 生成通用参数
    action = "TextSentiment"
    nonce = str(random.randint(1, 65535))
    region = "sz"
    signature_method = "HmacSHA256"
    timestamp = str(int(time.time()))
    # 密钥
    secret_key = os.getenv("TX_SecretKey")
    secret_id = os.getenv("TX_SecretId")
    # 定制参数
    content = "双万兆服务器就是好，只是内存小点"

    params = {
        "Action": action,
        "Nonce": nonce,
        "Region": region,
        "SecretId": secret_id,
        "SignatureMethod": signature_method,
        "Timestamp": timestamp,
        "content": content,
    }

    sign = signature(url=url, method=method, params=params, secret_key=secret_key)

    # 需要保留验证方法 SignatureMethod
    params["Signature"] = sign
    response = requests.get(url, params=params, verify=False, timeout=6)
    print(response.text)


if __name__ == '__main__':
    req_api()
