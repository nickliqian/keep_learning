import re


with open("./SmartOcean.ipynb", "r", encoding="utf-8") as f:
    data = f.readlines()


with open("./newSmartOcean.ipynb", "w", encoding="utf-8") as f:
    for d in data:
        rd = re.findall(r'"\d+\s-\s\d+\\n"', d)
        if rd:
            # print("{} ==> {}".format(d, rd))
            pass
        else:
            f.write(d)

