from redis import Redis
from rq import Queue
from myjob import count_words_at_url
import time

q = Queue(connection=Redis())

result = q.enqueue(count_words_at_url, 'http://nvie.com')

