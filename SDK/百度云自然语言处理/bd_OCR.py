from aip import AipOcr


def get_file_content(filePath):
    """
    读取图片
    :param filePath:
    :return:
    """
    with open(filePath, 'rb') as fp:
        return fp.read()


with open("/home/nick/Desktop/key/bd_ocr_key") as f:
    content = f.read()
APP_ID, API_KEY, SECRET_KEY = eval(content)
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

image = get_file_content('/home/nick/Desktop/123.png')
result = client.basicGeneral(image)

string = ""
for i in result["words_result"]:
    string += i["words"]

with open("/home/nick/Desktop/key/cre_key_word") as f:
    content = f.read()
key_word = eval(content)

string = string.replace(key_word[0], "")\
    .replace(key_word[1], "")\
    .replace(key_word[2], "")\
    .replace(key_word[3], "")\
    .replace(key_word[4], "")\
    .replace(key_word[5], "")\
    .replace(key_word[6], "")


print(string.split(":")[1:])


# """ 如果有可选参数 """
# options = {}
# options["language_type"] = "CHN_ENG"
# options["detect_direction"] = "true"
# options["detect_language"] = "true"
# options["probability"] = "true"
#
# """ 带参数调用通用文字识别, 图片参数为本地图片 """
# client.basicGeneral(image, options)

# url = "https//www.x.com/sample.jpg"
#
# """ 调用通用文字识别, 图片参数为远程url图片 """
# client.basicGeneralUrl(url)
#
# """ 如果有可选参数 """
# options = {}
# options["language_type"] = "CHN_ENG"
# options["detect_direction"] = "true"
# options["detect_language"] = "true"
# options["probability"] = "true"
#
# """ 带参数调用通用文字识别, 图片参数为远程url图片 """
# client.basicGeneralUrl(url, options)
