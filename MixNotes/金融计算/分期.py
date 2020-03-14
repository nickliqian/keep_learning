
earn = 0.05/365


print("【3期】")
base = 3463.26
cycle = 3
pay_each = 91.05

total = 0
for i in range(cycle + 1):
    owe = (cycle - i) * base
    # print(owe)
    get_more = owe * earn * 30
    # print(get_more)
    total += get_more

print(total, pay_each*cycle, total - pay_each*cycle)
print(base*cycle)

print("【6期】")
base = 1141.97
cycle = 6
pay_each = 49.18

total = 0
for i in range(cycle + 1):
    owe = (cycle - i) * base
    # print(owe)
    get_more = owe * earn * 30
    # print(get_more)
    total += get_more

print(total, pay_each*cycle, total - pay_each*cycle)
print(base*cycle)

print("【10期】")
base = 1082.48
cycle = 10
pay_each = 70.82

total = 0
for i in range(cycle + 1):
    owe = (cycle - i) * base
    # print(owe)
    get_more = owe * earn * 30
    # print(get_more)
    total += get_more

print(total, pay_each*cycle, total - pay_each*cycle)
print(base*cycle)

print("【12期】")
base = 909.82
cycle = 12
pay_each = 66.77

total = 0
for i in range(cycle + 1):
    owe = (cycle - i) * base
    # print(owe)
    get_more = owe * earn * 30
    # print(get_more)
    total += get_more

print(total, pay_each*cycle, total - pay_each*cycle)
print(base*cycle)
