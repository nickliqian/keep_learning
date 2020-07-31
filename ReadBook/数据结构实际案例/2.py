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
        """
        使用多个整型元素来储存数据，每个元素4个字节（32位）
        """
        self._size = int((max_value + 31 - 1) / 31)  # 计算需要的字节数，字节数也是数组的大小
        self.array = [0 for i in range(self._size)]  # 数组的元素都初始化为0，每个元素有32位

    @staticmethod
    def get_element_index(num):
        """
        获取该数即将储存的字节在数组中下标
        """
        return num // 31

    @staticmethod
    def get_bit_index(num):
        """
        获取该数在元素中的位下标
        """
        return num % 31

    def set(self, num):
        """
        将该数存在对应的元素的对应位置
        """
        element_index = self.get_element_index(num)
        bit_index = self.get_bit_index(num)
        self.array[element_index] = self.array[element_index] | (1 << bit_index)

    def find(self, num):
        """
        查找该数是否存在与bitmap中
        """
        element_index = self.get_element_index(num)
        bit_index = self.get_bit_index(num)
        if self.array[element_index] & (1 << bit_index):  # 1&1才是1，否则0；如果为1 ，说明数值存在
            return True
        return False

    def count_one(self):
        """
        统计bitmap中数据的个数
        """
        count = 0
        for n in self.array:
            while n > 0:
                n = n & (n - 1)
                count += 1
        return count


def main():
    array_list = [30, 32, 5, 45, 2, 78, 35, 67, 90, 879, 0, 340, 123, 46, 1, 5]
    # 根据最大数的值创建BitMap对象
    bitmap = BitMap(max_value=max(array_list))

    # 将数据逐个存入bitmap
    for num in array_list:
        bitmap.set(num)

    # 查询数据是否存在于bitmap中
    results = []
    for i in range(max(array_list) + 1):
        if bitmap.find(i):
            results.append(i)
    print(results)


if __name__ == '__main__':
    main()
