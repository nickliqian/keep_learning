import json
import redis


def fprint_type_len(variable):
    print(type(variable), len(variable))


def fprint_data_structure(variable):
    fprint_type_len(variable)
    if (type(variable) in [list, tuple, set]) and variable:
        fprint_data_structure(variable[0])
    elif isinstance(variable, dict) and variable:
        fprint_data_structure(variable[list(variable.keys())[0]])
    else:
        pass


def txt_to_json_map():
    with open("./all_code.txt", "r") as f:
        content = f.readlines()
    items = []
    for c in content:
        item = eval(c.strip())
        items.append(item)
    with open("./mapJson.json", "w") as f:
        f.write(json.dumps(items, ensure_ascii=False))


def restrict_data_code():
    with open("./city_word_code.json", "r") as f:
        data2 = json.load(f)
    words = dict()
    for word in data2:
        words[word["name"]] = word["code"]
    # print(words)

    map_dict = []
    with open("./mapJson.json", "r") as f:
        data1 = json.load(f)
    for city in data1:
        for street in city:
            item = street
            item["city_word"] = words[item["city_name"]]
            map_dict.append(item)
            print(item)

    with open("./finally_map.json", "w") as f:
        f.write(json.dumps(map_dict, ensure_ascii=False))


def save_to_redis():
    r_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    r_conn = redis.Redis(connection_pool=r_pool)

    with open("./finally_map.json", "r") as f:
        data = json.load(f)

    for street in data:
        r_conn.sadd("tencentHouse:task", str(street))
        print(street)


if __name__ == '__main__':
    save_to_redis()
    # txt_to_json_map()
    # restrict_data_code()