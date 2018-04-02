job 放在一个函数中
```
import requests
def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())
```

另外一个函数从创建队列
```
from rq import Queue
from redis import Redis
from somewhere import count_words_at_url

# Tell RQ what Redis connection to use
# 创建队列
redis_conn = Redis()
q = Queue(connection=redis_conn)  # no args implies the default queue

# Delay execution of count_words_at_url('http://nvie.com')
# 作业压入队列
job = q.enqueue(count_words_at_url, 'http://nvie.com')
print job.result   # => None

# Now, wait a while, until the worker is finished
time.sleep(2)
print job.result   # => 889
```

把作业压入指定队列
```
q = Queue('low', connection=redis_conn)
q.enqueue(count_words_at_url, 'http://nvie.com')
```

启动异步处理程序
```
$ rq worker
启动默认default队列工人

$ rq worker low
启动指定名称low队列工人

```
可以使用任何队列名称，以便灵活地根据自己的场景分配工作。
一个常见的命名模式是命名后的优先级队列的（例如 high，medium， low）。


你可以添加一些选项来修改队列工作的行为
默认情况下，这些将从将被传递给作业函数的kwargs中弹出。

timeout
指定作业在被视为“丢失”之前的最长运行时间。它的默认单位是秒，它可以是一个整数或表示一个整数的字符串（例如 2，'2'）。此外，它可以是具有指定单元，包括小时，分钟，秒的字符串（例如'1h'，'3m'，'5s'）。

result_ttl
指定存储作业的结果(返回值)key的到期时间

ttl
作业的最长排队时间，如果超过时间则取消任务

depends_on
指定在该作业排队之前必须完成的另一个作业（或作业ID）

job_id
允许你手动指定这个工作的job_id

at_front
将把工作放在队列的前面，而不是后面

kwargs 和 args
让您绕过这些参数的自动弹出，即：timeout为基础作业函数指定参数。


使用显示声明参数版本可能更好更有优势的
```
job = q.enqueue(count_words_at_url, 'http://nvie.com')

q.enqueue_call(func=count_words_at_url, args=('http://nvie.com',), timeout=30)
```

web进程无法访问正在worker中运行的源码，你可以通过传递函数的字符串使用。
```
q = Queue('low', connection=redis_conn)
q.enqueue('my_package.my_module.my_func', 3, 4)
```

除了排队作业，Queues还有一些其他方法：
```
from rq import Queue
from redis import Redis

redis_conn = Redis()
q = Queue(connection=redis_conn) 

# Getting the number of jobs in the queue
# 获取作业在队列中的编号
print len(q)

# Retrieving jobs 检索jobs
queued_job_ids = q.job_ids # Gets a list of job IDs from the queue 返回队列中作业的ID列表
queued_jobs = q.jobs # Gets a list of enqueued job instances 返回排队作业实例列表
job = q.fetch_job('my_id') # Returns job having ID "my_id" 返回含有指定ID的作业
```


作业入队列时，queue.enqueue()方法会返回一个Job实例，这是一个代理对象，可以用来检查实际工作的结果。
Jos对象具有result属性供访问，若返回值为None说明作业尚未完成，若返回指定值则说明该作业完成。
可以适当的加上time.sleep()来确保任务已经完成。


@job装饰器
用法类似与celery，如下
```
from rq.decorators import job

@job('low', connection=my_redis_conn, timeout=5)
def add(x, y):
    return x + y

作业和排队操作不能在一个文件里面
job = add.delay(3, 4)  #传递参数
time.sleep(1)
print job.result
```


出去测试目的可以无需将实际作业交给worker
这需要将async=False参数传递给Queue构造函数
```
>>> q = Queue('low', async=False, connection=my_redis_conn)
>>> job = q.enqueue(fib, 8)
>>> job.result
21
```
类似celery的ALWAYS_EAGER


Job dependencies
作业依赖
新版本rq具有执行混合作业的能力
执行依赖其他作业的作业时，使用depends_on参数指定
```
q = Queue('low', connection=my_redis_conn)
report_job = q.enqueue(generate_report)
q.enqueue(send_report, depends_on=report_job)
```
这允许你把一个大任务分解成多个小人物，依赖于其他作业时只有在其依赖成功完成时才会开始排队执行。


按队列顺序执行工作
$ rq worker high normal low

在一个工人中不会有并发操作，如果你需要则需要启动更多工人。


Burst mode 突发模式
```
rq worker --burst high normal low
```
默认情况：worker启动后立即开始作业，作业完成后置位阻塞状态并等待新作业。
突发模式：worker启动后完成所有当前可用工作，并在给定队列清空后立即退出。


1. 启动
2. 登记
3. 监听
4. 准备执行作业
   状态置为busy
   注册作业到StartedJobRegistry中
5. 启用一个子进程
6. 执行作业
7. 清理作业
   状态置为idle
   基于result_ttl设置作业和执行结果的过期状态
   作业会从StartedJobRegistry中移除
   执行成功的话作业会添加到FinishedJobRegistry中
   执行失败的话会添加到FailedQueue中
