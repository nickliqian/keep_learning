context = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
}

# 字典格式化打印
print('--字典格式化打印--')
[print(i) for i in context.items()]

# 字典扩充/更新
extra_context = {'a': 10, 'e': 5}
context.update(extra_context or {})
print('--字典扩充/更新--')
print(context)

# 字典内嵌套的作用,多个参数同样可以被解开
print('--字典内嵌套的作用/定义,解开关键字参数--')
f = {'f': 6}
new_context = dict(f, b=1, c=2)
print(new_context)
