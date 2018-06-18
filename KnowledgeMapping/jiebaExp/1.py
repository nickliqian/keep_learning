# encoding=utf-8
import jieba


with open("./xiyouji.txt", "r", errors='ignore') as f:
    content = f.read()

seg_list = jieba.cut(content, cut_all=False)

item = {}
for i in seg_list:
    if item.get(i, None):
        item[i] += 1
    else:
        item[i] = 1

r = sorted(item.items(),key = lambda x:x[1],reverse = True)

ignore_dict = (" ", ",", "\n", "。", "：", "“", "”", "！", "？", "，", "、", "─", "；")

with open("./result.txt", "w", encoding="utf-8") as f:
    j = 1
    for i in r:
        if i[0] not in ignore_dict:
            f.write("{}-{}-{}\n".format(j, i[0], i[1]))
            j += 1
