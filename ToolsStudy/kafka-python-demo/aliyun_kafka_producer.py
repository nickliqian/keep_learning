#!/usr/bin/env python
# encoding: utf-8

import ssl
import socket
from kafka import KafkaProducer
from kafka.errors import KafkaError
import setting

conf = setting.kafka_setting

print conf

# 配置ssl证书
ssl.create_default_context()
context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.verify_mode = ssl.CERT_REQUIRED
# context.check_hostname = True
context.load_verify_locations("ca-cert")

# 创建生产者，定义相关参数
producer = KafkaProducer(bootstrap_servers=conf['bootstrap_servers'],  # kafka服务器
                         sasl_mechanism="PLAIN",  # sasl机制
                         ssl_context=context,  # 用于包装的预配置SSLContext套接字连接
                         security_protocol='SASL_SSL',  # 安全协议
                         api_version=(0, 10),  # api版本
                         retries=5,  # 重试次数
                         sasl_plain_username=conf['sasl_plain_username'],  # sasl_plain用户名
                         sasl_plain_password=conf['sasl_plain_password'],  # sasl_plain密码
                         )

# 获取指定topic的分区
partitions = producer.partitions_for(conf['topic_name'])
print 'Topic下分区: %s' % partitions

try:
    # string = raw_input("Key Word:")
    string = {'a': 90}
    if not string:
        string = "空消息"
    # 发送消息到指定topic
    future = producer.send(topic=conf['topic_name'], value="00000000000000000000000000", key=None, partition=None, timestamp_ms=None)
    # 同步获得 Future 对象的结果
    future.get()
    print 'send message succeed.'
except KafkaError, e:
    print 'send message failed.'
    print e
