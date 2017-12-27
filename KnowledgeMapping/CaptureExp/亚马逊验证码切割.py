from PIL import Image

name = '0.png'
im = Image.open(name)

 # 转换像素
im = im.convert("P")

# 打印像素直方图,获得最多的像素
his = im.histogram()
values = {}
for i in range(0, 256):
    values[i] = his[i]
temp = sorted(values.items(), key=lambda x: x[1], reverse=True)
# print('下面是最多的三种像素值')
# for j, k in temp[:20]:
# 	print(j, k)
# print('--------------------')


# 生成纯色新图像 255 白色
im2 = Image.new("P", im.size, 255)
for y in range(im.size[1]):
    for x in range(im.size[0]):
        pix = im.getpixel((x, y))
        if pix == 0:
            im2.putpixel((x, y), 0)
im2.save('test2.gif')


# 原始图像转为P模式
im3=im.convert('P')
his = im3.histogram()
print(his)
# 原始图像转为L模式
im3=im.convert('L')
his = im3.histogram()
print(his)
# P模式图像转为L模式图像
im3=im.convert('P')
im3=im3.convert('L')
his = im3.histogram()
print(his)
threshold = 40
table = []
for i in range(256):
	if i < threshold:
		table.append(0)
	else:
		table.append(255)
im3 = im3.point(table,'1')
his = im3.histogram()
print(his)

im3.save('test3.gif')



inletter = False
foundletter = False
start = 0
end = 0
letters = []
for x in range(im2.size[0]):
    for y in range(im2.size[1]):
        pix = im3.getpixel((x, y))
        if pix != 255:
            inletter = True
    if foundletter == False and inletter == True:
        foundletter = True
        start = x

    if foundletter == True and inletter == False:
        foundletter = False
        end = x
        letters.append((start, end))

    inletter = False

print(letters)