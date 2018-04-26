import os


def split_number(filename, parents_dir):
    print("File name is {}".format(filename))
    with open(filename, "r") as f:
        results = f.readlines()

    for result in results:
        print(result.strip().split(",")[0])


def get_files_name(dir):
    all_filename = os.listdir(dir)
    return all_filename


if __name__ == '__main__':
    parents_dir = "/home/nick/Desktop/H3-移动号码归属/"
    names = get_files_name(parents_dir)
    print("文件夹{}下共{}个文件".format(parents_dir, len(parents_dir)))
    split_number(names)