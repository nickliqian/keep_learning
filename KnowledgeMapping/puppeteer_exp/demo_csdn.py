#!/usr/bin/python
# -*- coding: UTF-8 -*-
import asyncio
import pyppeteer
import time
import os
import random
from exe_js import js1, js3, js4, js5

# http://www.mamicode.com/info-detail-2302923.html
"""
{
    proxy: "127.0.0.1:1234",
    proxy-auth: "userx:passx",
    proxy-type: "meh"
}
"""
def input_time_random():
    return random.randint(300, 500)


async def main():
    print("in main ")
    print(os.environ.get('PYPPETEER_CHROMIUM_REVISION'))
    browser = await pyppeteer.launch(
        executablePath=r"D:\A\Desktop\项目+更新\node_project\chrome-win\chrome-win\chrome.exe",
        headless=False,
        args=[
            '--proxy-server=111.177.174.219:9999'
            ])
    page = await browser.newPage()
    await page.setViewport({"width": 1000, "height": 780})
    await page.setUserAgent("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36")
    await page.goto('https://blog.csdn.net/weixin_39198406')
    await page.waitForNavigation({'waitUntil': 'load'})

    await page.evaluate(js1)
    await page.evaluate(js3)
    await page.evaluate(js4)
    await page.evaluate(js5)

    while True:
        ele = await page.J(".js-page-next")  # 如果元素不存在，ele=None
        if ele:
            await page.click(".js-page-next", {'delay': input_time_random() + 300})
            await page.waitForNavigation({'waitUntil': 'load'})
        else:
            break

    content = await page.content()
    cookies = await page.cookies()
    await page.screenshot({'path': 'example.png'})

    dimensions = await page.evaluate('''() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }''')

    print(dimensions)

    await browser.close()
    return {'content': content, 'cookies': cookies}


asyncio.get_event_loop().run_until_complete(main())