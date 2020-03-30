import logging
import asyncio, os, json, time
from datetime import datetime
import aiomysql
from aiohttp import web


def index(request):
    return web.Response(body=b'<h1>Awesome</h1>')


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv


logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()


