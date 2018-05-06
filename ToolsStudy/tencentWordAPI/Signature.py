import hashlib
import hmac
import base64


# HmacSHA256 加密算法
def Hmac_SHA256(string, key):
    string_b = bytes(string, encoding="utf-8")
    key_b = bytes(key, encoding="utf-8")
    signature = base64.b64encode(hmac.new(key=key_b, msg=string_b, digestmod=hashlib.sha256).digest())
    return signature.decode("utf-8")


# 请求API
def signature(url, method, params, secret_key):
    url = url.replace("https://", "")
    src_string = method + url + "?" + "&".join(["{}={}".format(p, params[p]) for p in sorted(params)])
    # 使用hamxsha256+base64生成签名
    sign_string = Hmac_SHA256(src_string, secret_key)
    return sign_string


if __name__ == '__main__':
    m_url = "cvm.api.qcloud.com/v2/index.php"
    m_method = "GET"
    m_params = {
        "Action": "DescribeInstances",
        "Nonce": "11886",
        "Region": "ap-guangzhou",
        "SecretId": "AKIDz8krbsJ5yKBZQpn74WFkmLPx3gnPhESA",
        "SignatureMethod": "HmacSHA256",
        "Timestamp": "1465185768",
        "InstanceIds.0": "ins-09dx96dg"
    }
    m_secret_key = "Gu5t9xGARNpq86cd98joQYCN3Cozk1qA"
    sign = signature(m_url, m_method, m_params, m_secret_key)
    assert sign == "0EEm/HtGRr/VJXTAD9tYMth1Bzm3lLHz5RCDv1GdM8s="


