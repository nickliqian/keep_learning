import json
import csv
import os
import re

#
# with open("./bd.csv", "r", encoding="utf-8") as f:
#     a = json.loads(f.readline())
#     print(a)


# filename = "./bd.csv"
filename = os.path.join(r"C:\Users\李谦\Desktop", "bdW.csv")

with open(filename, mode="r", newline="", encoding="utf-8") as csvfile:
    spamreader = csv.reader(csvfile)
    i = 0
    error_list = []
    items = []
    for row in spamreader:
        if i == 0:
            pass
        else:
            try:
                data = row[4]
                new_data = data.replace("	", "").replace("\\", "")

                # 清理 javascript:SLC(98761,229)
                pattern = r'"javascript:SLC\(.*?\)"'
                new_data = re.sub(pattern, "", new_data)

                # pattern = r':\s("").+?(""),'
                # new_data = re.sub(pattern, "<test>", new_data)

                item = json.loads(new_data)
                items.append(item)
            except json.decoder.JSONDecodeError:
                error_list.append(row[0])
        i += 1
    print("json解析报错的id为：{}， 总数为{}".format(error_list, len(error_list)))

    # key_list = ['lastmod', 'cardNum', 'duty', 'courtName', 'focusNumber', '_version', '_select_time', 'publishDate',
    #             'regDate', 'sexy', 'performance', 'loc', 'SiteId', 'publishDateStamp', 'gistId', 'unperformPart',
    #             'partyTypeName', '_update_time', 'caseCode', 'changefreq', 'priority', 'StdStg', 'age', 'areaName',
    #             'performedPart', 'gistUnit', 'cambrian_appid', 'StdStl', 'type', 'sitelink', 'disruptTypeName',
    #             'businessEntity', 'iname']
    #
    # with open("new_file.csv", 'w', newline="", encoding="utf-8") as out_file:
    #     csv_writer = csv.writer(out_file)
    #     # 写入keys，第一列标题
    #     csv_writer.writerow(key_list)
    #
    #     for item in items:
    #         # key_list 有序列表
    #         # key_list顺 -> item.get(x, "")
    #         # 按照key_list的顺序分别取出item中对应key的value，如果没有则置为""
    #         iter_item = map(lambda x: item.get(x, ""), key_list)
    #         csv_writer.writerow(iter_item)



# with open('bd.csv', mode='r', newline='') as csvfile:
#     spamreader = csv.reader(csvfile)
#     i = 0
#     data = list(spamreader)[2][4]
#     print(data)
#     print(type(data))
#     print()
#     print()
#     print()
#     print()
#     data = json.loads(data)
#     print(type(data))