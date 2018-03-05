#!/usr/bin/env bash
service redis-server status
echo $?
ps -ef |grep redis
lsof -i:6379

redis-server /home/nick/installed/redis/redis.conf

service mysql status
echo $?
ps -ef |grep mysql
lsof -i:3306

