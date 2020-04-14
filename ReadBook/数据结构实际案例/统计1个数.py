def countOne(n):
    count = 0  # 用来计数
    while n > 0:
        n = n & (n - 1)
        count += 1
    return count


if __name__ == "__main__":
    print(countOne(7))
    print(countOne(8))