
"""
float divide()
num1 int
num2 int 1
"""
def divide(num1, num2=1):
    if num2 == 0:
        raise Exception("无效操作")
    val = num1 / num2
    return val

