import time

while True:
    now = time.localtime(time.time())
    print("\r" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end="")
    if (7 <= now.tm_hour <= 23) and (now.tm_min in [0, 30]) and (now.tm_sec == 6):
        print("---66666")
    time.sleep(1)
