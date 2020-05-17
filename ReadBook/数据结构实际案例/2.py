"""
Python实现bitmap

1 << 5
0000 0001 << 5 => 0010 0000 1位移5

0000 0000 | 0010 0000 => 0010 0000
0010 0000 | 0000 0100 => 0010 0100
0010 0100 | 1000 0100 => 1010 0100

1010 0100 &
"""


class BitMap(object):
    def __init__(self, max_value):
        self._size = int((max_value + 31 - 1) / 31)  # 向上取正  确定数组大小
        self.array = [0 for i in range(self._size)]  # 初始化为0  每个0代表 一个八位二进制 0000 0000

    def get_element_index(self, num):  # 获取该数的数组下标
        return num // 31

    def get_bit_index(self, num):  # 获取该数所在数组的位下标
        return num % 31

    def set(self, num):  # 将该数所在的位置1
        element_index = self.get_element_index(num)
        bit_index = self.get_bit_index(num)
        self.array[element_index] = self.array[element_index] | (1 << bit_index)  # 当前8位写数操作
        # print(element_index, bit_index, 1 << bit_index, self.array[element_index])

    def find(self, num):  # 查找该数是否存在
        element_index = self.get_element_index(num)
        bit_index = self.get_bit_index(num)
        if self.array[element_index] & (1 << bit_index):  # 1&1才是1，否则0；如果为1 ，说明数值存在
            return True
        return False

    def count_one(self):
        count = 0  # 用来计数
        for n in self.array:
            while n > 0:
                n = n & (n - 1)
                count += 1
        return count


if __name__ == '__main__':

    array_list = [1, 5, 45, 2, 78, 35, 67, 90, 879, 0, 340, 123, 46, 1, 5]
    results = []
    bitmap = BitMap(max_value=max(array_list))
    for num in array_list:
        bitmap.set(num)

    for i in range(max(array_list) + 1):
        if bitmap.find(i):
            results.append(i)

    print(array_list)
    print(results)

    print(bitmap.count_one())

    print(bitmap.find(3))
