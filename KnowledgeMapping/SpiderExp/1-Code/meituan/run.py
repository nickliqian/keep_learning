import requests

url = "http://www.meituan.com/chongwu/301872/"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Cookie": "uuid=19e412a95edb4baaacce.1518537746.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=161d7c83e4ab6-04b4cff7fd4a28-e323462-144000-161d7c83e4bc8; _lxsdk=161d7c83e4ab6-04b4cff7fd4a28-e323462-144000-161d7c83e4bc8; ci=1; rvct=1; iuuid=A0690053600703DE7CAED681AE9B9F376D722767FC3458382495849851B25B3D; cityname=%E5%8C%97%E4%BA%AC; __mta=148132488.1519743680545.1519786400366.1519789271704.4; _lxsdk_s=161da7fc0fa-3f8-a12-fe4%7C%7C2",
    "Host": "www.meituan.com",
    "Pragma": "no-cache",
    "Proxy-Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
}

response = requests.get(url=url, headers=headers, timeout=10)

print(response.history)

print(response.text)