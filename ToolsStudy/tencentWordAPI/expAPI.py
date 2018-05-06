import requests
import os
import time
import random
from Signature import signature


# 请求API
def req_api():
    # 请求方式
    method = "GET"
    url = "https://cvm.api.qcloud.com/v2/index.php"
    # 生成通用参数
    action = "DescribeInstances"
    nonce = str(random.randint(1, 65535))
    region = "ap-guangzhou"
    signature_method = "HmacSHA256"
    timestamp = str(int(time.time()))
    instance_ids = "ins-9srcrts2"
    # 密钥
    secret_key = os.getenv("TX_SecretKey")
    secret_id = os.getenv("TX_SecretId")

    params = {
        "Action": action,
        "Nonce": nonce,
        "Region": region,
        "SecretId": secret_id,
        "SignatureMethod": signature_method,
        "Timestamp": timestamp,
        "InstanceIds.0": instance_ids,
    }

    sign = signature(url=url, method=method, params=params, secret_key=secret_key)
    print(sign)

    # 需要保留验证方法SignatureMethod
    params["Signature"] = sign
    response = requests.get(url, params=params, verify=False, timeout=6)
    print(response.text)


if __name__ == '__main__':
    req_api()
