import time

from rqde import add


job = add.delay(3, 4)
time.sleep(1)
print(job.result)