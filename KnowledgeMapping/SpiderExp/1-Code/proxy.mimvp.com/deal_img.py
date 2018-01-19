from PIL import Image
import os


def two_value(threshold = 140):
    # 二值化
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table


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


def cron_img(lettersx, im2, name):
    name = name.replace(".png", "")
    name = [i for i in name]

    for i in range(len(lettersx)):
        region = (lettersx[i][0], 2, lettersx[i][1], 25)
        newim = im2.crop(region)
        newim.save("./train/" + name[i] + ".png")


def main():
    # 打开图像
    dir = "./img/"

    name_list = os.listdir(dir)

    for name in name_list:

        im = Image.open(dir+name)

        # 使用L模式灰度化
        im = im.convert('L')

        # 二值化
        table = two_value()
        im2 = im.point(table, '1')

        # 得到分割坐标
        lettersx = get_cron_loction(im2)

        # 分割图像
        cron_img(lettersx, im2, name)


if __name__ == '__main__':
    main()