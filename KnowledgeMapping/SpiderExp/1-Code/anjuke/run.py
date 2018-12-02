import random
from io import BytesIO
import json
import re
import time
from io import StringIO

from PIL import Image
import execjs
import requests


class AJK_Slide_Captcha():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                      AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
    }

    def get_sessionId(self, captcha_url):
        resp = requests.get(captcha_url, headers=self.headers)
        sessionId = re.search('name="sessionId".*?value="(.*?)"', resp.content.decode()).group(1)
        return sessionId

    def get_responseId_bgImgUrl(self, sessionId):
        resp = requests.get(
            "https://verifycode.58.com/captcha/getV3",
            headers=self.headers,
            params={
                "callback": "callback",
                "showType": "embed",
                "sessionId": sessionId,
                "_": str(int(time.time() * 1000))
            }
        )

        captchaData = json.loads(resp.text.replace("callback(", "").replace(")", ""))
        responseId = captchaData["data"]["responseId"]
        bgImgUrl = captchaData["data"]["bgImgUrl"]
        return (responseId, bgImgUrl)

    def get_image(self, bgImgUrl):
        resp = requests.get(
            "https://verifycode.58.com" + bgImgUrl,
            headers=self.headers
        )
        with open("./cp.jpg", "wb") as f:
            f.write(resp.content)
        # req.content是二进制的字符串 传化为file 的 io对象
        f = BytesIO(resp.content)
        image = Image.open(f)
        print(image.size)
        # image.show()
        return image

    def get_position(self, image):
        # image = image.resize((284, 160))
        image = image.resize((280, 158))  # 页面上的尺寸
        image = image.convert('L')
        image.save("cp2.jpg")
        yuzhi = 150
        yuzhi2 = 40
        ll = 10
        for i in range(55, image.size[0] - 20):  # 260   range(55, 264)
            for j in range(0, image.size[1] - 20):  # 160   range(0, 140)
                flag = True
                # 如果两列像素附近的色差大于40且像素点灰度大于150，说明有可能是缺口的地方
                # 如果两列像素附近色差小于40说明不是缺口的地方
                for l in range(0, ll):   # range(0, 10)
                    # print((i, j), (i + 1, j + l))
                    # print(image.getpixel((i, j)), image.getpixel((i + 1, j + l)))
                    pixel = image.getpixel((i, j)) - image.getpixel((i + 1, j + l))
                    if pixel < yuzhi2:
                        flag = False
                    # pixel = image.getpixel((i - l, j))
                    # if pixel<yuzhi:
                    #     flag=False
                # 如果像素灰度值小于150，说明不是缺口的地方
                for l in range(0, ll):
                    # print((i, j + l))
                    pixel = image.getpixel((i, j + l))
                    if pixel < yuzhi:
                        flag = False

                if flag:
                    cropedimage = image.crop((i, j, i + 30, j + 30))
                    return i - 7

    def get_trace(self, xPos, traceTxtPath):
        with open(traceTxtPath, 'r+') as fp:
            lines = fp.readlines()
        allValueLineList = []
        for line in lines:
            if line.strip() == '':
                continue
            start = int(re.search('"(\d+)', line).group(1))
            end = int(re.search('(\d+)\,\d+\,\d+\|"', line).group(1))

            if end - start == xPos or end - start == xPos + 1 or end - start == xPos - 1:
                allValueLineList.append((end - start, line.strip().strip('"')))
        print(allValueLineList)
        lastXpos, trace = random.choice(allValueLineList)
        changeNumCnt = 0
        while changeNumCnt < 4:
            changeNumCnt += 1
            num = random.choice(range(0, 10))
            try:
                search = random.choice(re.findall('(\d+%d)\|' % num, trace))
                subSearch = str(int(search) + random.choice([1, -1]))
                line = re.sub(search, subSearch, trace)
            except:
                changeNumCnt -= 1
        return (lastXpos, trace)

    def get_fpToken(self):
        resp = requests.get(
            "https://cdata.58.com/fpToken",
            headers=self.headers,
            params={
                "callback": "callback",
            }
        )
        fpData = json.loads(resp.text.replace("callback(", "").replace(")", ""))
        fpToken = fpData["token"]
        return fpToken

    def get_jiami_data(self, responseId, fpToken, lastXpos, trace):
        jsCode = execjs.compile(open("./jiami.js", "r").read())
        jiami_data = jsCode.call("getSlideAnswer", responseId, fpToken, lastXpos, trace)
        return jiami_data

    def slove(self, jiami_data, responseId, sessionId):
        response = requests.get(
            "https://verifycode.58.com/captcha/checkV3",
            headers=self.headers,
            params={
                "data": jiami_data,
                "responseId": responseId,
                "sessionId": sessionId,
                "_": str(int(time.time() * 1000))
            }
        )
        return response.text

    def run(self):
        # step1: 在验证码页面中 获取 sessionId
        sessionId = self.get_sessionId('https://www.anjuke.com/captcha-verify/?callback=shield')
        print('step1:    sessionId->', sessionId)
        # step2: 获取 responseId 和 bgImgUrl
        (responseId, bgImgUrl) = self.get_responseId_bgImgUrl(sessionId)
        print('step2:    responseId->', responseId)
        # Step 3, Get Image
        image = self.get_image(bgImgUrl)
        print('step3:    image->', image)
        # Step 4 ,caculate position
        position = self.get_position(image)
        print('step4:    position->', position)
        # Step 5 get trace
        (lastXpos, trace) = self.get_trace(position, traceTxtPath='CaptchaTrace.txt')
        print('step5:    trace->', trace)
        # Step 6 get fpToken
        fpToken = self.get_fpToken()
        print('step6:    fpToken->', fpToken)
        # Step 7 加密data
        jiami_data = self.get_jiami_data(responseId, fpToken, lastXpos, trace)
        print('step7:    jiami_data->', jiami_data)
        # Step 8 slove
        responseText = self.slove(jiami_data, responseId, sessionId)
        print('\nstep8:    最后请求结果->', responseText)


if __name__ == '__main__':
    AJK_Slide_Captcha().run()
