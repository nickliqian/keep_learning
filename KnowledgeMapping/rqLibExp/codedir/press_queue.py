import time

from redis import Redis
from req_function import count_words_at_url
from rq import Queue


q = Queue("low", connection=Redis())

job = q.enqueue(count_words_at_url, 'http://nvie.com')
job = q.enqueue(count_words_at_url, 'http://nvie.com')
job = q.enqueue(count_words_at_url, 'http://nvie.com')

print(job.result)  # => None

time.sleep(5)
print(job.result)   # => 889