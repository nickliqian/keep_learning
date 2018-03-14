# unpacking
# index提供索引数字
for index, item in enumerate(["a", "b", "c"]):
    print(index, item)

a = 1
b = 2
a, b = b, a

a, (b, c) = 1, (2, 3)

# python3可用
a, *rest = [1, 2, 3]
print("a: {}".format(a))
print("rest: {}".format(rest))

a, *middle, c = [1, 2, 3, 4]

filename = 'foobar.txt'
a = filename.rpartition('.')
print(a)
basename, __, ext = filename.rpartition('.')

print(basename)
print(ext)


four_nones = [None] * 4


print(four_nones)

attr = None
if attr:
    print("....")

if not attr:
    print("....")

if attr is None:
    print("....")

d = {"hello": "world"}

print(d.get("hello", "0"))
print(d.get("world", "0"))

if 'hello' in d:
    print(d['hello'])

a = [2, 3, 4, 5]
b = [i for i in a if i >4]
b = filter(lambda x: x>4, a)
c = [i+3 for i in a]
c = map(lambda i: i+3, a)

print(list(b))
print(list(c))















