import random
import requests


DEFAULT_AGENT = 'wswp'
DEFAULT_DELAY = 5
DEFAULT_RETRIES = 1
DEFAULT_TIMEOUT = 60


class Downloader:
    def __init__(self, delay=DEFAULT_DELAY, user_agent=DEFAULT_AGENT, proxies=None, num_retries=DEFAULT_RETRIES,
                 timeout=DEFAULT_TIMEOUT, opener=None, cache=None):
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.opener = opener
        self.cache = cache

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                pass
            else:
                if self.num_retries > 0 and 500 <= result["code"] < 600:
                    result = None

        if result is None:
            # 获取随机代理，如无代理则置位None
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent': self.user_agent}
            result = self.download(url, headers, proxy=proxy, num_retries=self.num_retries)

            if self.cache:
                self.cache[url] = result
        return result['html']

    def download(self, url, headers, proxy, num_retries, data=None, params=None):
        code = 0
        html = "initEmpty"
        try:
            response = requests.get(url, headers=headers,
                         proxies={"http": proxy, "https": proxy},
                         timeout=DEFAULT_TIMEOUT,
                         data=data,
                         params=params)
            html = response.text
            code = response.status_code
        # e这里代表异常对象，可能会含有某些属性
        except Exception:
            # 如果不是200说明访问失败，在指定条件下重试
            if code != 200:
                if num_retries > 0:
                    return self.download(url, headers, proxy, num_retries - 1, data, params)
        return {'html': html, 'code': code}


