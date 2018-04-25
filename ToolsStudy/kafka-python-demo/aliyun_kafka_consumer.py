#!/usr/bin/env python
# encoding: utf-8

import ssl
import socket
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import setting
import datetime

conf = setting.kafka_setting


# 配置ssl证书
context = ssl.create_default_context()
context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.verify_mode = ssl.CERT_REQUIRED
# context.check_hostname = True
context.load_verify_locations("ca-cert")

# 创建消费者 指定消费者id 一个id消费者对同一条消息只消费一次
# 如果是一个新的消费者id则会对未消费的消息开始消费
consumer = KafkaConsumer(bootstrap_servers=conf['bootstrap_servers'],
                        group_id=conf['consumer_id1'],
                        sasl_mechanism="PLAIN",
                        ssl_context=context,
                        security_protocol='SASL_SSL',
                        api_version = (0,10),
                        sasl_plain_username=conf['sasl_plain_username'],
                        sasl_plain_password=conf['sasl_plain_password'])

print 'consumer start to consuming...'
# 消费者 订阅 指定topic 也可以订阅多个
consumer.subscribe(topics=(conf['topic_name'], ), pattern=None, listener=None)
print "time topic offset key value partition"
# 循环接收消息，无消息时堵塞
for message in consumer:
    print str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), message.topic, message.offset, message.key, message.value, message.partition
