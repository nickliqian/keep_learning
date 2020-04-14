import time


path = "/Users/nick/Downloads/xinghe_modeling.sql"

with open(path, "r") as f:
    i = 0
    line = f.readline()
    while line:
        line = f.readline()
        print(i, type(line), line)
        i += 1


# with open("/Users/nick/Downloads/new.sql", "w") as f1:
#     a = input("pls input")
#     for i in range(8000):
#         s = time.time()
#         with open(path, "r") as f2:
#             for line in f2.readlines():
#                 f1.write(line)
#         e = time.time()
#         print(i, "=>", e-s)


# with open("/Users/nick/Downloads/new.sql", "r") as f1:
#     a = input("123")
#     s = list(f1.readlines())
#     a = input("123")

