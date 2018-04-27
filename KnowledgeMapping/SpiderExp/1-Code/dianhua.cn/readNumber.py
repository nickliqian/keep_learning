import os
import redis


# 获取指定文件夹文件列表
def get_files_name(dir):
    all_filename = os.listdir(dir)
    return all_filename


# 从文件中提取出号码前缀
def split_number(filename, parents_dir):
    print("File name is <{}>".format(filename))
    # 读取文件
    with open(os.path.join(parents_dir, filename), "r") as f:
        results = f.readlines()

    # 逐行读取文件
    for result in results:
        num = result.strip().split(",")[0]
        if len(num) == 7:
            r_conn.sadd("telephone_task", num)
        else:
            print(num)


if __name__ == '__main__':

    # 连接redis
    r_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    r_conn = redis.Redis(connection_pool=r_pool)

    # main_dir = "/home/nick/Desktop/H3-移动号码归属/"
    main_dir = "/home/watson/dc45/telephone_number/bd_dhb/H3-移动号码归属"
    # 获取所有文件名称 list
    files = get_files_name(main_dir)
    print("文件夹<{}>下共<{}>个文件".format(main_dir, len(files)))
    # 把每一个文件传入函数提取出电话号码前缀，第一行不要
    for file in files:
        split_number(file, main_dir)
