import time
import threading
from .downloader import Downloader

SLEEP_TIME = 1


def threaded_crawler(seed_url, delay=5, cache=None, scrape_callback=None, user_agent='wswp', proxies=None,
                     num_retries=1, max_threads=10, timeout=60):
    # 初始化采集任务队列、去重集合和爬虫对象
    crawl_queue = [seed_url]
    seen = {seed_url}
    my_downloader = Downloader(cache=cache, delay=delay, user_agent=user_agent, proxies=proxies,
                               num_retries=num_retries,
                               timeout=timeout)

    # 定义任务
    def process_queue():
        while True:
            try:
                url = crawl_queue.pop()
            except IndexError:
                # 任务队列为空则线程退出
                # ps：除了别的异常线程也会退出
                break
            else:
                # 采集执行者
                html = my_downloader(url)
                # 如果有回掉函数则执行（针对刚刚采集的html，深度取出url）
                if scrape_callback:
                    try:
                        links = scrape_callback(url, html) or []
                    except Exception as e:
                        print('Error in callback for: {}: {}'.format(url, e))
                    else:
                        # 处理url的新增情形
                        for link in links:
                            if not link.startswith(seed_url):
                                link = "".join([seed_url, link])
                            if link not in seen:
                                seen.add(link)
                                crawl_queue.append(link)

    threads = []
    # 检查线程状态
    while threads or crawl_queue:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

        if len(crawl_queue) < 1000:
            add_url()

        # 控制线程数量在最大值之内
        while len(threads) < max_threads and crawl_queue:
            # 创建新线程
            thread = threading.Thread(target=process_queue)
            # 线程设置
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)

        time.sleep(SLEEP_TIME)


def add_url():
    pass
