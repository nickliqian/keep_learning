#!/usr/bin/python
# -*- coding: UTF-8 -*-


import pandas as pd
import numpy as np


train = pd.read_csv('./train.csv')
test = pd.read_csv('./test.csv')

train.head(10)
train.head(10)
train.isnull().sum(axis=0)
train.isnull().sum(axis=0)

y = train['Y'] # 将训练集Survived 数据存储在y中
del train['Y'] # 删除训练集Survived数据

origin = ["年龄", "工作天数", "职业类型", "投资收入", "投资损失", "省份", "教育", "家庭角色", "婚姻状况", "教育时间", "民族", "工作情况", "性别"]
target = ["age", "work_days", "job", "invest_income", "invest_loss", "province", "education", "home_role", "marital_status", "education_time", "nation", "work_type", "gender"]
rename_dict = dict()
for i in range(len(origin)):
    rename_dict[origin[i]] = target[i]
train.rename(columns=rename_dict, inplace = True)


train['gender'] = train['gender'].map( {'女': 0, '男': 1} ).astype(int)

class_mapping_job = {label:idx for idx,label in enumerate(set(train['job']))}
train['job'] = train['job'].map(class_mapping_job).astype(int)


class_mapping_education = {label:idx for idx,label in enumerate(set(train['education']))}
train['education'] = train['education'].map(class_mapping_education).astype(int)


for dataset in train:
    dataset['province'] = dataset['province'].replace("省份", "")
train.head()