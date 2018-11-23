#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ruamel import yaml

data = {"age": [23, 24, 25], "sex": "男", "name": "牛皮"}
with open("test.yaml", "w", encoding='utf-8') as fs:
    yaml.dump(data, fs, Dumper=yaml.RoundTripDumper, allow_unicode=True)
