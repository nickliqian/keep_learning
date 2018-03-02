#!/bin/bash
source /etc/profile

service redis-server status > /dev/null
redis_status=$(echo $?)
if [[ $redis_status = "0" ]]
then
echo "redis pass"
else
echo "redis fail"
service redis-server start
echo "run redis server"
fi

service mysql status > /dev/null
mysql_status=$(echo $?)
if [[ $mysql_status = "0" ]]
then
echo "mysql pass"
else
echo "mysql fail"
echo "run mysql server"
service mysql start
fi


#!/bin/bash
source /etc/profile

lsof -i:6379 > /dev/null
redis_status=$(echo $?)
if [[ $redis_status = "0" ]]
then
echo "redis pass"
else
echo "redis fail"
/home/nick/installed/redis/src/redis-server /home/nick/installed/redis/redis.conf
echo "run redis server"
fi

service mysql status > /dev/null
mysql_status=$(echo $?)
if [[ $mysql_status = "0" ]]
then
echo "mysql pass"
else
echo "mysql fail"
echo "run mysql server"
service mysql start
fi