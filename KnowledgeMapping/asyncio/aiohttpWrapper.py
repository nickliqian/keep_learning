import aiohttp
import json


async def post(url, data, headers=None):
    async with aiohttp.ClientSession(headers=headers) as session:
        result = await session.post(url, data=data)
        return await result.json()


async def post_text_plain(url, data, headers=None):
    async with aiohttp.ClientSession(headers=headers) as session:
        result = await session.post(url, data=data)
        return await result.text()


async def get(url, headers=None, **kwargs):
    async with aiohttp.ClientSession(headers=headers) as session:
        result = await session.get(url, data=kwargs)
        return await result.json()


async def put(url, data, headers=None):
    async with aiohttp.ClientSession(headers=headers) as session:
        result = await session.put(url, data=data)
        return await result.json()


import asyncio
loop = asyncio.get_event_loop()
result = loop.run_until_complete(get(url="https://www.baidu.com"))
loop.close()