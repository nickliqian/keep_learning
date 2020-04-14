class Bitmap(object):
    def __init__(self,max):
        """
        确定所需数组个数
        """
        self.size = int ((max + 31 - 1) / 31)
        self.array = [0 for i in range(self.size)]

    def bitindex(self,num):
        """
        确定数组中元素的位索引
        """
        return num % 31

    def set_1(self,num):
        """
        将元素所在的位置1
        """
        elemindex = num / 31
        byteindex = self.bitindex(num)
        ele = self.array[elemindex]
        self.array[elemindex] = ele | (1 << byteindex)

    def test_1(self,i):
        """
        检测元素存在的位置
        """
        elemindex = i / 31
        byteindex = self.bitindex(i)
        if self.array[elemindex] & (1 << byteindex):
            return True
        return False


if __name__ == '__main__':
    Max = ord('z')
    suffle_array = [x for x in 'qwelmfg']
    result = []
    bitmap = Bitmap(Max)
    for c in suffle_array:
        bitmap.set_1(ord(c))
    for i in range(Max+1):
        if bitmap.test_1(i):
            result.append(chr(i))
    print('原始数组为:    %s' % suffle_array)
    print('排序后的数组为: %s' % result)

