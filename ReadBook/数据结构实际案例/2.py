"""
Python实现bitmap
"""
class BitMap(object):
    def __init__(self, maxValue):
        self._size = int((maxValue + 31 - 1) / 31)  # 向上取正  确定数组大小
        self.array = [0 for i in range(self._size)]  # 初始化为0

    def getElemIndex(self, num):  # 获取该数的数组下标
        return num // 31

    def getBitIndex(self, num):  # 获取该数所在数组的位下标
        return num % 31

    def set(self, num):  # 将该数所在的位置1
        elemIndex = self.getElemIndex(num)
        bitIndex = self.getBitIndex(num)
        self.array[elemIndex] = self.array[elemIndex] | (1 << bitIndex)
        print(elemIndex, bitIndex, 1 << bitIndex, self.array[elemIndex])


    def find(self, num):  # 查找该数是否存在
        elemIndex = self.getElemIndex(num)
        bitIndex = self.getBitIndex(num)
        if self.array[elemIndex] & (1 << bitIndex):
            return True
        return False

    def countOne(self):
        count = 0  # 用来计数
        for n in self.array:
            while n > 0:
                n = n & (n - 1)
                count += 1
        return count


if __name__ == '__main__':

    array_list = [1, 5, 45, 2, 78, 35, 67, 90, 879, 0, 340, 123, 46, 1, 5]
    results = []
    bitmap = BitMap(maxValue=max(array_list))
    for num in array_list:
        bitmap.set(num)

    for i in range(max(array_list) + 1):
        if bitmap.find(i):
            results.append(i)

    print(array_list)
    print(results)

    print(bitmap.countOne())

