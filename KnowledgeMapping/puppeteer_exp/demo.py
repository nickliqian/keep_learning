#!/usr/bin/python
# -*- coding: UTF-8 -*-
import asyncio
import pyppeteer
import time
import os
import random
from exe_js import js1, js3, js4, js5


def input_time_random():
    return random.randint(100, 151)


async def main():
    print("in main ")
    print(os.environ.get('PYPPETEER_CHROMIUM_REVISION'))
    browser = await pyppeteer.launch(
        executablePath=r"D:\A\Desktop\项目+更新\node_project\chrome-win\chrome-win\chrome.exe",
        headless=False)
    page = await browser.newPage()
    await page.setViewport({"width": 1900, "height": 1100})
    await page.setUserAgent("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36")
    await page.goto('https://www.taobao.com/')

    await page.evaluate(js1)
    await page.evaluate(js3)
    await page.evaluate(js4)
    await page.evaluate(js5)

    await page.type('#q', "IP", {'delay': input_time_random() - 50})
    # await page.click(".search-button button", {'delay': input_time_random()})
    await page.keyboard.press('Enter', {'delay': 1000})

    content = await page.content()
    cookies = await page.cookies()
    await page.screenshot({'path': 'example.png'})
    time.sleep(10)

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