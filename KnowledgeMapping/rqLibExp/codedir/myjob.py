import requests
import time


def count_words_at_url(url):
    resp = requests.get(url)
    time.sleep(10)
    return len(resp.text.split())