8. 从第三步开始循环
   
检索worker信息
```
from redis import Redis
from rq import Queue, Worker

# Returns all workers registered in this connection 返回所有worker在此连接中的注册信息
redis = Redis()
workers = Worker.all(connection=redis)

# Returns all workers in this queue (new in version 0.10.0) 返回此队列中的所有worker
queue = Queue('queue_name')
workers = Worker.all(queue=queue)
```

如果你是想监听worker的数量，使用Worker.count()
```
from redis import Redis
from rq import Worker

redis = Redis()

# Count the number of workers in this Redis connection 此连接中worker数量
workers = Worker.count(connection=redis)

# Count the number of workers for a specific queue 指定队列worker数量
queue = Queue('queue_name', connection=redis)
workers = Worker.all(queue=queue)
```

检查队列使用情况
```
from rq.worker import Worker
worker = Worker.find_by_key('rq:worker:name')

worker.successful_job_count  # Number of jobs finished successfully
worker.failed_job_count. # Number of failed jobs processed by this worker
worker.total_working_time  # Number of time spent executing jobs
```

终止worker
如果工作人员在任何时候收到SIGINT（通过Ctrl + C）或SIGTERM（通过 kill），worker将等待，直到当前正在运行的任务完成，停止工作循环并正常注册自己的终止。

Using a config file
如果你想rq worker通过配置文件来配置而不是通过命令行参数来配置，你可以通过创建一个Python文件来实现 settings.py：
```python
REDIS_URL = 'redis://localhost:6379/1'

# You can also specify the Redis DB to use
# REDIS_HOST = 'redis.example.com'
# REDIS_PORT = 6380
# REDIS_DB = 3
# REDIS_PASSWORD = 'very secret'

# Queues to listen on
QUEUES = ['high', 'normal', 'low']

# If you're using Sentry to collect your runtime exceptions, you can use this
# to configure RQ for it in a single step
# The 'sync+' prefix is required for raven: https://github.com/nvie/rq/issues/350#issuecomment-43592410
SENTRY_DSN = 'sync+http://public:secret@example.com/1'
```
指定配置文件
$ rq worker -c settings



Custom worker classes
自定义工人类
0.4.0版中的新功能。

有些时候你想定制工人的行为。到目前为止，一些比较常见的要求是：

1. 在运行作业之前管理数据库连接。
2. 使用不需要os.forkd的的作业执行模型。
3. 能够使用不同的并发模型，如 multiprocessingor gevent。
您可以使用该-w选项指定要使用的其他工作者类：
```
$ rq worker -w 'path.to.GeventWorker'
```


Custom Job and Queue classes
自定义作业和队列类

Custom exception handlers
自定义异常处理类
如果您需要针对不同类型的作业以不同方式处理错误，或者只是想自定义RQ的默认错误处理行为，请rq worker使用以下--exception-handler选项运行：
```
$ rq worker --exception-handler 'path.to.my.ErrorHandler'

# Multiple exception handlers is also supported
$ rq worker --exception-handler 'path.to.my.ErrorHandler' --exception-handler 'another.ErrorHandler'
```


job returned value 500s 过期
```
q.enqueue(foo)  # result expires after 500 secs (the default) 结果500s后过期
q.enqueue(foo, result_ttl=86400)  # result expires after 1 day 结果1天后过期
q.enqueue(foo, result_ttl=0)  # result gets deleted immediately 结果立即过期
q.enqueue(foo, result_ttl=-1)  # result never expires--you should delete jobs manually 结果从不过期，需要自己手动删除

q.enqueue(func_without_rv, result_ttl=500)  # job kept explicitly # 没有返回值的作业默认情况下在完成后会立即被删除
```


当job内部抛出异常时，它会被worker捕获，序列化并存储在作业的Redis hash exc_info键中，对Job的引用被放在failed队列中。
这项工作本身有一些有用的特性可以用来帮助检查：
- 该作业的原始创作时间
- 最后入队日期
- 始发队列
- 一个所需函数调用的文本描述
- 例外信息


处理工作超时
默认情况下，job应在180秒内执行。之后，worker终止了work house并将工作放到failed队列中，表明工作超时。

如果一项工作需要更多（或更少）时间完成，可以通过将默认超时期限指定为enqueue()呼叫的关键字参数来放宽（或收紧）默认超时期限 ，如下所示：
指定某项任务的timeout
```
q = Queue()
q.enqueue(mytask, args=(foo,), kwargs={'bar': qux}, timeout=600)  # 10 mins
```

直接对队列整体timeout设置司改
您还可以更改一次性通过特定队列实例入列的作业的默认超时时间，这对于这样的模式可能很有用：
```
# High prio jobs should end in 8 secs, while low prio
# work may take up to 10 mins
high = Queue('high', default_timeout=8)  # 8 secs
low = Queue('low', default_timeout=600)  # 10 mins

# Individual jobs can still override these defaults
# 指定job的情况下可以覆盖queue设置的的值
low.enqueue(really_really_slow, timeout=3600)  # 1 hr
```

