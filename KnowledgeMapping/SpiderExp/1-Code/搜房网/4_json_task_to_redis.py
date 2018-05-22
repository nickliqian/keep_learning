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


def save_to_redis():
    r_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    r_conn = redis.Redis(connection_pool=r_pool)

    with open("./streets.json", "r") as f:
        data = json.load(f)

    for city in data:
        for street in city:
            r_conn.sadd("soufang:task", str(street))
            print(street)
            # return


if __name__ == '__main__':
    save_to_redis()