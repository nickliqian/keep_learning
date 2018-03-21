import math


def get_line_a_b(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    b = (x1 * y2 - x2 * y1) / (x1 - x2)
    a = (y1 - b) / x1
    a_back = (y2 - b) / x2
    if a == a_back:
        print("y={}x+{}".format(a, b))
    else:
        print("方程无解")


def line_c(point1, point2, circle_point, r):
    x1, y1 = point1
    x2, y2 = point2
    m, n = circle_point
    b = (x1 * y2 - x2 * y1) / (x1 - x2)
    a = (y1 - b) / x1
    a_back = (y2 - b) / x2
    if a == a_back:
        print("y={}x+{}".format(a, b))
    else:
        print("方程无解")
        return 0
    xsq = (r**2+2*m-m**2-2*(b-n)-(b-n)**2)/(a**2-1)
    x = math.sqrt(xsq)
    print("x={}".format(x))
    y = a*x + b
    print("y={}".format(y))


# (x-px)^2+(y-py)^2 = r^2
def cir(x, y, r):
    pass


if __name__ == '__main__':
    line_c((1, 2), (3, 4), (5, 5), 2)


