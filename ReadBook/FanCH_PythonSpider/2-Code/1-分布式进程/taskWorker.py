import time
from multiprocessing.managers import BaseManager

class QueueManager(BaseManager):
    pass

# 注册获取Queue的方法名称
QueueManager.register("get_task_queue")
QueueManager.register("get_result_queue")

# 连接到服务器进程管理对象，保持口令正确
server_addr = "127.0.0.1"
print("Connect to server {} ...".format(server_addr))
m = QueueManager(address=(server_addr, 8001), authkey=b"test")

# 从网络连接
m.connect()

# 获取Queue对象
task = m.get_task_queue()
result = m.get_result_queue()

# 判断task队列是否为空
while not task.empty():
    # 如果task不为空则向其中取数据
    image_url = task.get(True, timeout=5)
    print("run task download {} ...".format(image_url))
    time.sleep(1)
    # 向result中回传数据
    result.put("{}--->success".format(image_url))
