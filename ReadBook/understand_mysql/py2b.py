

num = 3
for i in range(1, 2**num):
    s = str(bin(i)).replace("0b", "")
    fill_zero = num - len(s)

    ss = "0" * fill_zero + s
    print(ss, "=>", i)

