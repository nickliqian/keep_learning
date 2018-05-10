import re
import json


filepath = "/home/nick/Desktop/信用数据采集/"


def clean_1():
    with open(filepath+"crawl.log", "r") as f:
        content = f.readlines()


    error_list = set()

    j = 0
    for i in content:

        i = re.findall(r"(http://.*?htm)", i)[0]

        error_list.add(i)

        # error_list.append(i)

        # print(i)
        j += 1

    print(j)
    print(len(error_list))

    with open(filepath + "moreTask", "w") as f:
        for k in error_list:
            f.write(k + "\n")


def clean_2():
    with open(filepath + "moreTask", "r") as f:
        content = f.readlines()

    error_list = set()
    p = 0
    for i in content:
        if "-" in i:
            i = i.split("-")[0]+".htm"
            error_list.add(i)
            print(i)
            p += 1
        else:
            error_list.add(i)
            print(i)
            p += 1
    with open(filepath + "qishun_task", "w") as f:
        for k in error_list:
            f.write(k.strip() + "\n")

    print(p)


def deal_1():
    area_dict, industry_dict = map_dict()

    with open(filepath + "qishun_task", "r") as f:
        content = f.readlines()

    area_industry = []
    for c in content:

        origin = c

        a = c.strip().split(".com/")[1]

        lis = a.split("/")
        area = lis[0]
        industry = "/" + "/".join(lis[1:])

        # print(area, industry, origin.strip())

        try:
            area_industry.append({"area": area_dict[area], "industry": industry_dict[industry], "origin": origin.strip()})
        except Exception:
            print(origin.strip())
            pass
    # print(area_industry)

    # for obj in area_industry:
    #     print(obj)


def map_dict():
    with open("./a地域列表.json", "r") as f:
        content = json.load(f)
    area_dict = dict()
    for c in content:
        area_dict[c["href"]] = c["name"]
    # print(area_dict)

    with open("./d所有行业列表.json", "r") as f:
        content = json.load(f)
    industry_dict = dict()
    for c in content:
        industry_dict[c["href"]] = c["name"]
    # print(industry_dict)

    return area_dict, industry_dict


if __name__ == '__main__':
    deal_1()