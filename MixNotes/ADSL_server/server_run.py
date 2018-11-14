from flask import Flask
import redis
import os


# 初始化参数
port = 6000
redis_host = os.getenv("redis_host")
redis_password = os.getenv("redis_password")

# 连接redis
redis_pool = redis.ConnectionPool(host=redis_host, port=6379, password=redis_password, decode_responses=True)
redis_client = redis.Redis(connection_pool=redis_pool)
print("连接redis")

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(port=port)
