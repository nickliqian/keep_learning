from PIL import Image
import numpy as np

# 打开图像
name = '0.png'
im = Image.open(name)
# 使用L模式灰度化
im = im.convert('L')
im = im.convert('1')
# 旋转15度
im2 = im.rotate(15)
im2.save('旋转' + name)

# 生成图像像素值矩阵
im_array = np.array(im)
print(im_array)

# 旋转/对换操作
# import Image
# im = Image.open("j.jpg")
# im.rotate(45) #逆时针旋转 45 度角。
# im.transpose(Image.FLIP_LEFT_RIGHT) #左右对换。
# im.transpose(Image.FLIP_TOP_BOTTOM) #上下对换。
# im.transpose(Image.ROTATE_90) #旋转 90 度角。
# im.transpose(Image.ROTATE_180) #旋转 180 度角。
# im.transpose(Image.ROTATE_270) #旋转 270 度角。


# 获取图片尺寸
size = im.size

# 二值化
threshold = 140
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(255)
im2 = im2.point(table, '1')

# 转置
his = im2.histogram()
values = {}
for i in range(0, 256):
    values[i] = his[i]
for i in values.items():
    print(i)

# 去噪
im2 = im
for i in range(im.size[1]):
    for j in range(im.size[0]):
        # pos=(j,i)
        # print(pos)
        if i == 0 or j == 0 or i == im.size[1] - 1 or j == im.size[0] - 1:
            im2.putpixel((j, i), 255)  # 图片最外面一周都换成白点
        elif im.getpixel((j, i)) != im.getpixel((j - 1, i)) and im.getpixel((j, i)) != im.getpixel(
                (j + 1, i)) and im.getpixel((j, i - 1)) != im.getpixel((j, i)) and im.getpixel(
            (j, i + 1)) != im.getpixel((j, i)):
            im2.putpixel((j, i), 255)  # 不连续点也都换成白点

im2.save('q' + name)

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
        if pix != 255:
            inletter = True  # 如果不是白色，这说明已经开始接触到数字了
    # 如果接触到了数字，就标记这一行为start
    if foundletter == False and inletter == True:
        foundletter = True
        start = x  # 数字的起始坐标
    # 如果这一行没有接触到数字但是之前有接触到过数字，就记录这上一行的位置
    if foundletter == True and inletter == False:
        foundletter = False
        end = x - 1  # 数字的结束位置
        lettersx.append((start, end))
    inletter = False
print(lettersx)

inletter = False
foundletter = False
start = 0
end = 0
lettersy = []  # 用来记录每个数字的起始位置
# 这两个循环就是遍历每个像素点
# x,y w,h  x = w, y = h
for y in range(im2.size[1]):
    for x in range(im2.size[0]):
        # 获取每个点的值（0，255）
        pix = im2.getpixel((x, y))
        # 当遇到黑色的时候，记录一下，说明以及接触到了数字
        if pix != 255:
            inletter = True  # 如果不是白色，这说明已经开始接触到数字了
    # 如果接触到了数字，就标记这一行为start
    if foundletter == False and inletter == True:
        foundletter = True
        start = y  # 数字的起始坐标lettersy
    # 如果这一行没有接触到数字但是之前有接触到过数字，就记录这上一行的位置
    if foundletter == True and inletter == False:
        foundletter = False
        end = y - 1  # 数字的结束位置
        lettersy.append((start, end))
    inletter = False
print(lettersy)

i = 1
for i in range(4):
    region = (lettersx[i][0], 2, lettersx[i][1], 16)
    newim = im2.crop(region)
    newim.save('part' + str(i + 1) + '-' + name)

# 遍历每一行（按高度的最大值） H30 i = 0~29
for i in range(im.size[1]):
    temp = []
    # 遍历每一列 W100 i = 0~99
    for j in range(im.size[0]):
        pos = (j, i)  # 构造一个元组
        col = im.getpixel(pos)  # 获取pos位置的颜色值
        # 获取某坐标的点的颜色，黑色为0，白色为255，为了显示规程，把它转变成1了
        if col == 255:
            col = 1
        temp.append(col)
    print(temp)
