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

image = get_file_content('/home/nick/Desktop/qichachagif.png')
result = client.basicGeneral(image)

print(result)
