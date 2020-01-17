import requests
import os


hrefs = """
http://www.supersunsir.com/wp-content/uploads/2019/08/wp_01-1024x288.jpg
http://www.supersunsir.com/wp-content/uploads/2019/08/wp_01.jpg
http://www.supersunsir.com/wp-content/uploads/2019/08/wp_01.jpg
http://www.supersunsir.com/wp-content/uploads/2019/08/wp_02.jpg
http://www.supersunsir.com/wp-content/uploads/2019/08/wp_03.jpg
http://www.supersunsir.com/wp-content/uploads/2019/08/wp_04.png
http://www.supersunsir.com/wp-content/uploads/2019/08/wp_05.jpg
http://www.supersunsir.com/wp-content/uploads/2019/08/wp_06.jpg
http://www.supersunsir.com/wp-content/uploads/2019/08/wp_07.jpg
http://www.supersunsir.com/wp-content/uploads/2019/08/wp_08.jpg
http://www.supersunsir.com/wp-content/uploads/2019/08/wp_09.jpg
http://www.supersunsir.com/wp-content/uploads/2019/08/wp_10.jpg
http://www.supersunsir.com/wp-content/uploads/2019/08/wp_11.jpg
http://www.supersunsir.com/wp-content/uploads/2019/08/wp_12.jpg
http://www.supersunsir.com/wp-content/uploads/2019/08/wp_14.jpg
http://www.supersunsir.com/wp-content/uploads/2019/08/wp_15.jpg
http://www.supersunsir.com/wp-content/uploads/2019/08/wp_16.jpg
http://www.supersunsir.com/wp-content/uploads/2019/08/wp_17.jpg
http://www.supersunsir.com/wp-content/uploads/2019/08/wp_18.png
"""
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
}

h_list = hrefs.split("\n")
for index, h in enumerate(h_list):
    h = h.strip()
    if not h:
        pass
    else:
        print("\n【Start】{}".format(h))
        while True:
            try:
                response = requests.get(url=h, headers=headers, timeout=10, stream=True)
                break
            except Exception as e:
                print("【{}】 {}".format(type(e), e))

        content_size = int(response.headers["content-length"])
        # print("【Content Size】: {}".format(content_size))
        chunk_size = 1024
        if response.status_code == 200:
            print("【文件大小】：{:.2f}MB".format(content_size / chunk_size / 1024))
            name = h.split("/")[-1]
            print("【文件名称】：{}".format(name))
            with open(os.path.join(r"C:\Users\nick\Pictures\壁纸\shuangping", name), "wb") as f:
                f.flush()
                size = 0

                for chunk in response.iter_content(chunk_size=chunk_size):

                    if chunk:
                        f.write(chunk)
                        f.flush()

                        size += len(chunk)
                        bar = ">" * int(size * 50 / content_size)
                        num = float(size / content_size * 100)
                        print("\r【下载进度】：{}{:.2f}%".format(bar, num), end="")
        else:
            raise Exception("【状态码错误】 期望是200，得到{}".format(response.status_code))


