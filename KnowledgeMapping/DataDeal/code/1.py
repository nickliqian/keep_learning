from pandas import Series,DataFrame
import json


with open(r"C:\Users\李谦\Desktop\dataDeal\hlj.csv", encoding='utf-8') as f:
    records = []
    for line in f:
        try:
            if "{}" in line:
                print("Data is empty -> {}".format(line))
            else:
                content = ("[" + line + "]").replace('""', '"')\
                                                    .replace('"["', '["').replace('"]"', '"]')\
                                                    .replace('"{"', '{"').replace('"}"', '"}').replace('\n', '')

                t = content.split('"},')
                # print("分割长度：{} {}".format(len(t), content))

                s = t[0] + '"},' + '"' + t[1][:-1] + '"' + ']'

                # print(s)
                data = json.loads(s)
                records.append(data[3])
        except Exception as e:
            print("异常1 {}".format(line))
            raise e

print(len(records))
print(type(records))
hlj = DataFrame(records)
print(hlj)
hlj.to_csv('hlj_v.csv')

