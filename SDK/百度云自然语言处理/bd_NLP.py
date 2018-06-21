#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
url: http://ai.baidu.com/docs#/NLP-Python-SDK/8dece6d6
"""
from aip import AipNlp
import os


# 调用词法分析
def lexer(text):
    return client.lexer(text)


# 调用词法分析（定制版）
def lexer_custom(text):
    return client.lexerCustom(text)


# 调用依存句法分析 options["mode"] = 1
def dep_parser(text, options=None):
    try:
        if options["mode"]:
            return client.depParser(text, options)
        else:
            return client.depParser(text)
    except KeyError:
        return {"message": "options参数错误"}
    except TypeError:
        return {"message": "options参数错误"}


# 调用词向量表示
def word_vec(word):
    return client.wordEmbedding(word)


# 调用DNN语言模型
def dnn_lm(text):
    return client.dnnlm(text)


# 调用情感倾向分析
def sentiment(text):
    return client.sentimentClassify(text)


if __name__ == '__main__':

    APP_ID = os.getenv("APP_ID")
    API_KEY = os.getenv("API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

    wd = "今天天气好哈"
    result = dnn_lm(wd)
    print(result)

