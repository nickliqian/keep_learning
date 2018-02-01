import requests
import json
import re

url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php"

params = {
    "resource_id": "6899",
    "query": "被执行人",
    "pn": "10",
    # "rn": "5",
    # "ie": "utf-8",
    # "oe": "utf-8",
    # "format": "json",
    # "t": "1517490611700",
    # "cb": "jQuery110206295192736769775_1517490433434",
    # "_": "1517490433491"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                  "63.0.3239.108 Safari/537.36",
}

r = requests.get(url=url, headers=headers, params=params)
content = r.text

# pattern = re.compile(r"(/\*\*/jQuery.*?\()|(\);)")
# content = re.sub(pattern, "", content)

data_dict = json.loads(content, encoding="utf-8")

rows = data_dict["data"][0]["result"]
i = 1
for row in rows:
    print(str(i) + " " + row["iname"])
    # print(row["SiteId"])
    # print(row["StdStg"])  # 6899 不变 资源ID
    # print(row["StdStl"])  # 8 不变
    # print(row["loc"])
    # print("=======================")
    i += 1



# with open("./content.json", "w") as f:
#     f.write(r.text)

# print(r.text)