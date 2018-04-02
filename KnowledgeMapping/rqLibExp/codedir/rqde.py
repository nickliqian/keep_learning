from rq.decorators import job
from redis import Redis


@job("low", connection=Redis(), timeout=5)
def add(x, y):
    return x + y

