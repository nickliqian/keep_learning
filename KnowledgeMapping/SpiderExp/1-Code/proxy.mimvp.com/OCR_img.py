import math
import os
from PIL import Image


class VectorCompare:
    # 计算矢量大小
    # 计算平方和
    def magnitude(self, concordance):
        total = 0
        for word, count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    # 计算矢量之间的 cos 值
    def relation(self, concordance1, concordance2):
        topvalue = 0

        for word, count in concordance1.items():
            if word in concordance2:
                # 计算相乘的和
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))


# 将图片转换为矢量
def buildvector(im):
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1


def get_cron_loction(im2):
    # 分割
    inletter = False
    foundletter = False
    start = 0
    end = 0
    lettersx = []  # 用来记录每个数字的起始位置
    # 这两个循环就是遍历每个像素点
    # x,y w,h  x = w, y = h
    for x in range(im2.size[0]):
        for y in range(im2.size[1]):
            # 获取每个点的值（0，255）
            pix = im2.getpixel((x, y))
            # 当遇到黑色的时候，记录一下，说明以及接触到了数字
            if pix != 1:
                inletter = True  # 如果不是白色，这说明已经开始接触到数字了
        # 如果接触到了数字，就标记这一行为start
        if foundletter == False and inletter == True:
            foundletter = True
            start = x  # 数字的起始坐标
        # 如果这一行没有接触到数字但是之前有接触到过数字，就记录这上一行的位置
        if foundletter == True and inletter == False:
            foundletter = False
            end = x  # 数字的结束位置
            lettersx.append((start, end))
        inletter = False
    print(lettersx)
    return lettersx


# 训练集
v = VectorCompare()
iconset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
imageset = []
for letter in iconset:
    for img in os.listdir('./train/%s/' % (letter)):
        temp = []
        if img.endswith(".png"):
            temp.append(buildvector(Image.open("../iconset1/%s/%s" % (letter, img))))
        imageset.append({letter: temp})

def check_img(im2):
    # 识别验证码
    letters = get_cron_loction(im2)
    count = 0
    for letter in letters:
        # (切割的起始横坐标，起始纵坐标，切割的宽度，切割的高度)
        im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))

        guess = []
        # 将切割得到的验证码小片段与每个训练片段进行比较
        for image in imageset:
            for x, y in image.items():
                if len(y) != 0:
                    guess.append((v.relation(y[0], buildvector(im3)), x))

        # 排序选出夹角最小的（即cos值最大）的向量，夹角越小则越接近重合，匹配越接近
        guess.sort(reverse=True)
        print("", guess[0])