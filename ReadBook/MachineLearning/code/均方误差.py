import random

array = []
for i in range(10):
    a = random.random()*10
    b = random.random()*10
    array.append((a, b))

print(array)

result = 0
for j in array:
    s = (j[0]-j[1])**2
    result += s

print(result)