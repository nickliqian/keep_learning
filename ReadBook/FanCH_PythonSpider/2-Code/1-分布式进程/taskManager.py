import random
import time
import queue as Queue
from multiprocessing.managers import BaseManager

# 新建队列
task_queue = Queue.Queue()
result_queue = Queue.Queue()

# 在网络上注册队列
class Queuemanager(BaseManager):
    pass
Queuemanager.register("get_task_queue", callable=lambda:task_queue)
Queuemanager.register("get_result_queue", callable=lambda:result_queue)

# 绑定端口，设置验证口令（对象初始化）
manager = Queuemanager(address=("", 8001), authkey=b"test")

# 启动管理，监听信息通道
manager.start()

# 通过管理实例的方法获得通过网络访问Queue对象
task = manager.get_task_queue()
result = manager.get_result_queue()

# 添加任务到task队列
for url in ["image_url_" + str(i) for i in range(10)]:
    print("put task {} ...".format(url))
    task.put(url)

try:
    # 获取result队列数据, 如果为空就阻塞30秒
    print("get result ...")
    for i in range(10):
        print("result is {}".format(result.get(timeout=30)))
finally:
    # 关闭管理
    manager.shutdown()
    print("关闭管理器监听")






