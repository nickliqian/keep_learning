import aiohttp
import asyncio

async def get_status(url, id):
    r = await aiohttp.request("GET", url)
    print(r.status, id)
    r.close()


tasks = []
for i in range(1):
    tasks.append(asyncio.ensure_future(get_status('https://api.github.com/events', id=i)))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()